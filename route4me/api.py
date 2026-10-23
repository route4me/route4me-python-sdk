"""The :class:`Route4Me` client.

The client owns the HTTP session, the timeout, retry and circuit-breaker
settings, and one attribute per API resource (``route4me.route``,
``route4me.optimization``, ...). Every request a resource sends goes through it.
"""

import threading
from json import dump, dumps

import requests
from requests.adapters import HTTPAdapter

from ._redact import redact_text
from ._resilience import CircuitBreaker, execute_with_retry
from ._url import is_v5_url
from .account_profile import AccountProfile
from .activity_feed import ActivityFeed
from .address import Address
from .address_barcodes import AddressBarcodes
from .address_book import AddressBook
from .address_book_v5 import AddressBookV5
from .api_endpoints import API_HOST
from .asset_tracking import AssetTracking
from .auth_history import AuthHistory
from .autocomplete import Autocomplete
from .avoidance_zones import AvoidanceZones
from .config import UNSET, normalize_timeout, resolve, resolve_timeout
from .configuration_settings import ConfigurationSettings
from .configuration_settings_v5 import ConfigurationSettingsV5
from .distance import Distance
from .drivers import Drivers
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
from .route_destinations_v5 import RouteDestinationsV5
from .route_status import RouteStatus
from .routes_v5 import RoutesV5
from .team_v5 import TeamV5
from .telematics import Telematics
from .territory import Territory
from .vehicle_capacity_profiles import VehicleCapacityProfiles
from .vehicle_profiles import VehicleProfiles
from .vehicles import Vehicle
from .vehicles_v5 import VehiclesV5

HEADERS = {
    "User-Agent": "Route4Me Python SDK",
    "Accept-Encoding": "identity, deflate, compress, gzip",
    "Accept": "*/*",
}


