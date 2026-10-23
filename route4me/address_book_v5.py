"""The :class:`AddressBookV5` resource (API V5): address book contacts and groups.

.. versionadded:: 1.0.0
"""

import json

from ._url import path_segment
from .api_endpoints import (
    ADDRESS_BOOK_CONTACTS_ALL_V5,
    ADDRESS_BOOK_CONTACTS_BATCH_CREATE_V5,
    ADDRESS_BOOK_CONTACTS_BATCH_UPDATE_V5,
    ADDRESS_BOOK_CONTACTS_CLUSTERING_V5,
    ADDRESS_BOOK_CONTACTS_CUSTOM_FIELDS_V5,
    ADDRESS_BOOK_CONTACTS_DELETE_BY_AREAS_V5,
    ADDRESS_BOOK_CONTACTS_DELETE_V5,
    ADDRESS_BOOK_CONTACTS_DEPOTS_V5,
    ADDRESS_BOOK_CONTACTS_EXPORT_BY_AREA_IDS_V5,
    ADDRESS_BOOK_CONTACTS_EXPORT_BY_AREAS_V5,
    ADDRESS_BOOK_CONTACTS_EXPORT_RESULT_V5,
    ADDRESS_BOOK_CONTACTS_EXPORT_STATUS_V5,
    ADDRESS_BOOK_CONTACTS_EXPORT_V5,
    ADDRESS_BOOK_CONTACTS_PAGINATED_V5,
    ADDRESS_BOOK_CONTACTS_SHOW_V5,
    ADDRESS_BOOK_CONTACTS_UPDATE_BY_AREAS_V5,
    ADDRESS_BOOK_CONTACTS_V5,
    ADDRESS_BOOK_GROUPS_FILTER_ALL_V5,
    ADDRESS_BOOK_GROUPS_V5,
    ADDRESS_BOOK_JOB_RESULT_V5,
    ADDRESS_BOOK_JOB_STATUS_V5,
)
from .base import Base
from .exceptions import APIException, ParamValueException


