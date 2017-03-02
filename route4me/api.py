import json
import requests

# codebeat:disable[TOO_MANY_FUNCTIONS, LOC, ABC, ARITY, TOTAL_LOC]
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
from route4me.activity_feed import ActivityFeed
from route4me.address import Address
from route4me.address_book import AddressBook
from route4me.avoidance_zones import AvoindanceZones
from route4me.exceptions import APIException
from route4me.gps import SetGPS
from route4me.optimization import Optimization
from route4me.orders import Order
from route4me.rapid_address import RapidAddress
from route4me.route import Route
from route4me.territory import Territory
from route4me.utils import json2obj
from route4me.file_uploading import FileUploading
from route4me.members import Members
from route4me.vehicles import Vehicle
from route4me.constants import HEADERS
from route4me.api_endpoints import API_HOST


class Route4Me(object):
    """
    Route4Me Python SDK
    """

    def __init__(self,
                 key,
                 headers=HEADERS,
                 redirects=True,
                 verify_ssl=True,
                 proxies={}):
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
        self.setGPS = SetGPS(self)
        self.route = Route(self)
        self.rapid_address = RapidAddress(self)
        self.territory = Territory(self)
        self.headers = headers
        self.redirects = redirects
        self.verify_ssl = verify_ssl
        self.proxies = proxies

    def _make_request(self, url, params, data, request_method):
        """
        Make request to API
        :param url:
        :param params:
        :param data:
        :param request_method:
        :return: response
        :raise: APIException
        """
        request_params = self._transform_params(params)
        response = request_method(url, request_params, data)
        if not 200 <= response.status_code < 400:
            raise APIException(response.status_code, response.text,
                               response.url)
        return response

    def _transform_params(self, params):
        """
        Convert params dict to url params
        :param params:
        :return:
        """
        return urlencode(params)

    def get(self, request_method):
        """
        Execute optimization
        :param request_method:
        :return: JSON
        """
        params = self.optimization.get_params()
        return self._make_request(API_HOST, params,
                                  json.dumps(self.optimization.data),
                                  request_method)

    def _request_post(self, url, request_params, data=None, files=None):
        """
        POST request
        :param url:
        :param request_params:
        :param data:
        :param files:
        :return:
        """
        return requests.post(url, params=request_params,
                             allow_redirects=self.redirects,
                             proxies=self.proxies, files=files,
                             data=data, headers=self.headers,
                             verify=self.verify_ssl)

    def _request_get(self, url, request_params, data=None):
        """
        GET request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return requests.get(url, params=request_params,
                            allow_redirects=self.redirects,
                            proxies=self.proxies,
                            data=data,
                            headers=self.headers,
                            verify=self.verify_ssl)

    def _request_put(self, url, request_params, data=None):
        """
        PUT request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return requests.request('PUT', url, params=request_params,
                                proxies=self.proxies,
                                data=data,
                                headers=self.headers,
                                verify=self.verify_ssl)

    def _request_delete(self, url, request_params, data=None):
        """
        DELETE request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return requests.request('DELETE', url, params=request_params,
                                data=data,
                                headers=self.headers,
                                verify=self.verify_ssl)

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
        :return: response as a object
        """
        self.optimization.optimization_problem_id(optimization_id)
        self.optimization.reoptimize(1)
        data = {'parameters': data}
        self.response = self._make_request(API_HOST,
                                           self.optimization.get_params(),
                                           json.dumps(data),
                                           self._request_put)
        try:
            response = json2obj(self.response.content)
            return response
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
        response = json.loads(self.response.content)
        if 'addresses' in response:
            self.address.addresses = self.response['addresses']

    def export_result_to_json(self, file_name):
        """
        Export response to JSON File
        :param file_name:
        :return:
        """
        if self.response:
            try:
                f = open(file_name, 'w')
                f.write(json.dumps(self.response.content,
                                   ensure_ascii=False,
                                   sort_keys=True,
                                   indent=4))
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
                f = open(file_name, 'w')
                f.write(json.dumps(self.optimization.data,
                                   ensure_ascii=False,
                                   sort_keys=True,
                                   indent=4))
                f.close()
            except Exception:
                raise

# codebeat:enable[TOO_MANY_FUNCTIONS, LOC, ABC, ARITY, TOTAL_LOC]
