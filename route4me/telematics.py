# -*- coding: utf-8 -*-

from .api_endpoints import TELEMATICS_VENDORS_V4, TELEMATICS_REGISTER_V4
from .api_endpoints import TELEMATICS_CONNECTIONS_V4, TELEMATICS_VENDORS_INFO_V4
from .base import Base
from .exceptions import ParamValueException


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
            self.response = self.api._request_get(TELEMATICS_VENDORS_V4,
                                                  self.params)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Missing API KEY')

    def get_vendor(self, vendor_id):

        self.params.update({'vendor_id': vendor_id})

        if self.check_required_params(self.params, ['api_key']):
            self.response = self.api._request_get(TELEMATICS_VENDORS_V4,
                                                  self.params)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Missing API KEY')

    def search_vendor(self, **kwargs):

        kwargs.update({'api_key': self.params['api_key'], })

        if self.check_required_params(kwargs, ['api_key']):
            self.response = self.api._request_get(TELEMATICS_VENDORS_V4,
                                                  kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Missing API KEY')

    def compare_vendors(self, vendors_id):

        self.params.update({'vendors': vendors_id})

        if self.check_required_params(self.params, ['api_key']):
            self.response = self.api._request_get(TELEMATICS_VENDORS_V4,
                                                  self.params)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Missing API KEY')

    def register_member(self, member_id):
        self.params.update({'member_id': member_id})

        if self.check_required_params(self.params, ['api_key']):
            self.response = self.api._request_get(TELEMATICS_REGISTER_V4,
                                                  self.params)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Missing API KEY')

    def get_connections(self, api_token, **kwargs):
        kwargs.update({"api_token": api_token})

        if self.check_required_params(kwargs, ['api_token']):
            self.response = self.api._request_get(TELEMATICS_CONNECTIONS_V4,
                                                  kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Missing API Token')

    def get_vendors_info(self, api_token, **kwargs):
        kwargs.update({"api_token": api_token})

        if self.check_required_params(kwargs, ['api_token']):
            self.response = self.api._request_get(TELEMATICS_VENDORS_INFO_V4,
                                                  kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Missing API Token')

    def register_connection(self, api_token, **kwargs):
        params = {"api_token": api_token}
        kwargs.update({"validate_remote_credentials": "true"})
        if self.check_required_params(kwargs, ['vendor_id']):
            self.response = self.api._request_post(TELEMATICS_CONNECTIONS_V4,
                                                   params,
                                                   data=kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Missing Vendor ID')

    def get_connection(self, api_token, connection_token):
        params = {
            "api_token": api_token,
            "connection_token": connection_token
        }
        self.response = self.api._request_get(TELEMATICS_CONNECTIONS_V4,
                                              params)
        return self.response.json()

    def delete_connection(self, api_token, connection_token):
        params = {
            "api_token": api_token,
            "connection_token": connection_token
        }
        self.response = self.api._request_delete(TELEMATICS_CONNECTIONS_V4,
                                                 params)
        return self.response.json()

    def update_connection(self, api_token, connection_token, **kwargs):
        params = {
            "api_token": api_token,
            "connection_token": connection_token
        }
        kwargs.update({"validate_remote_credentials": "true"})
        if self.check_required_params(kwargs, ['vendor_id']):
            self.response = self.api._request_put(TELEMATICS_CONNECTIONS_V4,
                                                  params,
                                                  data=kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Missing Vendor ID')
