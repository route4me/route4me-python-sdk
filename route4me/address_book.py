import json

from .base import Base
from .exceptions import ParamValueException
from .utils import json2obj


class AddressBook(Base):
    """
    Address Book Management
    """
    REQUIRED_FIELDS = ['address_1', 'cached_lat', 'cached_lng', ]

    def __init__(self, api, addresses=[]):
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
            self.response = self.api._request_post(self.api.addressbook_url(),
                                                   self.params, data=json.dumps(self.json_data, ensure_ascii=False))
            return self.response.content

        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_addressbook_contacts(self, **kwargs):
        """
        Get contacts from AddressBook using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['limit', 'Offset', ]):
            self.response = self.api._request_get(self.api.addressbook_url(),
                                                  kwargs)
            response = json.loads(self.response.content)
            return response
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
            self.response = self.api._request_get(self.api.addressbook_url(),
                                                  kwargs)
            response = json.loads(self.response.content)
            return response
        else:
            raise ParamValueException('params', 'Params are not complete')

    def update_contact(self, **kwargs):
        """
        Update a contact from AddressBook using PUT request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        if self.check_required_params(kwargs, ['address_id', ]):
            self.response = self.api._request_put(self.api.addressbook_url(),
                                                  self.params, data=json.dumps(kwargs))
            response = json.loads(self.response.content)
            return response
        else:
            raise ParamValueException('params', 'Params are not complete')

    def delete_addressbook_contact(self, **kwargs):
        """
        Delete a contact from AddressBook using DELETE request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        if self.check_required_params(kwargs, ['address_ids', ]):
            self.response = self.api._request_delete(self.api.addressbook_url(),
                                                     self.params, data=json.dumps(kwargs))
            response = json2obj(self.response.content)
            return response
        else:
            raise ParamValueException('params', 'Params are not complete')
