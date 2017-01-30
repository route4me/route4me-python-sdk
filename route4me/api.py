import json
import requests
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
from .activity_feed import ActivityFeed
from .address import Address
from .address_book import AddressBook
from .api_endpoints import *
from .avoidance_zones import AvoindanceZones
from .exceptions import APIException
from .gps import SetGPS
from .optimization import Optimization
from .orders import Order
from .rapid_address import RapidAddress
from .route import Route
from .territory import Territory
from .utils import json2obj
from .file_uploading import FileUploading
from .members import Members


class Route4Me(object):
    """
    Route4Me Python SDK
    """
# codebeat:disable[TOO_MANY_FUNCTIONS, LOC, ABC]
    def __init__(self,
                 key,
                 headers={'User-Agent': 'python-sdk',
                          'Accept-Encoding': 'identity, deflate, compress, gzip',
                          'Accept': '*/*', },
                 redirects=True, verify_ssl=True, proxies={}):
        self.key = key
        self.response = None
        self.activity_feed = ActivityFeed(self)
        self.address = Address(self)
        self.address_book = AddressBook(self)
        self.avoidance_zones = AvoindanceZones(self)
        self.file_uploading = FileUploading(self)
        self.optimization = Optimization(self)
        self.members = Members(self)
        self.order = Order(self)
        self.setGPS = SetGPS(self)
        self.route = Route(self)
        self.rapid_address = RapidAddress(self)
        self.territory = Territory(self)
        self.headers = headers
        self.redirects = redirects
        self.verify_ssl = verify_ssl
        self.proxies = proxies

    def _build_base_url(self):
        """
        Return API HOST
        :return:
        """
        return '{0}?'.format(API_HOST)

    def show_route_url(self):
        """
        Return GENERATE ROUTE HOST
        :return:
        """
        return '{0}?'.format(SHOW_ROUTE_HOST)

    def activity_feed_url(self):
        """
        Return ACTIVITY FEED HOST
        :return:
        """
        return '{0}?'.format(ACTIVITY_FEED)

    def file_upload_url(self):
        """
        Return FILE UPLOAD HOST
        :return:
        """
        return '{0}?'.format(FILE_UPLOAD_HOST)

    def file_upload_preview_url(self):
        """
        Return FILE UPLOAD PREVIEW HOST
        :return:
        """
        return '{0}?'.format(FILE_UPLOAD_PREVIEW_HOST)

    def file_upload_geocode_url(self):
        """
        Return FILE UPLOAD GEOCODE HOST
        :return:
        """
        return '{0}?'.format(FILE_UPLOAD_GEOCODE_HOST)

    def route_url(self):
        """
        Return GENERATE ROUTE API HOST
        :return:
        """
        return '{0}?'.format(ROUTE_HOST)

    def address_url(self):
        """
        Return GENERATE ADDRESS HOST
        :return:
        """
        return '{0}?'.format(ADDRESS_HOST)

    def order_url(self):
        """
        Return ORDER HOST
        :return:
        """
        return ORDERS_HOST

    def single_geocoder_url(self):
        """
        Return GENERATE GEOCODE HOST
        :return:
        """
        return '{0}?'.format(SINGLE_GEOCODER)

    def member_authenticate_url(self):
        """
        Return MEMBER AUTHENTICATE HOST
        :return:
        """
        return '{0}?'.format(MEMBER_AUTHENTICATE)

    def user_license_url(self):
        """
        Return USER LICENSE HOST
        :return:
        """
        return '{0}?'.format(USER_LICENSE_HOST)

    def validate_session_url(self):
        """
        Return VALIDATE SESSION
        :return:
        """
        return '{0}?'.format(VALIDATE_SESSION)

    def webinar_register_url(self):
        """
        Return WEBINAR REGISTER
        :return:
        """
        return '{0}?'.format(WEBINAR_REGISTER)

    def register_action_url(self):
        """
        Return REGISTER ACTION
        :return:
        """
        return '{0}?'.format(REGISTER_ACTION)

    def verify_device_license_url(self):
        """
        Return VERIFY DEVICE LICENSE
        :return:
        """
        return '{0}?'.format(VERIFY_DEVICE_LICENSE)

    def batch_geocoder_url(self):
        """
        Return GENERATE GEOCODE HOST
        :return:
        """
        return '{0}?'.format(BATCH_GEOCODER)

    def get_users_host_url(self):
        """
        Return GET USERS HOST
        :return:
        """
        return '{0}?'.format(GET_USERS_HOST)

    def add_route_notes_host_url(self):
        """
        Return ADD ROUTE NOTES HOST
        :return:
        """
        return '{0}?'.format(ADD_ROUTE_NOTES_HOST)

    def get_activities_host_url(self):
        """
        Return GET ACTIVITIES HOST
        :return:
        """
        return '{0}?'.format(GET_ACTIVITIES_HOST)

    def duplicate_route_url(self):
        """
        Return DUPLICATE ROUTE URL
        :return:
        """
        return '{0}?'.format(DUPLICATE_ROUTE)

    def share_route_url(self):
        """
        Return SHARE ROUTE URL
        :return:
        """
        return '{0}?'.format(SHARE_ROUTE_HOST)

    def merge_route_url(self):
        """
        Return MERGE ROUTES HOST
        :return:
        """
        return '{0}?'.format(MERGE_ROUTES_HOST)

    def resequence_route_url(self):
        """
        Return RESEQUENCE ROUTE HOST
        :return:
        """
        return '{0}?'.format(RESEQUENCE_ROUTE)

    def move_route_destination_url(self):
        """
        Return MOVE ROUTE DESTINATION URL
        :return:
        """
        return '{0}?'.format(MOVE_ROUTE_DESTINATION)

    def addressbook_url(self):
        """
        Return ADDRESSBOOK HOST
        :return:
        """
        return '{0}?'.format(ADDRESSBOOK)

    def avoidance_url(self):
        """
        Return AVOIDANCE HOST
        :return:
        """
        return '{0}?'.format(AVOIDANCE)

    def territory_url(self):
        """
        Return TERRITORY HOST
        :return:
        """
        return '{0}?'.format(TERRITORY_HOST)

    def export_url(self):
        """
        Return GENERATE EXPORT HOST
        :return:
        """
        return EXPORTER

    def rapid_address_zip_url(self):
        """
        Return GENERATE RAPID ADDRESS ZIP HOST
        :return:
        """
        return RAPID_ADDRESS_ZIP

    def rapid_address_service_url(self):
        """
        Return GENERATE RAPID ADDRESS SERVICE HOST
        :return:
        """
        return RAPID_ADDRESS_SERVICE

    def rapid_address_url(self):
        """
        Return GENERATE RAPID ADDRESS HOST
        :return:
        """
        return RAPID_ADDRESS

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
                             data=data, headers=self.headers, verify=self.verify_ssl)

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
                            data=data, headers=self.headers, verify=self.verify_ssl)

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
                                data=data, headers=self.headers, verify=self.verify_ssl)

    def _request_delete(self, url, request_params, data=None):
        """
        DELETE request
        :param url:
        :param request_params:
        :param data:
        :return:
        """
        return requests.request('DELETE', url, params=request_params,
                                data=data, headers=self.headers, verify=self.verify_ssl)

    def run_optimization(self):
        """
        Run optimization and return response as an object.
        :return: response as an object
        """
        self.response = self.get(self._request_post)
        response = self.response.content
        try:
            response = json2obj(response)
            return response
        except AttributeError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    def reoptimization(self, optimization_id, data={}):
        """
        Execute reoptimization
        :param optimization_id:
        :return: response as a object
        """
        self.optimization.optimization_problem_id(optimization_id)
        self.optimization.reoptimize(1)
        data = {'parameters': data}
        self.response = self._make_request(self._build_base_url(),
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

    def request_address(self, params):
        params.update({'api_key': self.key})
        return self._make_request(self.address_url(), params, None, self._request_get)

    def delete_address(self, params):
        params.update({'api_key': self.key})
        return self._make_request(self.address_url(), params, None, self._request_delete)

    def update_address(self, params, data):
        params.update({'api_key': self.key})
        data = json.dumps(data)
        return self._make_request(self.address_url(), params, data, self._request_put)

    def update_route(self, params, data):
        params.update({'api_key': self.key})
        data = json.dumps(data)
        return self._make_request(self.route_url(), params, data, self._request_put)

# codebeat:enable[TOO_MANY_FUNCTIONS]