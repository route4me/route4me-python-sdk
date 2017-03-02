import json
from route4me.base import Base
from route4me.exceptions import ParamValueException
from route4me.api_endpoints import ORDERS_HOST

class Order(Base):
    """
    Orders are transactional events.
    """

    REQUIRED_FIELDS = ('address_1', 'cached_lat', 'cached_lng', )

    def __init__(self, api):
        """
        Order Instance
        :param api:
        :return:
        """
        Base.__init__(self, api)

    def create_order(self, **kwargs):
        """
        Create an Order
        :param kwargs:
        :return: API response content
        """
        if self.check_required_params(kwargs, self.REQUIRED_FIELDS):
            response = self.api._request_post(ORDERS_HOST,
                                              self.params,
                                              data=json.dumps(kwargs, ensure_ascii=False))
            try:
                return json.loads(response.content)
            except ValueError:
                return response.content
        else:
            raise ParamValueException('order', 'Missing required params')

    def get_order(self, **kwargs):
        """
        Get an Order
        :param kwargs:
        :return: API response content
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['order_id', 'api_key', ]):
            response = self.api._request_get(ORDERS_HOST,
                                             kwargs)
            try:
                return json.loads(response.content)
            except ValueError:
                return response.content
        else:
            raise ParamValueException('order', 'Missing required params')

    def update_order(self, **kwargs):
        """
        Update an Order
        :param kwargs:
        :return: API response content
        """
        if self.check_required_params(kwargs, self.REQUIRED_FIELDS):
            response = self.api._request_put(ORDERS_HOST,
                                             self.params, data=json.dumps(kwargs))
            try:
                return json.loads(response.content)
            except ValueError:
                return response.content
        else:
            raise ParamValueException('order', 'Missing required params')

    def delete_order(self, **kwargs):
        """
        Delete an Order
        :param kwargs:
        :return: API response content
        """
        if self.check_required_params(kwargs, ['order_ids', ]):
            response = self.api._request_delete(ORDERS_HOST,
                                                self.params, data=json.dumps(kwargs))
            try:
                return json.loads(response.content)
            except ValueError:
                return response.content
        else:
            raise ParamValueException('order', 'Missing required params')

