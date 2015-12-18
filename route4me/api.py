import requests
from urllib import urlencode
from address import Address
from gps import SetGPS
from route import Route
from optimization import Optimization
from utils import *
from exceptions import APIException
from api_endpoints import API_HOST, SHOW_ROUTE_HOST, BATCH_GEOCODER,\
    EXPORTER, SINGLE_GEOCODER


class Route4Me(object):
    """
    Route4Me Python SDK
    """
    def __init__(self, key, headers={'User-Agent': 'python-sdk'}):
        self.key = key
        self.response = None
        self.key = key
        self.address = Address(self)
        self.optimization = Optimization(self)
        self.setGPS = SetGPS(self)
        self.route = Route(self)
        self.headers = headers

    def _build_base_url(self):
        """
        Return API HOST
        :return:
        """
        return '{0}?'.format(API_HOST)

    def route_url(self):
        """
        Return GENERATE ROUTE HOST
        :return:
        """
        return '{0}?'.format(SHOW_ROUTE_HOST)

    def single_geocoder_url(self):
        """
        Return GENERATE GEOCODE HOST
        :return:
        """
        return '{0}?'.format(SINGLE_GEOCODER)

    def batch_geocoder_url(self):
        """
        Return GENERATE GEOCODE HOST
        :return:
        """
        return '{0}?'.format(BATCH_GEOCODER)

    def export_url(self):
        """
        Return GENERATE EXPORT HOST
        :return:
        """
        return EXPORTER

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
        return self._make_request(self._build_base_url(), params,
                                  json.dumps(self.optimization.data),
                                  request_method)

    def _request_post(self, url, request_params, data=None, redirects=True):
        """
        POST request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return requests.post(url, params=request_params,
                             allow_redirects=redirects,
                             data=data, headers=self.headers, verify=False)

    def _request_get(self, url, request_params, data=None, redirects=True):
        """
        GET request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return requests.get(url, params=request_params,
                            allow_redirects=redirects,
                            data=data, headers=self.headers, verify=False)

    def _request_put(self, url, request_params, data=None):
        """
        PUT request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return requests.request('PUT', url, params=request_params,
                                data=data, headers=self.headers, verify=False)

    def _request_delete(self, url, request_params, data=None):
        """
        DELETE request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return requests.request('DELETE', url, params=request_params,
                                data=data, headers=self.headers, verify=False)

    def run_optimization(self):
        """
        Run optimization and return response as an object.
        :return: response as an object
        """
        self.response = self.get(self._request_post)
        return json2obj(self.response.content)

    def reoptimization(self, optimization_id):
        """
        Execute reoptimization
        :param optimization_id:
        :return: response as a object
        """
        request_method = self._request_put
        self.optimization.optimization_problem_id(optimization_id)
        self.optimization.reoptimize(1)
        params = self.optimization.get_params()
        self.response = self._make_request(self._build_base_url(), params, [],
                                           request_method)
        return json2obj(self.response.content)

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
            except Exception as e:
                print e

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
            except Exception as e:
                print e

    def get_batch_geocodes(self, params):
        """
        Get Geocodes from given addresses
        :param params:
        :return: response as a object
        """
        request_method = self._request_get
        self.response = self._make_request(self.batch_geocoder_url(), params,
                                           [], request_method)
        return self.response.content

    def get_geocode(self, params):
        """
        Get Geocodes from given address
        :param params:
        :return: response as a object
        """
        request_method = self._request_get
        self.response = self._make_request(self.single_geocoder_url(), params,
                                           [], request_method)
        return self.response.content

    def export_route(self, route_id, output_format='csv'):
        """
        Get Route from given post data
        :param route_id:
        :param output_format:
        :return: response as a object
        """
        data = {'route_id': route_id, 'strExportFormat': output_format}
        request_method = self._request_post
        self.response = self._make_request(self.export_url(), {}, data,
                                           request_method)
        return self.response.content
