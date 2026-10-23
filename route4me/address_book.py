from ._api_method import make_request
from .api_endpoints import ADDRESSBOOK
from .base import Base
from .exceptions import ParamValueException


class AddressBook(Base):
    """
    Address Book Management
    """

    REQUIRED_FIELDS = (
        "address_1",
        "cached_lat",
        "cached_lng",
    )

    def __init__(self, api):
        self.json_data = {}
        Base.__init__(self, api)

    def create_contact(self, **kwargs):
        self.json_data = kwargs
        if not self.check_required_params(self.json_data, self.REQUIRED_FIELDS):
            raise ParamValueException("params", "Params are not complete")
        return make_request(self, ADDRESSBOOK, "post", self.params, body=self.json_data)

    def get_addressbook_contacts(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(self, ADDRESSBOOK, "get", kwargs, required=["api_key"])

    def get_addressbook_contact(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(self, ADDRESSBOOK, "get", kwargs, required=["address_id"])

    def update_contact(self, **kwargs):
        if not self.check_required_params(kwargs, ["address_id"]):
            raise ParamValueException("params", "Params are not complete")
        return make_request(self, ADDRESSBOOK, "put", self.params, body=kwargs)

    def delete_addressbook_contact(self, **kwargs):
        if not self.check_required_params(kwargs, ["address_ids"]):
            raise ParamValueException("params", "Params are not complete")
        return make_request(self, ADDRESSBOOK, "delete", self.params, body=kwargs)