class Route4Me:  # pylint: disable=too-many-instance-attributes  # one attribute per API resource
    """Client for the Route4Me API.

    Each API area is a resource attribute: :attr:`account_profile`,
    :attr:`activity_feed`, :attr:`address`, :attr:`address_barcodes`,
    :attr:`address_book`, :attr:`address_book_v5`, :attr:`asset_tracking`,
    :attr:`auth_history`, :attr:`autocomplete`, :attr:`avoidance_zones`,
    :attr:`configuration_settings`, :attr:`configuration_settings_v5`,
    :attr:`distance`, :attr:`drivers`, :attr:`file_uploading`, :attr:`gps`,
    :attr:`members`, :attr:`optimization`, :attr:`optimization_profiles`,
    :attr:`order`, :attr:`orders_group`, :attr:`rapid_address`, :attr:`route`,
    :attr:`route_destinations_v5`, :attr:`route_status`, :attr:`routes_v5`,
    :attr:`team_v5`, :attr:`telematics`, :attr:`territory`,
    :attr:`vehicle_capacity_profiles`, :attr:`vehicle_profiles`,
    :attr:`vehicles` and :attr:`vehicles_v5`.

    The client can be used as a context manager; leaving the block closes the
    pooled session::

        from route4me import Route4Me

        with Route4Me("11111111111111111111111111111111") as route4me:
            routes = route4me.route.get_routes(limit=10, offset=0)

    Resource methods return the decoded JSON reply, or on an API error the
    ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>`. The optimization methods of
    this class (:meth:`run_optimization`, :meth:`re_optimization`,
    :meth:`get_optimization`) raise :class:`~route4me.exceptions.APIException`
    instead.
    """

    # Public constructor: each keyword mirrors an option of route4me.config.Route4MeConfig.
    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals,too-many-statements
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
        """Create a client for one API key.

        :param key: Route4Me API key.
        :param headers: request headers, copied per client. ``None`` (the default)
            uses :data:`HEADERS`.
        :param redirects: follow redirects. When disabled, the optimization
            requests (:meth:`run_optimization`, :meth:`get_optimization`) also
            send ``redirect=0`` to the API.
        :param verify_ssl: verify TLS certificates. Leave this on.
        :param proxies: ``requests``-style proxy mapping.
        :param timeout: per-request timeout in seconds. Accepts ``None`` (wait
            forever -- the behaviour before 1.0.0), a number, or a
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

        .. versionchanged:: 1.0.0
           Requests now time out after 30s by default; previously there was no
           timeout at all and a stalled socket blocked the calling thread
           indefinitely. Pass ``timeout=None`` to restore the old behaviour.

        .. versionadded:: 1.0.0
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
        self.account_profile = AccountProfile(self)
        self.address_barcodes = AddressBarcodes(self)
        self.address_book_v5 = AddressBookV5(self)
        self.asset_tracking = AssetTracking(self)
        self.auth_history = AuthHistory(self)
        self.autocomplete = Autocomplete(self)
        self.configuration_settings = ConfigurationSettings(self)
        self.configuration_settings_v5 = ConfigurationSettingsV5(self)
        self.distance = Distance(self)
        self.drivers = Drivers(self)
        self.route_destinations_v5 = RouteDestinationsV5(self)
        self.routes_v5 = RoutesV5(self)
        self.team_v5 = TeamV5(self)
        self.vehicle_capacity_profiles = VehicleCapacityProfiles(self)
        self.vehicle_profiles = VehicleProfiles(self)
        self.vehicles_v5 = VehiclesV5(self)

    def _make_request(self, url, params, request_method, **kwargs):
        """Send one request, adding the API key, and raise on an HTTP error.

        API V5 requests (``https://wh.route4me.com/modules/api/v5.x/...``) carry
        the key as an ``Authorization: Bearer`` header, which keeps it out of
        URLs and therefore out of proxy and server logs. Every other request
        carries it as the ``api_key`` query parameter, which the V4 API requires.

        :param url: absolute URL of the API endpoint.
        :param params: query parameters. They are copied, and the key is added
            to the copy; the caller's dict is not changed. ``True`` and
            ``False`` are sent as ``1`` and ``0``.
        :param request_method: one of :meth:`_request_get`,
            :meth:`_request_post`, :meth:`_request_put` or
            :meth:`_request_delete`.
        :param kwargs: ``data``, ``json``, ``files`` or ``timeout``, passed
            through to ``request_method``.
        :return: the :class:`requests.Response`.
        :raise APIException: when the API answers outside the 200-399 range.
            The API key is removed from the stored body and URL.

        .. versionchanged:: 1.0.0
           API V5 requests send the key as a bearer token instead of
           ``api_key``. Boolean query values are sent as ``1`` and ``0``.
        """
        # Copy rather than mutate. Every resource passes its own long-lived
        # `self.params`, so writing api_key in place meant query parameters
        # accumulated on that dict across calls and leaked between them.
        # requests would send True as "True": PHP reads "False" as true, and
        # the V5 (Laravel) boolean rule accepts only 1, 0, true and false.
        params = {k: int(v) if isinstance(v, bool) else v for k, v in params.items()} if params else {}
        if is_v5_url(url):
            params.pop("api_key", None)
            kwargs["headers"] = {**self.headers, "Authorization": f"Bearer {self.key}"}
        else:
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
        """Resolve the effective timeout: per-call > constructor > global.

        :param per_call: timeout given for this call, or ``UNSET``.
        :return: the normalised timeout to pass to ``requests``.
        """
        return resolve_timeout(per_call, self.timeout)

    def _setting(self, per_call, per_client, name):
        """Resolve one layered setting: per-call > constructor > global.

        :param per_call: value given for this call, or ``UNSET``.
        :param per_client: value given to the constructor, or ``UNSET``.
        :param name: attribute name on :class:`~route4me.config.Route4MeConfig`.
        :return: the effective value.
        """
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
        """Build the pooled session, with retries disabled in the adapter.

        :return: a new :class:`requests.Session`.
        """
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

        :param method: HTTP verb, e.g. ``"GET"``.
        :param url: absolute URL of the API endpoint.
        :param kwargs: keyword arguments for :meth:`requests.Session.request`.
        :return: the final :class:`requests.Response`, whatever its status.
        :raise CircuitBreakerOpen: when the circuit breaker is open.
        :raise requests.RequestException: when the last attempt fails at the
            transport level (connection error, timeout, ...).
        """
        kwargs.setdefault("verify", self.verify_ssl)
        proxies = self.proxies or None
        if proxies is not None:
            kwargs.setdefault("proxies", proxies)

        session = self.session
        caller = session.request if session is not None else requests.request

        def send():
            """Perform one attempt.

            :return: the :class:`requests.Response`.
            """
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
        """Enter a ``with`` block.

        :return: this client.
        """
        return self

    def __exit__(self, exc_type, exc, tb):
        """Close the pooled session when the ``with`` block ends.

        :param exc_type: type of the exception raised in the block, if any.
        :param exc: the exception raised in the block, if any.
        :param tb: its traceback, if any.
        :return: ``False``, so an exception raised in the block propagates.
        """
        self.close()
        return False

    def get(self, request_method, params=None):
        """Send the optimization built on :attr:`optimization`.

        Sends a request to ``/api.v4/optimization_problem.php`` with the query
        parameters of :attr:`optimization` and its ``data`` serialised to JSON
        as the body. When redirects are disabled, ``redirect=0`` is added to
        the query.

        :param request_method: :meth:`_request_post` to create an optimization,
            :meth:`_request_get` to fetch one.
        :param params: the query to send; ``None`` (the default) uses a copy of
            the query parameters of :attr:`optimization`.
        :return: the :class:`requests.Response`.
        :raise APIException: when the API answers outside the 200-399 range.
        """
        params = dict(self.optimization.get_params() if params is None else params)
        if not self.redirects:
            params["redirect"] = 0
        return self._make_request(API_HOST, params, request_method, data=dumps(self.optimization.data))

    def _request_post(self, url, request_params, *, data=None, json=None, files=None, timeout=UNSET, headers=None):
        """Send a POST request through :meth:`_send`.

        :param url: absolute URL of the API endpoint.
        :param request_params: query parameters.
        :param data: form fields, or a pre-encoded body.
        :param json: body to send as JSON.
        :param files: files for a multipart upload.
        :param timeout: per-call timeout; ``UNSET`` uses the client's.
        :param headers: request headers; ``None`` uses the client's :attr:`headers`.
        :return: the :class:`requests.Response`.
        """
        return self._send(
            "POST",
            url,
            params=request_params,
            allow_redirects=self.redirects,
            files=files,
            data=data,
            headers=self.headers if headers is None else headers,
            json=json,
            timeout=self._timeout(timeout),
        )

    def _request_get(self, url, request_params, *, data=None, timeout=UNSET, headers=None):
        """Send a GET request through :meth:`_send`.

        :param url: absolute URL of the API endpoint.
        :param request_params: query parameters.
        :param data: request body, if any.
        :param timeout: per-call timeout; ``UNSET`` uses the client's.
        :param headers: request headers; ``None`` uses the client's :attr:`headers`.
        :return: the :class:`requests.Response`.
        """
        return self._send(
            "GET",
            url,
            params=request_params,
            allow_redirects=self.redirects,
            data=data,
            headers=self.headers if headers is None else headers,
            timeout=self._timeout(timeout),
        )

    def _request_put(self, url, request_params, *, json=None, data=None, timeout=UNSET, headers=None):
        """Send a PUT request through :meth:`_send`.

        :param url: absolute URL of the API endpoint.
        :param request_params: query parameters.
        :param json: body to send as JSON.
        :param data: form fields, or a pre-encoded body.
        :param timeout: per-call timeout; ``UNSET`` uses the client's.
        :param headers: request headers; ``None`` uses the client's :attr:`headers`.
        :return: the :class:`requests.Response`.
        """
        return self._send(
            "PUT",
            url,
            params=request_params,
            allow_redirects=self.redirects,
            data=data,
            json=json,
            headers=self.headers if headers is None else headers,
            timeout=self._timeout(timeout),
        )

    def _request_patch(self, url, request_params, *, json=None, data=None, timeout=UNSET, headers=None):
        """Send a PATCH request through :meth:`_send`.

        API V5 uses PATCH for partial updates. Like PUT, it is never retried.

        :param url: absolute URL of the API endpoint.
        :param request_params: query parameters.
        :param json: body to send as JSON.
        :param data: form fields, or a pre-encoded body.
        :param timeout: per-call timeout; ``UNSET`` uses the client's.
        :param headers: request headers; ``None`` uses the client's :attr:`headers`.
        :return: the :class:`requests.Response`.

        .. versionadded:: 1.0.0
        """
        return self._send(
            "PATCH",
            url,
            params=request_params,
            allow_redirects=self.redirects,
            data=data,
            json=json,
            headers=self.headers if headers is None else headers,
            timeout=self._timeout(timeout),
        )

    def _request_delete(self, url, request_params, *, data=None, json=None, timeout=UNSET, headers=None):
        """Send a DELETE request through :meth:`_send`.

        :param url: absolute URL of the API endpoint.
        :param request_params: query parameters.
        :param data: form fields, or a pre-encoded body.
        :param json: body to send as JSON.
        :param timeout: per-call timeout; ``UNSET`` uses the client's.
        :param headers: request headers; ``None`` uses the client's :attr:`headers`.
        :return: the :class:`requests.Response`.
        """
        return self._send(
            "DELETE",
            url,
            params=request_params,
            allow_redirects=self.redirects,
            data=data,
            json=json,
            headers=self.headers if headers is None else headers,
            timeout=self._timeout(timeout),
        )

    def run_optimization(self):
        """Create an optimization from the parameters and addresses set so far.

        Sends ``POST /api.v4/optimization_problem.php`` with the request built
        on :attr:`optimization`: its route parameters, and the addresses added
        with :meth:`Address.add_address <route4me.address.Address.add_address>`.

        :return: the decoded JSON reply: the optimization problem, with its
            routes and addresses.
        :raise APIException: when the API answers outside the 200-399 range.
        """
        self.response = self.get(self._request_post)
        return self.response.json()

    def re_optimization(self, optimization_id, data=None):
        """Re-optimize an existing optimization.

        Sends ``PUT /api.v4/optimization_problem.php`` with
        ``optimization_problem_id`` and ``reoptimize=1`` in the query and
        ``{"parameters": data}`` as the JSON body.

        :param optimization_id: ID of the optimization problem.
        :param data: route parameters to change before re-optimizing, e.g.
            ``{"route_name": "Monday"}``. ``None`` sends no changes.
        :return: the decoded JSON reply: the re-optimized problem.
        :raise ParamValueException: when ``optimization_id`` is not a string.
        :raise APIException: when the API answers outside the 200-399 range.

        .. versionchanged:: 1.0.0
           Routed through ``_make_request``. It previously called
           ``_request_put`` directly and so never raised on an HTTP error --
           callers got ``response.json()`` of an error body, or a
           ``JSONDecodeError`` if the server returned HTML.
        """
        if data is None:
            data = {}
        params = self.optimization.validated_params(optimization_problem_id=optimization_id, reoptimize=1)
        data = {"parameters": data}
        self.response = self._make_request(API_HOST, params, self._request_put, json=data)
        return self.response.json()

    def get_optimization(self, optimization_problem_id):
        """Get an optimization by ID.

        Sends ``GET /api.v4/optimization_problem.php``. When the reply has
        ``addresses``, they are also stored on :attr:`address`.

        :param optimization_problem_id: ID of the optimization problem.
        :return: the decoded JSON reply: the optimization problem.
        :raise ParamValueException: when ``optimization_problem_id`` is not a
            string.
        :raise APIException: when the API answers outside the 200-399 range.

        .. versionchanged:: 1.0.0
           Now returns the payload. It previously returned ``None`` always, and
           raised ``TypeError`` for any response containing ``addresses`` --
           which is every real optimization response -- via ``parse_response``.
        """
        params = self.optimization.validated_params(optimization_problem_id=optimization_problem_id)
        self.response = self.get(self._request_get, params)
        return self.parse_response()

    def parse_response(self):
        """Decode the last response and keep its addresses.

        When the decoded reply is a dict with ``addresses``, they are stored on
        :attr:`address` (see :meth:`Address.get_addresses
        <route4me.address.Address.get_addresses>`).

        :return: the decoded JSON of :attr:`response`.

        .. versionchanged:: 1.0.0
           Reads the decoded payload. It previously subscripted
           ``self.response`` -- a :class:`requests.Response`, which is not
           subscriptable -- raising ``TypeError``.
        """
        payload = self.response.json()
        if isinstance(payload, dict) and "addresses" in payload:
            self.address.addresses = payload["addresses"]
        return payload

    def export_result_to_json(self, file_name):
        """Write the decoded JSON of the last response to a file.

        Does nothing when no request has been sent yet.

        :param file_name: path of the file to write; an existing file is
            overwritten.

        .. versionchanged:: 1.0.0
           Serialises the decoded payload. It previously passed
           ``Response.content`` (``bytes``) to ``json.dump``, which raises
           ``TypeError: Object of type bytes is not JSON serializable`` -- so
           this method had never worked.
        """
        if self.response:
            with open(file_name, "w", encoding="utf-8") as f:
                dump(
                    self.response.json(),
                    f,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4,
                )

    def export_request_to_json(self, file_name):
        """Write the optimization request body built so far to a file.

        :param file_name: path of the file to write; an existing file is
            overwritten.
        """
        if self.optimization.data:
            with open(file_name, "w", encoding="utf-8") as f:
                dump(
                    self.optimization.data,
                    f,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4,
                )
