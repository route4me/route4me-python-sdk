from .base import Base
from .utils import json2obj
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
        if self.check_required_params(kwargs, ['limit', 'Offset', ]):
            self.response = self.api._request_get(self.api._build_base_url(),
                                                  kwargs)
            response = json2obj(self.response.content)
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
            self.response = self.api._request_get(self.api._build_base_url(),
                                                  kwargs)
            response = json2obj(self.response.content)
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
        if self.check_required_params(kwargs, ['optimization_problem_id', 'addresses', 'reoptimize']):
            self.response = self.api._request_put(self.api._build_base_url(),
                                                  kwargs)
            response = json2obj(self.response.content)
            return response
        else:
            raise ParamValueException('params', 'Params are not complete')
