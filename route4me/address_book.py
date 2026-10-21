"""The :class:`AddressBook` resource: create, read, update and delete address book contacts."""

from .api_endpoints import ADDRESSBOOK
from .base import Base
from .exceptions import ParamValueException


class AddressBook(Base):
    """Address book: the account's saved contacts.

    Use it as ``route4me.address_book``. Every method sends a request to
    ``/api.v4/address_book.php``.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
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
        """Create a contact.

        Sends ``POST /api.v4/address_book.php`` with the keywords as the JSON
        body.

        :param kwargs: the contact fields. Required: ``address_1``,
            ``cached_lat`` and ``cached_lng``.
        :return: the decoded JSON reply: the new contact, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.
        """
        self.json_data = kwargs
        if not self.check_required_params(self.json_data, self.REQUIRED_FIELDS):
            raise ParamValueException("params", "Params are not complete")
        return self._call_api(ADDRESSBOOK, "post", self.params, body=self.json_data)

    def get_addressbook_contacts(self, **kwargs):
        """List contacts.

        Sends ``GET /api.v4/address_book.php``.

        :param kwargs: query parameters, sent as is, e.g. ``limit`` and
            ``offset``.
        :return: the decoded JSON reply: the contacts, or the
            ``{"errors": ...}`` dict on an API error.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(ADDRESSBOOK, "get", kwargs, required=["api_key"])

    def get_addressbook_contact(self, **kwargs):
        """Get a contact by ID.

        Sends ``GET /api.v4/address_book.php``.

        :param kwargs: query parameters. Required: ``address_id``.
        :return: the decoded JSON reply: the contact, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``address_id`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(ADDRESSBOOK, "get", kwargs, required=["address_id"])

    def update_contact(self, **kwargs):
        """Update a contact.

        Sends ``PUT /api.v4/address_book.php`` with the keywords as the JSON
        body.

        :param kwargs: the fields to change. Required: ``address_id``, the
            contact to update.
        :return: the decoded JSON reply: the updated contact, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``address_id`` is missing.
        """
        if not self.check_required_params(kwargs, ["address_id"]):
            raise ParamValueException("params", "Params are not complete")
        return self._call_api(ADDRESSBOOK, "put", self.params, body=kwargs)

    def delete_addressbook_contact(self, **kwargs):
        """Delete contacts.

        Sends ``DELETE /api.v4/address_book.php`` with the keywords as the
        JSON body.

        :param kwargs: required: ``address_ids``, a list of contact IDs.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``address_ids`` is missing.
        """
        if not self.check_required_params(kwargs, ["address_ids"]):
            raise ParamValueException("params", "Params are not complete")
        return self._call_api(ADDRESSBOOK, "delete", self.params, body=kwargs)
