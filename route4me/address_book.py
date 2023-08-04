# -*- coding: utf-8 -*-

from .api_endpoints import ADDRESSBOOK
from .base import Base
from .exceptions import ParamValueException, APIException


class AddressBook(Base):
    """
    Address Book Management
    """
    REQUIRED_FIELDS = ('address_1', 'cached_lat', 'cached_lng',)

    def __init__(self, api):
        """
        AddressBook Instance
        :param api:
        :return:
        """
        self.json_data = {}
        Base.__init__(self, api)

    def create_contact(self, **kwargs):
        """
        Create a contact in AddressBook using POST request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        self.json_data = kwargs
        if self.check_required_params(self.json_data, self.REQUIRED_FIELDS):
            try:
                self.response = self.api._make_request(ADDRESSBOOK,
                                                       self.params,
                                                       self.api._request_post,
                                                       json=self.json_data)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_addressbook_contacts(self, **kwargs):
        """
        Get contacts from AddressBook using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['api_key', ]):
            try:
                self.response = self.api._make_request(ADDRESSBOOK,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_addressbook_contact(self, **kwargs):
        """
        Get a contact from AddressBook using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['address_id', ]):
            try:
                self.response = self.api._make_request(ADDRESSBOOK,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def update_contact(self, **kwargs):
        """
        Update a contact from AddressBook using PUT request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        if self.check_required_params(kwargs, ['address_id', ]):
            try:
                self.response = self.api._make_request(ADDRESSBOOK,
                                                       self.params,
                                                       self.api._request_put,
                                                       json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def delete_addressbook_contact(self, **kwargs):
        """
        Delete a contact from AddressBook using DELETE request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        if self.check_required_params(kwargs, ['address_ids', ]):
            try:
                self.response = self.api._make_request(ADDRESSBOOK,
                                                       self.params,
                                                       self.api._request_delete,
                                                       json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Params are not complete')
