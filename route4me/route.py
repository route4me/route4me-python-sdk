# -*- coding: utf-8 -*-

# codebeat:disable[TOO_MANY_FUNCTIONS]


from .api_endpoints import ROUTE_HOST, EXPORTER
from .api_endpoints import ADDRESS_HOST, GET_ACTIVITIES_HOST, DUPLICATE_ROUTE, SHARE_ROUTE_HOST
from .api_endpoints import MERGE_ROUTES_HOST, RESEQUENCE_ROUTE
from .api_endpoints import EXPORTER_V5
from .base import Base
from .exceptions import ParamValueException


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
            self.response = self.api._request_get(ROUTE_HOST,
                                                  self.params)
            return self.response.json()

        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_route_tracking(self, **kwargs):
        """
        Get route using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        if self.validate_params(**kwargs):
            self.params.update(kwargs)
        self.params.update({'device_tracking_history': 1})
        if self.check_required_params(self.params, self.requirements):
            self.response = self.api._request_get(ROUTE_HOST,
                                                  self.params)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_routes(self, **kwargs):
        """
        Get routes using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.

        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['limit', 'offset', ]):
            self.response = self.api._request_get(ROUTE_HOST,
                                                  kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_activities(self, **kwargs):
        """
        Get routes activities using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.

        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['route_id',
                                               'limit',
                                               'offset', ]):
            self.response = self.api._request_get(GET_ACTIVITIES_HOST,
                                                  kwargs)
            return self.response.json()
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
            self.response = self.api._request_get(DUPLICATE_ROUTE,
                                                  kwargs)
            print(self.response.content)
            return self.response.json()
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
            self.response = self.api._request_delete(ROUTE_HOST,
                                                     kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def delete_route(self, **kwargs):
        """
        Delete given route
        :return: API response
        :raises: ParamValueException if required params are not present.
        AttributeError if there is an error deleting a route
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['route_id', ]):
            self.response = self.api._request_delete(ROUTE_HOST, kwargs)
            response = self.response.json()
            try:
                response = response.get('deleted')
                return response
            except AttributeError:
                return response.errors
        else:
            raise ParamValueException('params', 'Params are not complete')

    def insert_address_into_route(self, addresses, route_id):
        params = {'route_id': route_id}
        response = self._update_route(params, addresses)
        return response.json()

    def move_addresses_from_route(self, addresses, route_id):
        params = {'route_id': route_id}
        response = self._update_route(params, addresses)
        return response.json()

    def update_route_parameters(self, data, route_id):
        params = {'route_id': route_id}
        response = self._update_route(params, data)
        return response.json()

    def update_route(self, data, route_id):
        params = {'route_id': route_id}
        response = self._update_route(params, data)
        return response.json()

    def insert_address_into_route_optimal_position(self, **kwargs):
        """
        Insert an address into a route in an optimal position using PUT
        :return: API response
        :raises: ParamValueException if required params are not present.
        AttributeError if there is an error deleting a route
        """
        if self.check_required_params(kwargs, ['addresses',
                                               'route_id',
                                               'optimal_position']):
            params = {'api_key': self.params['api_key'],
                      'route_id': kwargs.pop('route_id')}
            response = self.api._request_put(ROUTE_HOST,
                                             params,
                                             json=kwargs)
            return response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_route_path_points(self, **kwargs):
        """
        Get path point from a route using GET
        :return: API response
        :raises: ParamValueException if required params are not present.
        AttributeError if there is an error deleting a route
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['route_path_output',
                                               'route_id', ]):
            response = self.api._request_get(ROUTE_HOST,
                                             kwargs)
            return response.json()

        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_route_directions(self, **kwargs):
        """
        Get route directions using GET
        :return: API response
        :raises: ParamValueException if required params are not present.
        AttributeError if there is an error deleting a route
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['directions', 'route_id', ]):
            response = self.api._request_get(ROUTE_HOST,
                                             kwargs)
            return response.json()

        else:
            raise ParamValueException('params', 'Params are not complete')

    def share_route(self, **kwargs):
        """
        Share a route using POST
        :return: API response
        :raises: ParamValueException if required params are not present.
        AttributeError if there is an error deleting a route
        """
        if self.check_required_params(kwargs, ['recipient_email',
                                               'route_id',
                                               'response_format']):
            params = {'api_key': self.params['api_key'],
                      'route_id': kwargs.pop('route_id'),
                      'response_format': kwargs.pop('response_format')}
            response = self.api._request_post(SHARE_ROUTE_HOST,
                                              params,
                                              json=kwargs)
            return response.json()

        else:
            raise ParamValueException('params', 'Params are not complete')

    def resequence_route(self, **kwargs):
        """
        Resequence a route using PUT
        :return: API response
        :raises: ParamValueException if required params are not present.
        AttributeError if there is an error deleting a route
        """
        if self.check_required_params(kwargs, ['addresses',
                                               'route_id',
                                               'route_destination_id']):
            params = {
                'api_key': self.params['api_key'],
                'route_id': kwargs.pop('route_id'),
                'route_destination_id': kwargs.pop('route_destination_id'),
            }
            response = self.api._request_put(ROUTE_HOST,
                                             params, json=kwargs)
            return response.json()

        else:
            raise ParamValueException('params', 'Params are not complete')

    def resequence_multiple_stops(self, route_id, addresses_data):
        """
        Resequence multiple stops using PUT
        :return: API response
        :raises: ParamValueException if required params are not present.
        AttributeError if there is an error deleting a route
        """
        if self.check_required_params(addresses_data, ['addresses']):
            params = {
                'api_key': self.params['api_key'],
                'route_id': route_id,
            }
            response = self.api._request_put(ROUTE_HOST,
                                             params, json=addresses_data)
            return response.json()

        else:
            raise ParamValueException('params', 'Params are not complete')

    def merge_routes(self, **kwargs):
        """
        Merge routes using POST
        :return: API response
        :raises: ParamValueException if required params are not present.
        AttributeError if there is an error deleting a route
        """
        if self.check_required_params(kwargs, ['route_ids']):
            response = self.api._request_post(MERGE_ROUTES_HOST,
                                              self.params,
                                              json=kwargs)
            return response.json()

        else:
            raise ParamValueException('params', 'Params are not complete')

    def resequence_route_all(self, **kwargs):
        """
        Resequence Route using GET
        :return: API response
        :raises: ParamValueException if required params are not present.
        AttributeError if there is an error deleting a route
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['disable_optimization',
                                               'route_id',
                                               'optimize', ]):
            response = self.api._request_get(RESEQUENCE_ROUTE,
                                             kwargs)
            return response.json()

        else:
            raise ParamValueException('params', 'Params are not complete')

    def update_route_destination_custom_data(self, **kwargs):
        """
        Update route destination custom data using PUT
        :return: API response
        :raises: ParamValueException if required params are not present.
        AttributeError if there is an error deleting a route
        """
        if self.check_required_params(kwargs, ['route_id',
                                               'route_destination_id']):
            params = {
                'api_key': self.params['api_key'],
                'route_id': kwargs.pop('route_id'),
                'route_destination_id': kwargs.pop('route_destination_id'),
            }
            response = self.api._request_put(ADDRESS_HOST,
                                             params, json=kwargs)
            return response.json()

        else:
            raise ParamValueException('params', 'Params are not complete')

    def export_route(self, route_id, output_format='csv'):
        """
        Get Route from given post data
        :param route_id:
        :param output_format:
        :return: response as a object
        """
        print("DEPRECATED. Please use export_route_v5")
        data = {'route_id': route_id, 'strExportFormat': output_format}
        self.response = self.api._make_request(EXPORTER, {}, data,
                                               self.api._request_post)
        return self.response.content

    def _update_route(self, params, data):
        params.update({'api_key': self.api.key})
        return self.api._request_put(ROUTE_HOST, request_params=params, json=data)

    def export_route_v5(self, route_id, output_format='csv', all_custom_fields=True, columns=None):
        """
        Get Route from given post data
        :param route_id:
        :param output_format:
        :return: response as a object
        """
        params = {
            'api_key': self.params['api_key'],
        }
        data = {'all_custom_fields': all_custom_fields, 'format': output_format}
        if columns is not None:
            data["columns"] = columns
        self.response = self.api._make_request(EXPORTER_V5.format(route_id=route_id), params, data,
                                               self.api._request_post)
        return self.response.content

# codebeat:enable[TOO_MANY_FUNCTIONS]
