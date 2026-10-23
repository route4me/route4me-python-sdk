"""The :class:`OrdersV5` resource (API V5): archived orders, order history, batch actions and custom fields."""

from ._url import path_int, path_segment
from .api_endpoints import (
    ORDERS_ARCHIVE_V5,
    ORDERS_CUSTOM_FIELDS_V5,
    ORDERS_HISTORY_V5,
    ORDERS_PLATFORM_BATCH_CREATE_V5,
    ORDERS_PLATFORM_BATCH_DELETE_V5,
    ORDERS_PLATFORM_BATCH_UPDATE_FILTER_V5,
    ORDERS_PLATFORM_BATCH_UPDATE_V5,
    ORDERS_PLATFORM_CUSTOM_USER_FIELDS_V5,
    ORDERS_PLATFORM_V5,
)
from .base import Base
from .exceptions import ParamValueException


class OrdersV5(Base):
    """Orders on API V5: archive, history, batch actions and custom fields.

    Use it as ``route4me.orders_v5``. It mirrors the C# ``OrderManagerV5``.
    Requests go to ``/modules/api/v5.0/orders/...`` and
    ``/modules/api/v5.0/orders-platform/...`` on ``wh.route4me.com``. For the
    API V4 orders see :class:`~route4me.orders.Order`.

    Order custom fields have two API V5 families, and this class offers both:
    the ``orders-platform/order-custom-user-fields`` methods
    (:meth:`get_custom_user_fields` and the rest, keyed by field UUID) and the
    ``orders/custom-fields`` methods (:meth:`get_order_custom_fields` and the
    rest, keyed by integer field ID).

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    #: Body fields the spec requires to create an ``orders-platform`` custom user field.
    CUSTOM_USER_FIELD_CREATE_FIELDS = (
        "order_custom_field_name",
        "order_custom_field_type",
        "order_custom_field_label",
        "order_custom_field_type_info",
    )
    #: Body fields the spec requires to update an ``orders-platform`` custom user field.
    CUSTOM_USER_FIELD_UPDATE_FIELDS = (
        "order_custom_field_type",
        "order_custom_field_label",
        "order_custom_field_type_info",
    )
    #: Body fields the spec requires to create an ``orders/custom-fields`` field.
    ORDER_CUSTOM_FIELD_CREATE_FIELDS = (
        "order_custom_field_name",
        "order_custom_field_label",
        "order_custom_field_type",
    )

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    def _require(self, values, names):
        """Raise when a required field is missing.

        :param values: the fields given.
        :param names: the names that must be present.
        :raise ParamValueException: naming every missing field.
        """
        missing = self._missing(values, names)
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")

    # ---------------------------------------------------------- orders

    def archive_orders(self, **kwargs):
        """List archived orders, a page at a time.

        Sends ``POST /modules/api/v5.0/orders/archive`` with the keywords as
        the JSON body.

        :param kwargs: the body: ``cursor``, the ``next_page_cursor`` of the
            previous page; ``per_page``; and ``filters``, a dict.
        :return: the decoded JSON reply, with the orders under ``items`` and
            the cursor of the next page under ``next_page_cursor``, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ORDERS_ARCHIVE_V5, "post", {}, body=dict(kwargs))

    def get_order_history(self, **kwargs):
        """Get the history of an order.

        Sends ``GET /modules/api/v5.0/orders/history`` with the keywords as
        the query.

        :param kwargs: query parameters naming the order: ``order_id``,
            ``order_uuid`` or ``tracking_number``.
        :return: the decoded JSON reply, with the events under ``results``,
            or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ORDERS_HISTORY_V5, "get", dict(kwargs))

    def search_orders(self, **kwargs):
        """Search the orders of the orders platform, or filter them.

        Sends ``POST /modules/api/v5.0/orders-platform`` with the keywords as
        the JSON body. It mirrors C# ``OrderManagerV5.SearchOrders``.

        :param kwargs: the body, all optional: ``order_ids`` or
            ``order_uuids``, lists of orders to return; ``filters``, a dict
            such as ``{"created_timestamp": [start, end]}`` or
            ``{"statuses": [1]}``; ``search``, text to search for; ``fields``,
            the fields to return; ``order_by``, a list of
            ``[field, direction]`` pairs; ``limit`` and ``offset``;
            ``addition``; and ``return_provided_fields_as_map``.
        :return: the decoded JSON reply: the matching orders, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ORDERS_PLATFORM_V5, "post", {}, body=dict(kwargs))

    def batch_create_orders(self, data):
        """Create several orders in one request.

        Sends ``POST /modules/api/v5.0/orders-platform/batch-create`` with
        ``{"data": data}`` as the JSON body. It mirrors C#
        ``OrderManagerV5.BatchCreateOrders``.

        :param data: the orders, a list of order dicts, each with at least
            ``address_1`` and, to skip geocoding, ``cached_lat`` and
            ``cached_lng``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``data`` is ``None`` or empty.

        .. versionadded:: 1.0.0
        """
        if not data:
            raise ParamValueException("data", "Missing required params")
        return self._call_api(ORDERS_PLATFORM_BATCH_CREATE_V5, "post", {}, body={"data": list(data)})

    def batch_delete(self, **kwargs):
        """Delete several orders.

        Sends ``POST /modules/api/v5.0/orders-platform/batch-delete`` with the
        keywords as the JSON body.

        :param kwargs: the body: ``order_ids``, a list of order UUIDs.
        :return: the decoded JSON reply, e.g. ``{"status": true}``, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ORDERS_PLATFORM_BATCH_DELETE_V5, "post", {}, body=dict(kwargs))

    def batch_update(self, **kwargs):
        """Update several orders with the same values.

        Sends ``POST /modules/api/v5.0/orders-platform/batch-update`` with the
        keywords as the JSON body.

        :param kwargs: the body: ``order_ids``, a list of order UUIDs, and
            ``data``, a dict of the order fields to set.
        :return: the decoded JSON reply: the list of updated orders, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ORDERS_PLATFORM_BATCH_UPDATE_V5, "post", {}, body=dict(kwargs))

    def batch_update_filter(self, **kwargs):
        """Update every order that matches a filter, in the background.

        Sends ``PUT /modules/api/v5.0/orders-platform/batch-update/filter``
        with the keywords as the JSON body.

        :param kwargs: the body: ``data``, a dict of the order fields to set,
            and ``filters`` and ``search``, dicts selecting the orders.
        :return: the decoded JSON reply, e.g. ``{"status": true, "async":
            true}``, or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ORDERS_PLATFORM_BATCH_UPDATE_FILTER_V5, "put", {}, body=dict(kwargs))

    # ------------------------------- orders-platform/order-custom-user-fields

    @staticmethod
    def _custom_user_field_url(order_custom_field_uuid):
        """Build the URL of one ``orders-platform`` custom user field.

        :param order_custom_field_uuid: UUID of the field.
        :return: the absolute URL.
        :raise ParamValueException: when ``order_custom_field_uuid`` is empty.
        """
        uuid = path_segment(order_custom_field_uuid, "order_custom_field_uuid")
        return f"{ORDERS_PLATFORM_CUSTOM_USER_FIELDS_V5}/{uuid}"

    def get_custom_user_fields(self):
        """List the order custom user fields of the account.

        Sends ``GET /modules/api/v5.0/orders-platform/order-custom-user-fields``.

        :return: the decoded JSON reply, with the fields under ``data``, or
            the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ORDERS_PLATFORM_CUSTOM_USER_FIELDS_V5, "get", {})

    def create_custom_user_fields(self, **kwargs):
        """Create an order custom user field.

        Sends ``POST /modules/api/v5.0/orders-platform/order-custom-user-fields``
        with the keywords as the JSON body.

        :param kwargs: the field. Required: ``order_custom_field_name``,
            ``order_custom_field_type``, ``order_custom_field_label`` and
            ``order_custom_field_type_info`` (a dict).
        :return: the decoded JSON reply, with the new field under ``data``, or
            the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        self._require(kwargs, self.CUSTOM_USER_FIELD_CREATE_FIELDS)
        return self._call_api(ORDERS_PLATFORM_CUSTOM_USER_FIELDS_V5, "post", {}, body=dict(kwargs))

    def update_custom_user_fields(self, order_custom_field_uuid, **kwargs):
        """Update an order custom user field.

        Sends ``PUT /modules/api/v5.0/orders-platform/order-custom-user-fields/{order_custom_field_uuid}``
        with the keywords as the JSON body.

        :param order_custom_field_uuid: UUID of the field.
        :param kwargs: the new values. Required: ``order_custom_field_type``,
            ``order_custom_field_label`` and ``order_custom_field_type_info``.
        :return: the decoded JSON reply, with the field under ``data``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``order_custom_field_uuid`` is empty
            or a required field is missing.

        .. versionadded:: 1.0.0
        """
        url = self._custom_user_field_url(order_custom_field_uuid)
        self._require(kwargs, self.CUSTOM_USER_FIELD_UPDATE_FIELDS)
        return self._call_api(url, "put", {}, body=dict(kwargs))

    def delete_custom_user_fields(self, order_custom_field_uuid):
        """Delete an order custom user field.

        Sends ``DELETE /modules/api/v5.0/orders-platform/order-custom-user-fields/{order_custom_field_uuid}``.

        :param order_custom_field_uuid: UUID of the field.
        :return: the decoded JSON reply, with the deleted field under
            ``data``, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``order_custom_field_uuid`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._custom_user_field_url(order_custom_field_uuid), "delete", {})

    # ------------------------------------------------- orders/custom-fields

    @staticmethod
    def _order_custom_field_url(order_custom_field_id):
        """Build the URL of one ``orders/custom-fields`` field.

        :param order_custom_field_id: integer ID of the field.
        :return: the absolute URL.
        :raise ParamValueException: when ``order_custom_field_id`` is not a
            non-negative integer.
        """
        return f"{ORDERS_CUSTOM_FIELDS_V5}/{path_int(order_custom_field_id, 'order_custom_field_id')}"

    def get_order_custom_fields(self):
        """List the order custom fields of the account.

        Sends ``GET /modules/api/v5.0/orders/custom-fields``.

        :return: the decoded JSON reply, ``{"status": true, "code": 200,
            "data": [...]}``, or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ORDERS_CUSTOM_FIELDS_V5, "get", {})

    def create_order_custom_field(self, **kwargs):
        """Create an order custom field.

        Sends ``POST /modules/api/v5.0/orders/custom-fields`` with the
        keywords as the JSON body.

        :param kwargs: the field. Required: ``order_custom_field_name``,
            ``order_custom_field_label`` and ``order_custom_field_type``;
            optional: ``order_custom_field_type_info`` (a dict).
        :return: the decoded JSON reply, with the new field under ``data``, or
            the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        self._require(kwargs, self.ORDER_CUSTOM_FIELD_CREATE_FIELDS)
        return self._call_api(ORDERS_CUSTOM_FIELDS_V5, "post", {}, body=dict(kwargs))

    def update_order_custom_field(self, order_custom_field_id, **kwargs):
        """Update an order custom field.

        Sends ``PUT /modules/api/v5.0/orders/custom-fields/{order_custom_field_id}``
        with the keywords as the JSON body.

        :param order_custom_field_id: integer ID of the field.
        :param kwargs: the values to change: ``order_custom_field_label``,
            ``order_custom_field_type`` or ``order_custom_field_type_info``.
        :return: the decoded JSON reply, with the field under ``data``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``order_custom_field_id`` is not a
            non-negative integer.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._order_custom_field_url(order_custom_field_id), "put", {}, body=dict(kwargs))

    def delete_order_custom_field(self, order_custom_field_id):
        """Delete an order custom field.

        Sends ``DELETE /modules/api/v5.0/orders/custom-fields/{order_custom_field_id}``.

        :param order_custom_field_id: integer ID of the field.
        :return: the decoded JSON reply, e.g. ``{"status": true, "code":
            200}``, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``order_custom_field_id`` is not a
            non-negative integer.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._order_custom_field_url(order_custom_field_id), "delete", {})
