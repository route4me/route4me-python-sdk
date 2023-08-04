# -*- coding: utf-8 -*-

from .api_endpoints import TELEMATICS_VENDORS_V4, TELEMATICS_REGISTER_V4
from .api_endpoints import TELEMATICS_CONNECTIONS_V4, TELEMATICS_VENDORS_INFO_V4
from .base import Base
from .exceptions import ParamValueException, APIException


class Telematics(Base):
    """
    Telematics Management
    """

    def __init__(self, api):
        """
        Telematics Instance
        :param api:
        :return:
        """
        Base.__init__(self, api)

    @staticmethod
    def pp_response(response):
        if isinstance(response, dict):
            for k, v in response.items():
                print("{} : {}".format(k, v))
            print('')

    @staticmethod
    def pp_vendor_comparison(vendor):
        if isinstance(vendor, dict):
            features = [x['name'] for x in vendor['features']]
            print('{}\t{}\t{}'.format(vendor['id'], vendor['name'], ', '.join(features)))

    def get_vendors(self):
        if self.check_required_params(self.params, ['api_key', ]):
            try:
                self.response = self.api._make_request(TELEMATICS_VENDORS_V4,
                                                       self.params,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Missing API KEY')

    def get_vendor(self, vendor_id):

        self.params.update({'vendor_id': vendor_id})

        if self.check_required_params(self.params, ['api_key']):
            try:
                self.response = self.api._make_request(TELEMATICS_VENDORS_V4,
                                                       self.params,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Missing API KEY')

    def search_vendor(self, **kwargs):

        kwargs.update({'api_key': self.params['api_key'], })

        if self.check_required_params(kwargs, ['api_key']):
            try:
                self.response = self.api._make_request(TELEMATICS_VENDORS_V4,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Missing API KEY')

    def compare_vendors(self, vendors_id):

        self.params.update({'vendors': vendors_id})

        if self.check_required_params(self.params, ['api_key']):
            try:
                self.response = self.api._make_request(TELEMATICS_VENDORS_V4,
                                                       self.params,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Missing API KEY')

    def register_member(self, member_id):
        self.params.update({'member_id': member_id})

        if self.check_required_params(self.params, ['api_key']):
            try:
                self.response = self.api._make_request(TELEMATICS_REGISTER_V4,
                                                       self.params,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Missing API KEY')

    def get_connections(self, api_token, **kwargs):
        kwargs.update({"api_token": api_token})

        if self.check_required_params(kwargs, ['api_token']):
            try:
                self.response = self.api._make_request(TELEMATICS_CONNECTIONS_V4,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Missing API Token')

    def get_vendors_info(self, api_token, **kwargs):
        kwargs.update({"api_token": api_token})

        if self.check_required_params(kwargs, ['api_token']):
            try:
                self.response = self.api._make_request(TELEMATICS_VENDORS_INFO_V4,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Missing API Token')

    def register_connection(self, api_token, **kwargs):
        params = {"api_token": api_token}
        kwargs.update({"validate_remote_credentials": "true"})
        if self.check_required_params(kwargs, ['vendor_id']):
            try:
                self.response = self.api._make_request(TELEMATICS_CONNECTIONS_V4,
                                                       params,
                                                       self.api._request_post,
                                                       json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Missing Vendor ID')

    def get_connection(self, api_token, connection_token):
        params = {
            "api_token": api_token,
            "connection_token": connection_token
        }
        try:
            self.response = self.api._make_request(TELEMATICS_CONNECTIONS_V4,
                                                   params,
                                                   self.api._request_get)
            return self.response.json()
        except APIException as e:
            return e.to_dict()

    def delete_connection(self, api_token, connection_token):
        params = {
            "api_token": api_token,
            "connection_token": connection_token
        }
        try:
            self.response = self.api._make_request(TELEMATICS_CONNECTIONS_V4,
                                                   params,
                                                   self.api._request_delete)
            return self.response.json()
        except APIException as e:
            e.to_dict()

    def update_connection(self, api_token, connection_token, **kwargs):
        params = {
            "api_token": api_token,
            "connection_token": connection_token
        }
        kwargs.update({"validate_remote_credentials": "true"})
        if self.check_required_params(kwargs, ['vendor_id']):
            try:
                self.response = self.api._make_request(TELEMATICS_CONNECTIONS_V4,
                                                       params,
                                                       self.api._request_put,
                                                       json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Missing Vendor ID')
