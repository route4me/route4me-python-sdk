import threading
from json import dump, dumps

import requests
from requests.adapters import HTTPAdapter

from ._redact import redact_text
from ._resilience import CircuitBreaker, execute_with_retry
from .activity_feed import ActivityFeed
from .address import Address
from .address_book import AddressBook
from .api_endpoints import API_HOST
from .avoidance_zones import AvoidanceZones
from .config import UNSET, normalize_timeout, resolve, resolve_timeout
from .exceptions import APIException
from .file_uploading import FileUploading
from .gps import GPS
from .members import Members
from .optimization import Optimization
from .optimization_profiles import OptimizationProfiles
from .orders import Order
from .orders_group import OrdersGroup
from .rapid_address import RapidAddress
from .route import Route
from .route_status import RouteStatus
from .telematics import Telematics
from .territory import Territory
from .vehicles import Vehicle

HEADERS = {
    "User-Agent": "Route4Me Python SDK",
    "Accept-Encoding": "identity, deflate, compress, gzip",
    "Accept": "*/*",
}


class Route4Me:  # pylint: disable=too-many-instance-attributes  # one attribute per API resource
    """
    Route4Me Python SDK
    """

    # Public constructor: each keyword mirrors an option of route4me.config.Route4MeConfig.
    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
        self,
        key,
        headers=None,
        redirects=True,
        verify_ssl=True,
        proxies=None,
        timeout=UNSET,
        retry_count=UNSET,
        retry_initial_delay=UNSET,
        enable_circuit_breaker=UNSET,
        circuit_breaker_failure_threshold=UNSET,
        circuit_breaker_duration=UNSET,
        on_retry=UNSET,
        on_circuit_breaker_open=UNSET,
        use_session=UNSET,
        session=None,
    ):
        """
        :param key: Route4Me API key.
        :param headers: request headers, copied per client. ``None`` (the default)
            uses :data:`HEADERS`.
        :param redirects: follow redirects (also sent to the API as
            ``redirect=0`` when disabled).
        :param verify_ssl: verify TLS certificates. Leave this on.
        :param proxies: ``requests``-style proxy mapping.
        :param timeout: per-request timeout in seconds. Accepts ``None`` (wait
            forever -- the pre-0.2.0 behaviour), a number, or a
            ``(connect, read)`` pair. Defaults to
            :data:`route4me.config.DEFAULT_TIMEOUT`, i.e. ``(6.05, 30.0)``.
        :param retry_count: retries after the first attempt. 0 (the default)
            disables retrying. Only idempotent verbs are ever retried -- POST is
            excluded because replaying a create can duplicate server-side work.
        :param retry_initial_delay: exponential-backoff base, in seconds.
        :param enable_circuit_breaker: fail fast after a run of failures.
        :param circuit_breaker_failure_threshold: consecutive failures to open.
        :param circuit_breaker_duration: seconds to stay open.
        :param on_retry: ``callback(exc_or_response, delay, attempt)``.
        :param on_circuit_breaker_open: ``callback(exc, reset_timeout)``.
        :param use_session: reuse one :class:`requests.Session` for connection
            pooling. On by default; without it every call pays a fresh TCP and
            TLS handshake.
        :param session: inject a pre-built session (mainly for testing).

        Any option left unset falls back to
        :class:`route4me.config.Route4MeConfig`, so a whole process can be tuned
        in one place.

        .. versionchanged:: 0.2.0
           Requests now time out after 30s by default; previously there was no
           timeout at all and a stalled socket blocked the calling thread
           indefinitely. Pass ``timeout=None`` to restore the old behaviour.

        .. versionadded:: 0.3.0
           Connection pooling, opt-in retry with exponential backoff, and an
           opt-in circuit breaker.
        """
        self.key = key
        self.response = None
        # Validate eagerly so a bad timeout is a construction-time error rather
        # than a confusing failure on the first request.
        self.timeout = timeout if timeout is UNSET else normalize_timeout(timeout)
        self._retry_count = retry_count
        self._retry_initial_delay = retry_initial_delay
        self._on_retry = on_retry
        self._use_session = use_session
        self._enable_circuit_breaker = enable_circuit_breaker
        self._circuit_breaker_failure_threshold = circuit_breaker_failure_threshold
        self._circuit_breaker_duration = circuit_breaker_duration
        self._on_circuit_breaker_open = on_circuit_breaker_open
        self._session = session
        # requests.Session is not fully thread-safe; serialise the lazy creation
        # so two threads cannot build and pool two different sessions.
        self._session_lock = threading.Lock()
        self._circuit_breaker = None
        self._breaker_lock = threading.Lock()
        self.activity_feed = ActivityFeed(self)
        self.address = Address(self)
        self.address_book = AddressBook(self)
        self.avoidance_zones = AvoidanceZones(self)
        self.file_uploading = FileUploading(self)
        self.optimization = Optimization(self)
        self.members = Members(self)
        self.vehicles = Vehicle(self)
        self.order = Order(self)
        self.gps = GPS(self)
        self.route = Route(self)
        self.rapid_address = RapidAddress(self)
        self.telematics = Telematics(self)
        self.territory = Territory(self)
        # Copy: HEADERS is a module-level dict used as the default argument, so
        # assigning it directly made every client share one object -- mutating
        # one client's headers mutated every other client's and the module
        # constant itself.
        self.headers = dict(HEADERS) if headers is None else dict(headers)
        self.redirects = redirects
        self.verify_ssl = verify_ssl
        self.proxies = proxies if proxies is not None else {}
        self.route_status = RouteStatus(self)
        self.orders_group = OrdersGroup(self)
        self.optimization_profiles = OptimizationProfiles(self)

    def _make_request(self, url, params, request_method, **kwargs):
        """
        Make request to API
        :param url:
        :param params:
        :param request_method:
        :param kwargs: additional arguments
        :return: response
        :raise: APIException
        """
        # Copy rather than mutate. Every resource passes its own long-lived
        # `self.params`, so writing api_key in place meant query parameters
        # accumulated on that dict across calls and leaked between them.
        params = dict(params) if params else {}
        params["api_key"] = self.key
        response = request_method(url, params, **kwargs)
        if not 200 <= response.status_code < 400:
            # Both the URL and the body are scrubbed. `Response.url` carries
            # `?api_key=<plaintext>` for V4, and several V4 endpoints echo the
            # request parameters back inside their error payloads, so the key
            # can appear in the body as well.
            raise APIException(
                response.status_code,
                redact_text(response.text, self.key),
                response.url,
            )
        return response

    # ------------------------------------------------------------- transport

    def _timeout(self, per_call=UNSET):
        """Resolve the effective timeout: per-call > constructor > global."""
        return resolve_timeout(per_call, self.timeout)

    def _setting(self, per_call, per_client, name):
        return resolve(per_call, per_client, name)

    @property
    def session(self):
        """The pooled :class:`requests.Session`, or ``None`` when disabled.

        Created on first use under a lock: ``requests.Session`` is not fully
        thread-safe, and two threads racing here would build two sessions and
        silently halve the benefit of pooling.
        """
        if not self._setting(UNSET, self._use_session, "use_session"):
            return None
        if self._session is None:
            with self._session_lock:
                if self._session is None:
                    self._session = self._build_session()
        return self._session

    def _build_session(self):
        session = requests.Session()
        pool = self._setting(UNSET, UNSET, "pool_maxsize")
        # Retries are handled in `_resilience`, not by urllib3 -- see that
        # module's docstring for why. The adapter is mounted purely for pooling.
        adapter = HTTPAdapter(pool_connections=pool, pool_maxsize=pool, max_retries=0)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    @property
    def circuit_breaker(self):
        """The shared :class:`CircuitBreaker`, or ``None`` when disabled."""
        if not self._setting(UNSET, self._enable_circuit_breaker, "enable_circuit_breaker"):
            return None
        if self._circuit_breaker is None:
            with self._breaker_lock:
                if self._circuit_breaker is None:
                    self._circuit_breaker = CircuitBreaker(
                        failure_threshold=self._setting(
                            UNSET,
                            self._circuit_breaker_failure_threshold,
                            "circuit_breaker_failure_threshold",
                        ),
                        reset_timeout=self._setting(UNSET, self._circuit_breaker_duration, "circuit_breaker_duration"),
                        on_open=self._setting(UNSET, self._on_circuit_breaker_open, "on_circuit_breaker_open"),
                    )
        return self._circuit_breaker

    def _send(self, method, url, **kwargs):
        """Issue one HTTP request through the session, with retry and breaker.

        All four ``_request_*`` helpers funnel through here, so pooling, retry,
        the breaker and the timeout apply uniformly -- including to every API V5
        manager added later, which need not know any of this exists.
        """
        kwargs.setdefault("verify", self.verify_ssl)
        proxies = self.proxies or None
        if proxies is not None:
            kwargs.setdefault("proxies", proxies)

        session = self.session
        caller = session.request if session is not None else requests.request

        def send():
            return caller(method, url, **kwargs)

        return execute_with_retry(
            send,
            method,
            retry_count=self._setting(UNSET, self._retry_count, "retry_count"),
            initial_delay=self._setting(UNSET, self._retry_initial_delay, "retry_initial_delay"),
            circuit_breaker=self.circuit_breaker,
            on_retry=self._setting(UNSET, self._on_retry, "on_retry"),
        )

    # -------------------------------------------------------------- lifecycle

    def close(self):
        """Close the pooled session and release its connections.

        Safe to call more than once, and safe to call when pooling is disabled.
        """
        with self._session_lock:
            if self._session is not None:
                self._session.close()
                self._session = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False

    def get(self, request_method):
        """
        Execute optimization
        :param request_method:
        :return: JSON
        """
        params = self.optimization.get_params()
        if not self.redirects:
            params.update(
                {
                    "redirect": 0,
                }
            )
        return self._make_request(API_HOST, params, request_method, data=dumps(self.optimization.data))

    def _request_post(self, url, request_params, *, data=None, json=None, files=None, timeout=UNSET):
        """
        POST request
        :param url:
        :param request_params:
        :param data:
        :param files:
        :return:
        """
        return self._send(
            "POST",
            url,
            params=request_params,
            allow_redirects=self.redirects,
            files=files,
            data=data,
            headers=self.headers,
            json=json,
            timeout=self._timeout(timeout),
        )

    def _request_get(self, url, request_params, *, data=None, timeout=UNSET):
        """
        GET request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return self._send(
            "GET",
            url,
            params=request_params,
            allow_redirects=self.redirects,
            data=data,
            headers=self.headers,
            timeout=self._timeout(timeout),
        )

    def _request_put(self, url, request_params, *, json=None, data=None, timeout=UNSET):
        """
        PUT request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return self._send(
            "PUT",
            url,
            params=request_params,
            data=data,
            json=json,
            headers=self.headers,
            timeout=self._timeout(timeout),
        )

    def _request_delete(self, url, request_params, *, data=None, json=None, timeout=UNSET):
        """
        DELETE request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return self._send(
            "DELETE",
            url,
            params=request_params,
            data=data,
            json=json,
            headers=self.headers,
            timeout=self._timeout(timeout),
        )

    def run_optimization(self):
        """
        Run optimization and return response as an object.
        :return: response as an object
        """
        self.response = self.get(self._request_post)
        return self.response.json()

    def re_optimization(self, optimization_id, data=None):
        """
        Execute reoptimization
        :param optimization_id:
        :param data:
        :return: response as a object
        :raise APIException: on a non-2xx/3xx response

        .. versionchanged:: 0.3.1
           Routed through ``_make_request``. It previously called
           ``_request_put`` directly and so never raised on an HTTP error --
           callers got ``response.json()`` of an error body, or a
           ``JSONDecodeError`` if the server returned HTML.
        """
        if data is None:
            data = {}
        self.optimization.optimization_problem_id(optimization_id)
        self.optimization.reoptimize(1)
        data = {"parameters": data}
        self.response = self._make_request(API_HOST, self.optimization.get_params(), self._request_put, json=data)
        return self.response.json()

    def get_optimization(self, optimization_problem_id):
        """
        Get optimization given optimization_problem_id
        :param optimization_problem_id:
        :return: the parsed optimization payload

        .. versionchanged:: 0.3.1
           Now returns the payload. It previously returned ``None`` always, and
           raised ``TypeError`` for any response containing ``addresses`` --
           which is every real optimization response -- via ``parse_response``.
        """
        self.optimization.optimization_problem_id(optimization_problem_id)
        self.response = self.get(self._request_get)
        return self.parse_response()

    def parse_response(self):
        """
        Parse response and set it to Route4me instance
        :return: the parsed response payload

        .. versionchanged:: 0.3.1
           Reads the decoded payload. It previously subscripted
           ``self.response`` -- a :class:`requests.Response`, which is not
           subscriptable -- raising ``TypeError``.
        """
        payload = self.response.json()
        if isinstance(payload, dict) and "addresses" in payload:
            self.address.addresses = payload["addresses"]
        return payload

    def export_result_to_json(self, file_name):
        """
        Export response to JSON File
        :param file_name:
        :return:

        .. versionchanged:: 0.3.1
           Serialises the decoded payload. It previously passed
           ``Response.content`` (``bytes``) to ``json.dump``, which raises
           ``TypeError: Object of type bytes is not JSON serializable`` -- so
           this method had never worked.
        """
        if self.response:
            with open(file_name, "w") as f:
                dump(
                    self.response.json(),
                    f,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4,
                )

    def export_request_to_json(self, file_name):
        """
        Export resquest to JSON File
        :param file_name:
        :return:
        """
        if self.optimization.data:
            with open(file_name, "w") as f:
                dump(
                    self.optimization.data,
                    f,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4,
                )
