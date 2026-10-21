"""The :class:`Order` resource: create, read, update and delete orders."""

from .api_endpoints import ORDERS_HOST
from .base import Base
from .exceptions import ParamValueException


class Order(Base):
    """Orders: transactional events, such as a delivery to make.

    Use it as ``route4me.order``. Every method sends a request to
    ``/api.v4/order.php``.

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
