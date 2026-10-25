"""The :class:`AddressBook` resource: address book contacts and groups (API V4)."""

import warnings

from .api_endpoints import ADDRESS_BOOK_GROUP, ADDRESS_BOOK_GROUP_SEARCH, ADDRESSBOOK, SAVE_GEOCODED_ADDRESSES
from .base import Base
from .exceptions import ParamValueException


class AddressBook(Base):
    """Address book: the account's saved contacts and their groups.

    Use it as ``route4me.address_book``. The contact methods send a request to
    ``/api.v4/address_book.php``, the group methods to
    ``/api.v4/address_book_group.php``. The API V5 address book is
    :class:`~route4me.address_book_v5.AddressBookV5`.

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

        .. deprecated:: 1.0.0
           The C# SDK marks this operation obsolete. Use
           :meth:`~route4me.address_book_v5.AddressBookV5.add_address_book_contact`.
        """
        warnings.warn(
            "AddressBook.create_contact is deprecated: the C# SDK marks it obsolete. "
            "Use AddressBookV5.add_address_book_contact.",
            DeprecationWarning,
            stacklevel=2,
        )
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

        .. deprecated:: 1.0.0
           The C# SDK marks this operation obsolete. Use
           :meth:`~route4me.address_book_v5.AddressBookV5.get_address_book_contacts`.
        """
        warnings.warn(
            "AddressBook.get_addressbook_contacts is deprecated: the C# SDK marks it obsolete. "
            "Use AddressBookV5.get_address_book_contacts.",
            DeprecationWarning,
            stacklevel=2,
        )
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

        .. deprecated:: 1.0.0
           The C# SDK marks this operation obsolete. Use
           :meth:`~route4me.address_book_v5.AddressBookV5.update_address_book_contact`.
        """
        warnings.warn(
            "AddressBook.update_contact is deprecated: the C# SDK marks it obsolete. "
            "Use AddressBookV5.update_address_book_contact.",
            DeprecationWarning,
            stacklevel=2,
        )
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

        .. deprecated:: 1.0.0
           The C# SDK marks this operation obsolete. Use
           :meth:`~route4me.address_book_v5.AddressBookV5.remove_address_book_contacts`.
        """
        warnings.warn(
            "AddressBook.delete_addressbook_contact is deprecated: the C# SDK marks it obsolete. "
            "Use AddressBookV5.remove_address_book_contacts.",
            DeprecationWarning,
            stacklevel=2,
        )
        if not self.check_required_params(kwargs, ["address_ids"]):
            raise ParamValueException("params", "Params are not complete")
        return self._call_api(ADDRESSBOOK, "delete", self.params, body=kwargs)

    # ------------------------------------------------------------ searches

    def search_address_book_contacts_by_filter(self, body, **kwargs):
        """Search contacts with a text filter.

        Sends ``POST /api.v4/address_book.php`` with ``body`` as the JSON body
        and the keywords as the query. The ``filter`` in the body tells this
        search apart from :meth:`create_contact`, which uses the same endpoint.

        :param body: the JSON body: ``filter``, e.g. ``{"query": "Main St",
            "display": "all"}``, and optionally ``fields``, the fields to
            return.
        :param kwargs: query parameters, optional: ``offset`` and ``limit``.
        :return: the decoded JSON reply: the matching contacts, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESSBOOK, "post", dict(kwargs), body=body)

    def get_address_book_contacts_by_group(self, body=None, **kwargs):
        """List the contacts of an address book group.

        Sends ``POST /api/address_book/get_search_group_addresses.php`` with
        ``body`` as the JSON body and the keywords as the query.

        :param body: the JSON body, optional: ``fields``, the fields to
            return, e.g. ``{"fields": ["address_id", "address_1"]}``.
        :param kwargs: query parameters. Required: ``group_id``.
        :return: the decoded JSON reply: the contacts of the group, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``group_id`` is missing.

        .. versionadded:: 1.0.0
        """
        if not self.check_required_params(kwargs, ["group_id"]):
            raise ParamValueException("group_id", "Missing required params")
        return self._call_api(ADDRESS_BOOK_GROUP_SEARCH, "post", dict(kwargs), body=body or {})

    def save_geocoded_addresses_to_database(self, **kwargs):
        """Save geocoded addresses from temporary storage to the address book.

        Sends ``POST /api/address_book/save_geocoded.php`` with the keywords
        as the JSON body.

        :param kwargs: the body. Required: ``optimization_problem_id``, the
            temporary optimization that holds the geocoded addresses.
        :return: the decoded JSON reply, e.g. ``{"status": true}``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``optimization_problem_id`` is
            missing.

        .. versionadded:: 1.0.0
        """
        if not self.check_required_params(kwargs, ["optimization_problem_id"]):
            raise ParamValueException("optimization_problem_id", "Missing required params")
        return self._call_api(SAVE_GEOCODED_ADDRESSES, "post", {}, body=kwargs)

    # -------------------------------------------------------------- groups

    def add_address_book_group(self, **kwargs):
        """Create an address book group.

        Sends ``POST /api.v4/address_book_group.php`` with the keywords as the
        JSON body.

        :param kwargs: the group: ``group_name``, ``group_color`` (a hex color
            such as ``"92e1c0"``), ``group_icon`` and ``filter``, the rules a
            contact must match, e.g. ``{"condition": "AND", "rules": [...]}``.
        :return: the decoded JSON reply: the new group, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_GROUP, "post", {}, body=kwargs)

    def get_address_book_groups(self, **kwargs):
        """List the address book groups, or get one.

        Sends ``GET /api.v4/address_book_group.php``.

        :param kwargs: query parameters, optional: ``group_id`` to get one
            group, or ``offset`` and ``limit`` to page through the list.
        :return: the decoded JSON reply: the list of groups, or the group when
            ``group_id`` is given, or the ``{"errors": ...}`` dict on an API
            error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_GROUP, "get", dict(kwargs))

    def update_address_book_group(self, **kwargs):
        """Update an address book group.

        Sends ``PUT /api.v4/address_book_group.php`` with the keywords as the
        JSON body.

        :param kwargs: the body. Required: ``group_id``, the group to update.
            Optional: ``group_name``, ``group_color``, ``group_icon`` and
            ``filter``.
        :return: the decoded JSON reply: the updated group, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``group_id`` is missing.

        .. versionadded:: 1.0.0
        """
        if not self.check_required_params(kwargs, ["group_id"]):
            raise ParamValueException("group_id", "Missing required params")
        return self._call_api(ADDRESS_BOOK_GROUP, "put", {}, body=kwargs)

    def remove_address_book_group(self, **kwargs):
        """Delete an address book group.

        Sends ``DELETE /api.v4/address_book_group.php`` with the keywords as
        the JSON body.

        :param kwargs: the body. Required: ``group_id``, the group to delete.
        :return: the decoded JSON reply, e.g. ``{"status": true}``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``group_id`` is missing.

        .. versionadded:: 1.0.0
        """
        if not self.check_required_params(kwargs, ["group_id"]):
            raise ParamValueException("group_id", "Missing required params")
        return self._call_api(ADDRESS_BOOK_GROUP, "delete", {}, body=kwargs)
