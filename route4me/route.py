from base import Base
from exceptions import ParamValueException
from utils import json2obj
from api_endpoints import ROUTE_HOST


class Route(Base):
    """
    A Route is a multi-sequence of addresses that need to be
    visited by a single vehicle and a single driver in a fixed time period.
    """
    requirements = [
            'api_key',
            'route_id',
    ]

    def __init__(self, api):
        """
        Routes
        :param api: route4me instance
        :return: route instance
        """
        self.response = None
        self.params = {'api_key': api.key, }
        Base.__init__(self, api)

    def get_route(self, **kwargs):
        """
        Get route using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        if self.validate_params(**kwargs):
            self.params.update(kwargs)
        if self.check_required_params(self.params, self.requirements):
            self.response = self.api._request_get(self._build_route_url(),
                                                  self.params)
            response = json2obj(self.response.content)
            return response

        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_routes(self, **kwargs):
        """
        Get routes using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.

        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['limit', 'Offset', ]):
            self.response = self.api._request_get(self._build_route_url(),
                                                  kwargs)
            response = json2obj(self.response.content)
            return response
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_activities(self, **kwargs):
        """
        Get routes activities using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.

        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['route_id', 'limit', 'Offset', ]):
            self.response = self.api._request_get(self.api.get_activities_host_url(),
                                                  kwargs)
            response = json2obj(self.response.content)
            return response
        else:
            raise ParamValueException('params', 'Params are not complete')

    def duplicate_route(self, **kwargs):
        """
        Duplicate route using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['route_id', ]):
            self.response = self.api._request_get(self._build_route_url(),
                                                  kwargs)
            response = json2obj(self.response.content)
            return response
        else:
            raise ParamValueException('params', 'Params are not complete')

    def delete_routes(self, **kwargs):
        """
        Delete routes using DELETE request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['route_id', ]):
            kwargs['route_id'] = ','.join(kwargs['route_id'])
            self.response = self.api._request_delete(self._build_route_url(),
                                                     kwargs)
            response = json2obj(self.response.content)
            return response
        else:
            raise ParamValueException('params', 'Params are not complete')

    def delete_route(self):
        """
        Delete given route
        :return: API response
        :raises: ParamValueException if required params are not present.
        AttributeError if there is an error deleting a route
        """
        if self.required_params(['route_id']):
            self.response = self.api._request_delete(self._build_route_url(), self.params)
            response = json2obj(self.response.content)
            try:
                response = response.deleted
                return response
            except AttributeError:
                return response.errors
        else:
            raise ParamValueException('params', 'Params are not complete')

    @staticmethod
    def _build_route_url():
        return ROUTE_HOST + '?'

    def insert_address_into_route(self, addresses, route_id):
        params = {'route_id': route_id}
        response = self.api.update_route(params, addresses)
        return json2obj(response.content)

    def move_addresses_from_route(self, addresses, route_id):
        params = {'route_id': route_id}
        response = self.api.update_route(params, addresses)
        return json2obj(response.content)

    def update_route_parameters(self, data, route_id):
        params = {'route_id': route_id}
        response = self.api.update_route(params, data)
        return json2obj(response.content)
