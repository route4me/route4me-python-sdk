# -*- coding: utf-8 -*-

import json

from .api_endpoints import ADDRESS_HOST, API_HOST
from .base import Base
from .exceptions import ParamValueException


class Optimization(Base):
    """
        An Optimization Problem is a collection of addresses that need to be
        visited. This is distinct from a Route, which is a sequence of
        addresses that need to be visited by a single vehicle and a single
        driver in a fixed time period. Solving an Optimization Problem
        results in a number of routes.
    """

    def __init__(self, api):
        """
        Optimization Instance
        :param api:
        :return:
        """
        Base.__init__(self, api)

    def get_optimizations(self, **kwargs):
        """
        Get optimizations using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.

        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['limit', 'offset', ]):
            self.response = self.api._request_get(API_HOST,
                                                  kwargs)
            response = self.response.json()
            return response
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_optimization(self, **kwargs):
        """
        Get optimization using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.

        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['optimization_problem_id', ]):
            self.response = self.api._request_get(API_HOST,
                                                  kwargs)
            response = self.response.json()
            return response
        else:
            raise ParamValueException('params', 'Params are not complete')

    def update_optimization(self, **kwargs):
        """
        Update optimization using PUT request
        :return: API response
        :raise: ParamValueException if required params are not present.

        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['optimization_problem_id',
                                               'addresses',
                                               'reoptimize']):
            self.response = self.api._request_put(API_HOST,
                                                  kwargs)
            response = self.response.json()
            return response
        else:
            raise ParamValueException('params', 'Params are not complete')

    def delete_optimization(self, **kwargs):
        """
        Delete optimization using DELETE request
        :return: API response
        :raise: ParamValueException if required params are not present.

        """
        self.json_data = kwargs
        if self.check_required_params(kwargs, ['optimization_problem_ids', ]):
            data = json.dumps(self.json_data, ensure_ascii=False)
            self.response = self.api._request_delete(API_HOST,
                                                     self.params,
                                                     data=data)
            response = self.response.json()
            return response
        else:
            raise ParamValueException('params', 'Params are not complete')

    def delete_address_from_optimization(self, **kwargs):
        """
        Delete Address from an optimization using DELETE request
        :return: API response
        :raise: ParamValueException if required params are not present.

        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['optimization_problem_id',
                                               'route_destination_id']):
            self.response = self.api._request_delete(ADDRESS_HOST,
                                                     kwargs)
            response = self.response.json()
            return response
        else:
            raise ParamValueException('params', 'Params are not complete')