class AddressBookV5(Base):
    """Address book (API V5): the account's saved contacts and their groups.

    Use it as ``route4me.address_book_v5``. It mirrors the C# SDK's
    ``AddressBookContactsManagerV5``. Every method sends a request to
    ``/modules/api/v5.0/address-book/...`` on ``wh.route4me.com``; the client
    sends the API key as a bearer token. The V4 address book is
    :class:`~route4me.address_book.AddressBook`.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    Some operations run as a background job: the API then answers
    ``202 Accepted`` with an empty body. Those methods return the raw body
    (``b""``), and the reply headers, such as ``Location``, stay readable in
    :attr:`response`.

    .. versionadded:: 1.0.0
    """

    CONTACT_REQUIRED_FIELDS = ("address_1", "cached_lat", "cached_lng")

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    def _check_required(self, params, required):
        """Raise when a required field is missing.

        :param params: the fields given.
        :param required: the names that must be present.
        :raise ParamValueException: naming every missing field.
        """
        missing = self._missing(params, required)
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")

    def _call_job_api(self, endpoint, method, body):
        """Send a request whose reply may be an empty ``202 Accepted``.

        :param endpoint: absolute URL of the API endpoint.
        :param method: ``"post"``, ``"put"`` or ``"delete"``.
        :param body: the JSON body.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error. The
            reply itself is kept in :attr:`response`.
        """
        try:
            self.response = self._request(endpoint, {}, method, json=body)
        except APIException as e:
            return e.to_dict()
        try:
            return json.loads(self.response.content)
        except ValueError:
            return self.response.content

    # ------------------------------------------------------------- contacts

    def get_address_book_contacts(self, **kwargs):
        """List contacts, filtered by query parameters.

        Sends ``GET /modules/api/v5.0/address-book/addresses/index/all``.

        :param kwargs: query parameters, all optional: ``fields`` (the fields
            to return), ``display`` (``"all"``, ``"routed"`` or
            ``"unrouted"``), ``display_list``, ``query`` (text to search for),
            ``limit`` and ``offset``. A list is sent as repeated keys.
        :return: the decoded JSON reply: the contacts and their total, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_CONTACTS_ALL_V5, "get", dict(kwargs))

    def get_address_book_contacts_by_body(self, **kwargs):
        """List contacts, filtered and sorted by a JSON body.

        Sends ``POST /modules/api/v5.0/address-book/addresses/index/all`` with
        the keywords as the JSON body. This is the POST form of
        :meth:`get_address_book_contacts`; it can also search inside areas.

        :param kwargs: the body, all optional: ``query``, ``fields``,
            ``filter`` (e.g. ``{"display": "routed", "selected_areas": [...]}``),
            ``order_by`` (e.g. ``[["address_alias", "asc"]]``), ``limit`` and
            ``offset``.
        :return: the decoded JSON reply: the contacts and their total, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_CONTACTS_ALL_V5, "post", {}, body=kwargs)

    def get_address_book_contacts_paginated(self, **kwargs):
        """List one page of contacts, filtered by query parameters.

        Sends ``GET /modules/api/v5.0/address-book/addresses/index/pagination``.

        :param kwargs: query parameters, all optional: ``fields``,
            ``display``, ``display_list``, ``query``, ``page`` and
            ``per_page``.
        :return: the decoded JSON reply: one page of contacts, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_CONTACTS_PAGINATED_V5, "get", dict(kwargs))

    def get_address_book_contacts_paginated_by_body(self, **kwargs):
        """List one page of contacts, filtered and sorted by a JSON body.

        Sends ``POST /modules/api/v5.0/address-book/addresses/index/pagination``
        with the keywords as the JSON body. This is the POST form of
        :meth:`get_address_book_contacts_paginated`.

        :param kwargs: the body, all optional: ``query``, ``fields``,
            ``filter``, ``order_by``, ``page`` and ``per_page``.
        :return: the decoded JSON reply: one page of contacts, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_CONTACTS_PAGINATED_V5, "post", {}, body=kwargs)

    def get_address_book_contacts_clustering(self, **kwargs):
        """Get the contacts grouped into map clusters, filtered by query parameters.

        Sends ``GET /modules/api/v5.0/address-book/addresses/index/clustering``.

        :param kwargs: query parameters, all optional: ``display``,
            ``display_list`` and ``query``.
        :return: the decoded JSON reply: the clusters, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_CONTACTS_CLUSTERING_V5, "get", dict(kwargs))

    def get_address_book_contacts_clustering_by_body(self, **kwargs):
        """Get the contacts grouped into map clusters, filtered by a JSON body.

        Sends ``POST /modules/api/v5.0/address-book/addresses/index/clustering``
        with the keywords as the JSON body. This is the POST form of
        :meth:`get_address_book_contacts_clustering`.

        :param kwargs: the body, all optional: ``query``, ``clustering``
            (e.g. ``{"precision": 5}``) and ``filter``.
        :return: the decoded JSON reply: the clusters, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_CONTACTS_CLUSTERING_V5, "post", {}, body=kwargs)

    def get_address_book_contacts_by_ids(self, **kwargs):
        """Get several contacts by their IDs.

        Sends ``POST /modules/api/v5.0/address-book/addresses/show`` with the
        keywords as the JSON body.

        :param kwargs: the body: ``address_ids``, a list of contact IDs.
        :return: the decoded JSON reply: the contacts, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_CONTACTS_SHOW_V5, "post", {}, body=kwargs)

    def get_depots_from_address_book(self):
        """List the contacts marked as depots.

        Sends ``GET /modules/api/v5.0/address-book/addresses/depots``.

        :return: the decoded JSON reply: the depot contacts, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_CONTACTS_DEPOTS_V5, "get", {})

    def get_custom_fields(self):
        """List the custom fields used by the contacts.

        Sends ``GET /modules/api/v5.0/address-book/addresses/custom-fields``.

        :return: the decoded JSON reply: the custom field names, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_CONTACTS_CUSTOM_FIELDS_V5, "get", {})

    def add_address_book_contact(self, **kwargs):
        """Create a contact.

        Sends ``POST /modules/api/v5.0/address-book/addresses`` with the
        keywords as the JSON body.

        :param kwargs: the contact fields. Required: ``address_1``,
            ``cached_lat`` and ``cached_lng``. Others include
            ``address_alias``, ``first_name``, ``last_name``,
            ``address_email``, ``address_phone_number``,
            ``address_custom_data``, ``address_stop_type`` and
            ``service_time``.
        :return: the decoded JSON reply: the new contact, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        self._check_required(kwargs, self.CONTACT_REQUIRED_FIELDS)
        return self._call_api(ADDRESS_BOOK_CONTACTS_V5, "post", {}, body=kwargs)

    def batch_create_address_book_contacts(self, **kwargs):
        """Create several contacts in one request.

        Sends ``POST /modules/api/v5.0/address-book/addresses/batch-create``
        with the keywords as the JSON body.

        :param kwargs: the body: ``data``, a list of contacts. Each contact
            takes the fields of :meth:`add_address_book_contact` and needs
            ``address_1``, ``cached_lat`` and ``cached_lng``.
        :return: the decoded JSON reply, e.g. ``{"status": true}``, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_CONTACTS_BATCH_CREATE_V5, "post", {}, body=kwargs)

    def update_address_book_contact(self, address_id, **kwargs):
        """Update a contact.

        Sends ``PUT /modules/api/v5.0/address-book/addresses/{address_id}``
        with the keywords as the JSON body.

        :param address_id: ID of the contact.
        :param kwargs: the contact fields, as for
            :meth:`add_address_book_contact`. The API requires
            ``address_1``, ``cached_lat`` and ``cached_lng`` here too.
        :return: the decoded JSON reply: the updated contact, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``address_id`` is empty or a required
            field is missing.

        .. versionadded:: 1.0.0
        """
        url = f"{ADDRESS_BOOK_CONTACTS_V5}/{path_segment(address_id, 'address_id')}"
        self._check_required(kwargs, self.CONTACT_REQUIRED_FIELDS)
        return self._call_api(url, "put", {}, body=kwargs)

    def batch_update_address_book_contact(self, **kwargs):
        """Give several contacts the same field values.

        Sends ``PUT /modules/api/v5.0/address-book/addresses/batch-update``
        with the keywords as the JSON body.

        :param kwargs: the body: ``address_ids``, the contacts to update,
            and the fields to set on all of them, e.g. ``address_group`` or
            ``service_time``.
        :return: the decoded JSON reply: the updated contacts, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_CONTACTS_BATCH_UPDATE_V5, "put", {}, body=kwargs)

    def update_address_book_contact_by_areas(self, **kwargs):
        """Give the contacts inside some areas the same field values.

        Sends ``PUT /modules/api/v5.0/address-book/addresses/update-by-areas``
        with the keywords as the JSON body. The API runs the update as a
        background job.

        :param kwargs: the body: ``filter``, which contacts to update (``query``,
            ``bounding_box`` or ``selected_areas``), and ``data``, the fields to
            set.
        :return: the decoded JSON reply, the raw body (``bytes``, ``b""`` when
            the job is queued) when it is not JSON, or the ``{"errors": ...}``
            dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_job_api(ADDRESS_BOOK_CONTACTS_UPDATE_BY_AREAS_V5, "put", kwargs)

    def remove_address_book_contacts(self, **kwargs):
        """Delete contacts.

        Sends ``DELETE /modules/api/v5.0/address-book/addresses/delete`` with
        the keywords as the JSON body. The API may run the deletion as a
        background job.

        :param kwargs: the body: ``address_ids``, a list of contact IDs.
        :return: the decoded JSON reply, the raw body (``bytes``, ``b""`` when
            the job is queued) when it is not JSON, or the ``{"errors": ...}``
            dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_job_api(ADDRESS_BOOK_CONTACTS_DELETE_V5, "delete", kwargs)

    def remove_address_book_contacts_by_areas(self, **kwargs):
        """Delete the contacts inside some areas.

        Sends ``DELETE /modules/api/v5.0/address-book/addresses/delete-by-areas``
        with the keywords as the JSON body. It mirrors C#
        ``RemoveAddressBookContactsByAreas``. The API runs the deletion as a
        background job; follow it with :meth:`get_contacts_job_status`.

        :param kwargs: the body: ``filter``, the areas, as for
            :meth:`update_address_book_contact_by_areas`, for example
            ``{"query": "...", "bounding_box": {...}}``.
        :return: the decoded JSON reply, the raw body (``bytes``, ``b""`` when
            the job is queued) when it is not JSON, or the ``{"errors": ...}``
            dict on an API error.
        :raise ParamValueException: when ``filter`` is missing.

        .. versionadded:: 1.0.0
        """
        self._check_required(kwargs, ["filter"])
        return self._call_job_api(ADDRESS_BOOK_CONTACTS_DELETE_BY_AREAS_V5, "delete", kwargs)

    def export_addresses(self, **kwargs):
        """Export contacts to a file.

        Sends ``POST /modules/api/v5.0/address-book/addresses/export`` with the
        keywords as the JSON body. The API builds the file in a background job.

        :param kwargs: the body: ``ids``, the contact IDs, and optionally
            ``filename``, ``extension`` (``"csv"``, ``"xls"`` or ``"xlsx"``)
            and ``tz``, the time zone of the dates.
        :return: the decoded JSON reply, the raw body (``bytes``, ``b""`` when
            the job is queued) when it is not JSON, or the ``{"errors": ...}``
            dict on an API error. The API answers ``202 Accepted`` with the
            export's status URL, ``.../export/status/{id}``, in the
            ``Location`` header of :attr:`response`; pass its last segment to
            :meth:`get_export_status`, then :meth:`get_export_result`.

        .. versionadded:: 1.0.0
        """
        return self._call_job_api(ADDRESS_BOOK_CONTACTS_EXPORT_V5, "post", kwargs)

    def get_export_status(self, export_id):
        """Get the status of a contact export.

        Sends ``GET /modules/api/v5.0/address-book/addresses/export/status/{export_id}``.

        :param export_id: the export's ID: the last segment of the
            ``Location`` header of the export reply.
        :return: the decoded JSON reply, a status string, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``export_id`` is empty.

        .. versionadded:: 1.0.0
        """
        url = f"{ADDRESS_BOOK_CONTACTS_EXPORT_STATUS_V5}/{path_segment(export_id, 'export_id')}"
        return self._call_api(url, "get", {})

    def get_export_result(self, export_id):
        """Download the file of a finished contact export.

        Sends ``GET /modules/api/v5.0/address-book/addresses/export/result/{export_id}``.

        :param export_id: the export's ID, as for :meth:`get_export_status`.
        :return: the file (``bytes``, for example CSV), or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``export_id`` is empty.

        .. versionadded:: 1.0.0
        """
        url = f"{ADDRESS_BOOK_CONTACTS_EXPORT_RESULT_V5}/{path_segment(export_id, 'export_id')}"
        try:
            return self._request(url, {}, "get").content
        except APIException as e:
            return e.to_dict()

    def export_addresses_by_areas(self, **kwargs):
        """Export the contacts inside some areas to a file.

        Sends ``POST /modules/api/v5.0/address-book/addresses/export-by-areas``
        with the keywords as the JSON body. The API builds the file in a
        background job.

        :param kwargs: the body: ``filter``, with ``query``, ``bounding_box``
            or ``selected_areas``, and optionally ``filename``, ``extension``
            and ``tz``.
        :return: the decoded JSON reply, the raw body (``bytes``, ``b""`` when
            the job is queued) when it is not JSON, or the ``{"errors": ...}``
            dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_job_api(ADDRESS_BOOK_CONTACTS_EXPORT_BY_AREAS_V5, "post", kwargs)

    def export_addresses_by_area_ids(self, **kwargs):
        """Export the contacts inside some territories to a file.

        Sends ``POST /modules/api/v5.0/address-book/addresses/export-by-area-ids``
        with the keywords as the JSON body. The API builds the file in a
        background job.

        :param kwargs: the body: ``territory_ids``, a list of territory IDs,
            and optionally ``filename``, ``extension`` and ``tz``.
        :return: the decoded JSON reply, the raw body (``bytes``, ``b""`` when
            the job is queued) when it is not JSON, or the ``{"errors": ...}``
            dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_job_api(ADDRESS_BOOK_CONTACTS_EXPORT_BY_AREA_IDS_V5, "post", kwargs)

    # ----------------------------------------------------------------- jobs

    def get_contacts_job_status(self, job_id):
        """Get the status of a background address book job.

        Sends ``GET /modules/api/v5.0/address-book/job-tracker/status/{job_id}``.
        A method that starts a job, such as :meth:`export_addresses` or
        :meth:`update_address_book_contact_by_areas`, returns ``b""``; the job
        ID is the last segment of the ``Location`` header of its reply.

        :param job_id: ID of the job.
        :return: the decoded JSON reply, with the job ``status``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``job_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(f"{ADDRESS_BOOK_JOB_STATUS_V5}/{path_segment(job_id, 'job_id')}", "get", {})

    def get_contacts_job_result(self, job_id):
        """Get the result of a finished background address book job.

        Sends ``GET /modules/api/v5.0/address-book/job-tracker/result/{job_id}``.

        :param job_id: ID of the job, as for :meth:`get_contacts_job_status`.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``job_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(f"{ADDRESS_BOOK_JOB_RESULT_V5}/{path_segment(job_id, 'job_id')}", "get", {})

    # --------------------------------------------------------------- groups

    def get_address_book_groups(self):
        """List the address book groups.

        Sends ``GET /modules/api/v5.0/address-book/groups``.

        :return: the decoded JSON reply: the groups, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ADDRESS_BOOK_GROUPS_V5, "get", {})

    def filter_contacts_by_group_rules(self, body, **kwargs):
        """List the contacts that match address book group rules.

        Sends ``POST /modules/api/v5.0/address-book/groups/filter/all`` with
        ``body`` as the JSON body and the keywords as the query.

        :param body: the JSON body. Required: ``rules``, the group rules,
            e.g. ``{"condition": "AND", "rules": [{"id": "address_1",
            "field": "address_1", "operator": "contains", "value": "Main"}]}``.
            Optional: ``bounding_box``, ``fields``, ``order_by``, ``limit``
            and ``offset``.
        :param kwargs: query parameters, optional: ``display`` (``"all"``,
            ``"routed"`` or ``"unrouted"``).
        :return: the decoded JSON reply: the matching contacts, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``rules`` is missing from ``body``.

        .. versionadded:: 1.0.0
        """
        self._check_required(body, ["rules"])
        return self._call_api(ADDRESS_BOOK_GROUPS_FILTER_ALL_V5, "post", dict(kwargs), body=body)
