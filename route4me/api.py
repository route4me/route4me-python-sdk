# -*- coding: utf-8 -*-
# codebeat:disable[TOO_MANY_FUNCTIONS, LOC, ABC, ARITY, TOTAL_LOC]

import requests
import json

from .activity_feed import ActivityFeed
from .address import Address
from .address_book import AddressBook
from .avoidance_zones import AvoindanceZones
from .exceptions import APIException
from .gps import GPS
from .optimization import Optimization
from .orders import Order
from .rapid_address import RapidAddress
from .route import Route
from .territory import Territory
from .file_uploading import FileUploading
from .members import Members
from .vehicles import Vehicle
from .telematics import Telematics
from .api_endpoints import API_HOST
from .route_status import RouteStatus
from .orders_group import OrdersGroup
from .optimization_profiles import OptimizationProfiles


HEADERS = {
    "User-Agent": "Route4Me Python SDK",
    "Accept-Encoding": "identity, deflate, compress, gzip",
    "Accept": "*/*",
}


class Route4Me(object):
    """
    Route4Me Python SDK
    """

    def __init__(
        self, key, headers=HEADERS, redirects=True, verify_ssl=True, proxies={}
    ):
        self.key = key
        self.response = None
        self.activity_feed = ActivityFeed(self)
        self.address = Address(self)
        self.address_book = AddressBook(self)
        self.avoidance_zones = AvoindanceZones(self)
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
        self.headers = headers
        self.redirects = redirects
        self.verify_ssl = verify_ssl
        self.proxies = proxies
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
            raise APIException(response.status_code, response.text, response.url)
        return response

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
        return self._make_request(
            API_HOST, params, request_method, data=json.dumps(self.optimization.data)
        )

    def _request_post(self, url, request_params, data=None, json=None, files=None):
        """
        POST request
        :param url:
        :param request_params:
        :param data:
        :param files:
        :return:
        """
        return requests.post(
            url,
            params=request_params,
            allow_redirects=self.redirects,
            proxies=self.proxies,
            files=files,
            data=data,
            headers=self.headers,
            json=json,
            verify=self.verify_ssl,
        )

    def _request_get(self, url, request_params, data=None):
        """
        GET request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return requests.get(
            url,
            params=request_params,
            allow_redirects=self.redirects,
            proxies=self.proxies,
            data=data,
            headers=self.headers,
            verify=self.verify_ssl,
        )

    def _request_put(self, url, request_params, json=None, data=None):
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
        )

    def _request_delete(self, url, request_params, data=None, json=None):
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
        )

    def run_optimization(self):
        """
        Run optimization and return response as an object.
        :return: response as an object
        """
        self.response = self.get(self._request_post)
        try:
            response = self.response.json()
            return response
        except AttributeError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    def re_optimization(self, optimization_id, data={}):
        """
        Execute reoptimization
        :param optimization_id:
        :param data:
        :return: response as a object
        """
        self.optimization.optimization_problem_id(optimization_id)
        self.optimization.reoptimize(1)
        data = {"parameters": data}
        self.response = self._request_put(
            API_HOST, self.optimization.get_params(), json=data
        )
        try:
            return self.response.json()
        except ValueError:
            raise
        except Exception:
            raise

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
            try:
                f = open(file_name, "w")
                json.dump(
                    self.response.content,
                    f,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4,
                )
                f.close()
            except Exception:
                raise

    def export_request_to_json(self, file_name):
        """
        Export resquest to JSON File
        :param file_name:
        :return:
        """
        if self.optimization.data:
            try:
                f = open(file_name, "w")
                json.dump(
                    self.optimization.data,
                    f,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4,
                )
                f.close()
            except Exception:
                raise


# codebeat:enable[TOO_MANY_FUNCTIONS, LOC, ABC, ARITY, TOTAL_LOC]
