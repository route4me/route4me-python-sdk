"""The :class:`Order` resource: orders and order custom user fields (API V4)."""

from .api_endpoints import ORDER_CUSTOM_USER_FIELDS, ORDERS_HOST, ORDERS_UPDATES
from .base import Base
from .exceptions import ParamValueException


class Order(Base):
    """Orders: transactional events, such as a delivery to make.

    Use it as ``route4me.order``. The order methods send their requests to
    ``/api.v4/order.php``, :meth:`get_orders_updates` to
    ``/api.v4/orders/changes.php``, and the custom user field methods to
    ``/api.v4/order_custom_user_fields.php``. For API V5 see
    :class:`~route4me.orders_v5.OrdersV5`.

    Every method returns the decoded JSON reply, the raw body (``bytes``) when
    it is not JSON, or on an API error the ``{"errors": ...}`` dict from
    :meth:`APIException.to_dict <route4me.exceptions.APIException.to_dict>`
    instead of raising.
    """

    REQUIRED_FIELDS = ("address_1",)

    def __init__(self, api):
        Base.__init__(self, api)

    def create_order(self, **kwargs):
        """Create an order.

        Sends ``POST /api.v4/order.php`` with the keywords as the JSON body.

        :param kwargs: the order fields. Required: ``address_1``.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``address_1`` is missing.
        """
        if not self.check_required_params(kwargs, self.REQUIRED_FIELDS):
            raise ParamValueException("order", "Missing required params")
        return self._request_decoded(ORDERS_HOST, self.params, "post", json=kwargs)

    def get_orders(self, **kwargs):
        """List orders, a page at a time, optionally searched or filtered by date.

        Sends ``GET /api.v4/order.php`` with the keywords in the query. It
        mirrors C# ``Route4MeManager.GetOrders``; to get one order, use
        :meth:`get_order`.

        :param kwargs: query parameters, all optional: ``limit`` and
            ``offset``; ``query``, text to search for; ``fields``, the fields
            to return, comma-separated; ``display``; ``day_added_YYMMDD`` or
            ``scheduled_for_YYMMDD``, a date such as ``"2026-10-22"``.
        :return: the decoded JSON reply: ``results`` and ``total``, the raw
            body (``bytes``) when it is not JSON, or the ``{"errors": ...}``
            dict on an API error.

        .. versionadded:: 1.0.0
        """
        params = dict(kwargs, api_key=self.params["api_key"])
        return self._request_decoded(ORDERS_HOST, params, "get")

    def get_order(self, **kwargs):
        """Get an order by ID.

        Sends ``GET /api.v4/order.php``.

        :param kwargs: query parameters. Required: ``order_id``.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``order_id`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        if not self.check_required_params(kwargs, ["order_id", "api_key"]):
            raise ParamValueException("order", "Missing required params")
        return self._request_decoded(ORDERS_HOST, kwargs, "get")

    def update_order(self, **kwargs):
        """Update an order.

        Sends ``PUT /api.v4/order.php`` with the keywords as the JSON body.

        :param kwargs: the order fields, including the ``order_id`` of the
            order to update. Required: ``address_1``.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``address_1`` is missing.
        """
        if not self.check_required_params(kwargs, self.REQUIRED_FIELDS):
            raise ParamValueException("order", "Missing required params")
        return self._request_decoded(ORDERS_HOST, self.params, "put", json=kwargs)

    def delete_order(self, **kwargs):
        """Delete orders.

        Sends ``DELETE /api.v4/order.php`` with the keywords as the JSON body.

        :param kwargs: required: ``order_ids``, a list of order IDs.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``order_ids`` is missing.
        """
        if not self.check_required_params(kwargs, ["order_ids"]):
            raise ParamValueException("order", "Missing required params")
        return self._request_decoded(ORDERS_HOST, self.params, "delete", json=kwargs)

    def filter_orders(self, body, **kwargs):
        """Search orders with a filter.

        Sends ``POST /api.v4/order.php`` with ``body`` as the JSON body and
        the keywords as the query. The same endpoint creates an order
        (:meth:`create_order`); a body with ``filter`` makes it a search.

        :param body: the JSON body, e.g. ``{"filter": {"display": "all",
            "statuses": [1]}}``. ``filter`` takes ``query``, ``display``,
            ``scheduled_for_YYMMDD``, ``tracking_numbers``,
            ``created_timestamp_start``, ``created_timestamp_end``, ``terms``
            and ``statuses``.
        :param kwargs: query parameters: ``limit`` and ``offset``.
        :return: the decoded JSON reply, with the orders under ``results``,
            the raw body (``bytes``) when it is not JSON, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._request_decoded(ORDERS_HOST, dict(kwargs), "post", json=body)

    def get_orders_updates(self, **kwargs):
        """Get the orders changed since a point in time.

        Sends ``GET /api.v4/orders/changes.php`` with the keywords as the
        query.

        :param kwargs: query parameters: ``last_known_ts``, the Unix timestamp
            of the last update already known.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._request_decoded(ORDERS_UPDATES, dict(kwargs), "get")

    def get_order_custom_user_fields(self):
        """List the order custom user fields of the account.

        Sends ``GET /api.v4/order_custom_user_fields.php``.

        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._request_decoded(ORDER_CUSTOM_USER_FIELDS, {}, "get")

    def create_order_custom_user_field(self, **kwargs):
        """Create an order custom user field.

        Sends ``POST /api.v4/order_custom_user_fields.php`` with the keywords
        as the JSON body.

        :param kwargs: the field: ``order_custom_field_name``,
            ``order_custom_field_label``, ``order_custom_field_type``,
            ``order_custom_field_value`` and ``order_custom_field_type_info``
            (a dict).
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._request_decoded(ORDER_CUSTOM_USER_FIELDS, {}, "post", json=dict(kwargs))

    def update_order_custom_user_field(self, **kwargs):
        """Update an order custom user field.

        Sends ``PUT /api.v4/order_custom_user_fields.php`` with the keywords
        as the JSON body.

        :param kwargs: ``order_custom_field_id``, the field to update, and the
            values to change: ``order_custom_field_name``,
            ``order_custom_field_label``, ``order_custom_field_type``,
            ``order_custom_field_value``, ``order_custom_field_type_info`` or
            ``root_owner_member_id``.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._request_decoded(ORDER_CUSTOM_USER_FIELDS, {}, "put", json=dict(kwargs))

    def remove_order_custom_user_field(self, order_custom_field_id):
        """Delete an order custom user field.

        Sends ``DELETE /api.v4/order_custom_user_fields.php`` with
        ``{"order_custom_field_id": ...}`` as the JSON body.

        :param order_custom_field_id: ID of the field.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        body = {"order_custom_field_id": order_custom_field_id}
        return self._request_decoded(ORDER_CUSTOM_USER_FIELDS, {}, "delete", json=body)
