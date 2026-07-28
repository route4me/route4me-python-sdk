import json

import requests

from ._redact import redact_text
from .activity_feed import ActivityFeed
from .address import Address
from .address_book import AddressBook
from .api_endpoints import API_HOST
from .avoidance_zones import AvoidanceZones
from .config import UNSET, normalize_timeout, resolve_timeout
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


class Route4Me:
    """
    Route4Me Python SDK
    """

    def __init__(self, key, headers=HEADERS, redirects=True, verify_ssl=True, proxies=None, timeout=UNSET):
        """
        :param key: Route4Me API key.
        :param headers: request headers; copied, never shared between clients.
        :param redirects: follow redirects (also sent to the API as
            ``redirect=0`` when disabled).
        :param verify_ssl: verify TLS certificates. Leave this on.
        :param proxies: ``requests``-style proxy mapping.
        :param timeout: per-request timeout in seconds. Accepts ``None`` (wait
            forever -- the pre-0.2.0 behaviour), a number, or a
            ``(connect, read)`` pair. Defaults to
            :data:`route4me.config.DEFAULT_TIMEOUT`, i.e. ``(6.05, 30.0)``.

        .. versionchanged:: 0.2.0
           Requests now time out after 30s by default; previously there was no
           timeout at all and a stalled socket blocked the calling thread
           indefinitely. Pass ``timeout=None`` to restore the old behaviour.
        """
        self.key = key
        self.response = None
        # Validate eagerly so a bad timeout is a construction-time error rather
        # than a confusing failure on the first request.
        self.timeout = timeout if timeout is UNSET else normalize_timeout(timeout)
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

    def _timeout(self, per_call=UNSET):
        """Resolve the effective timeout: per-call > constructor > global."""
        return resolve_timeout(per_call, self.timeout)

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
        return self._make_request(API_HOST, params, request_method, data=json.dumps(self.optimization.data))

    def _request_post(self, url, request_params, data=None, json=None, files=None, timeout=UNSET):
        """
        POST request
        :param url:
        :param request_params:
        :param data:
        :param files:
        :return:
        """
        return requests.post(  # nosec B113 - timeout is supplied below via self._timeout()
            url,
            params=request_params,
            allow_redirects=self.redirects,
            proxies=self.proxies,
            files=files,
            data=data,
            headers=self.headers,
            json=json,
            verify=self.verify_ssl,
            timeout=self._timeout(timeout),
        )

    def _request_get(self, url, request_params, data=None, timeout=UNSET):
        """
        GET request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return requests.get(  # nosec B113 - timeout is supplied below via self._timeout()
            url,
            params=request_params,
            allow_redirects=self.redirects,
            proxies=self.proxies,
            data=data,
            headers=self.headers,
            verify=self.verify_ssl,
            timeout=self._timeout(timeout),
        )

    def _request_put(self, url, request_params, json=None, data=None, timeout=UNSET):
        """
        PUT request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return requests.request(
            "PUT",
            url,
            params=request_params,
            proxies=self.proxies,
            data=data,
            json=json,
            headers=self.headers,
            verify=self.verify_ssl,
            timeout=self._timeout(timeout),
        )

    def _request_delete(self, url, request_params, data=None, json=None, timeout=UNSET):
        """
        DELETE request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return requests.request(
            "DELETE",
            url,
            params=request_params,
            data=data,
            json=json,
            headers=self.headers,
            verify=self.verify_ssl,
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
        """
        if data is None:
            data = {}
        self.optimization.optimization_problem_id(optimization_id)
        self.optimization.reoptimize(1)
        data = {"parameters": data}
        self.response = self._request_put(API_HOST, self.optimization.get_params(), json=data)
        return self.response.json()

    def get_optimization(self, optimization_problem_id):
        """
        Get optimization given optimization_problem_id
        :param optimization_problem_id:
        :return:
        """
        self.optimization.optimization_problem_id(optimization_problem_id)
        self.response = self.get(self._request_get)
        self.parse_response()

    def parse_response(self):
        """
        Parse response and set it to Route4me instance
        :return:
        """
        response = self.response.json()
        if "addresses" in response:
            self.address.addresses = self.response["addresses"]

    def export_result_to_json(self, file_name):
        """
        Export response to JSON File
        :param file_name:
        :return:
        """
        if self.response:
            with open(file_name, "w") as f:
                json.dump(
                    self.response.content,
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
                json.dump(
                    self.optimization.data,
                    f,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4,
                )
