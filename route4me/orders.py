from .api_endpoints import ORDERS_HOST
from .base import Base
from .exceptions import ParamValueException


class Order(Base):
    """
    Orders are transactional events.
    """

    REQUIRED_FIELDS = ("address_1",)

    def __init__(self, api):
        Base.__init__(self, api)

    def create_order(self, **kwargs):
        if not self.check_required_params(kwargs, self.REQUIRED_FIELDS):
            raise ParamValueException("order", "Missing required params")
        return self._request_decoded(ORDERS_HOST, self.params, "post", json=kwargs)

    def get_order(self, **kwargs):
        """
        Get an Order
        :param kwargs:
        :return: API response content
        """
        kwargs.update({"api_key": self.params["api_key"]})
        if not self.check_required_params(kwargs, ["order_id", "api_key"]):
            raise ParamValueException("order", "Missing required params")
        return self._request_decoded(ORDERS_HOST, kwargs, "get")

    def update_order(self, **kwargs):
        """
        Update an Order
        :param kwargs:
        :return: API response content
        """
        if not self.check_required_params(kwargs, self.REQUIRED_FIELDS):
            raise ParamValueException("order", "Missing required params")
        return self._request_decoded(ORDERS_HOST, self.params, "put", json=kwargs)

    def delete_order(self, **kwargs):
        """
        Delete an Order
        :param kwargs:
        :return: API response content
        """
        if not self.check_required_params(kwargs, ["order_ids"]):
            raise ParamValueException("order", "Missing required params")
        return self._request_decoded(ORDERS_HOST, self.params, "delete", json=kwargs)
