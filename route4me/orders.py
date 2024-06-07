# -*- coding: utf-8 -*-

import json

from .api_endpoints import ORDERS_HOST
from .base import Base
from .exceptions import ParamValueException, APIException


class Order(Base):
    """
    Orders are transactional events.
    """

    REQUIRED_FIELDS = ('address_1', )

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
            try:
                response = self.api._make_request(ORDERS_HOST,
                                                  self.params,
                                                  self.api._request_post,
                                                  json=kwargs)
                try:
                    return response.json()
                except ValueError:
                    return response.content
            except APIException as e:
                return e.to_dict()
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
            try:
                response = self.api._make_request(ORDERS_HOST,
                                                  kwargs,
                                                  self.api._request_get)
                try:
                    return json.loads(response.content)
                except ValueError:
                    return response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('order', 'Missing required params')

    def update_order(self, **kwargs):
        """
        Update an Order
        :param kwargs:
        :return: API response content
        """
        if self.check_required_params(kwargs, self.REQUIRED_FIELDS):
            try:
                response = self.api._make_request(ORDERS_HOST,
                                                  self.params,
                                                  self.api._request_put,
                                                  json=kwargs)
                try:
                    return json.loads(response.content)
                except ValueError:
                    return response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('order', 'Missing required params')

    def delete_order(self, **kwargs):
        """
        Delete an Order
        :param kwargs:
        :return: API response content
        """
        if self.check_required_params(kwargs, ['order_ids', ]):
            try:
                response = self.api._make_request(ORDERS_HOST,
                                                  self.params,
                                                  self.api._request_delete,
                                                  json=kwargs)
                try:
                    return json.loads(response.content)
                except ValueError:
                    return response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('order', 'Missing required params')
