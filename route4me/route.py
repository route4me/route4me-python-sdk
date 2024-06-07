# -*- coding: utf-8 -*-

# codebeat:disable[TOO_MANY_FUNCTIONS]


from .api_endpoints import ROUTE_HOST, EXPORTER
from .api_endpoints import ADDRESS_HOST, GET_ACTIVITIES_HOST, DUPLICATE_ROUTE, SHARE_ROUTE_HOST
from .api_endpoints import MERGE_ROUTES_HOST, RESEQUENCE_ROUTE
from .api_endpoints import EXPORTER_V5
from .base import Base
from .exceptions import ParamValueException, APIException


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
            try:
                self.response = self.api._make_request(ROUTE_HOST,
                                                       self.params,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ROUTE_HOST,
                                                       self.params,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ROUTE_HOST,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(GET_ACTIVITIES_HOST,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(DUPLICATE_ROUTE,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ROUTE_HOST,
                                                       kwargs,
                                                       self.api._request_delete)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ROUTE_HOST,
                                                       kwargs,
                                                       self.api._request_delete)
                response = self.response.json()
                try:
                    response = response.get('deleted')
                    return response
                except AttributeError:
                    return response.errors
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def insert_address_into_route(self, addresses, route_id):
        params = {'route_id': route_id}
        return self._update_route(params, addresses)

    def move_addresses_from_route(self, addresses, route_id):
        params = {'route_id': route_id}
        return self._update_route(params, addresses)

    def update_route_parameters(self, data, route_id):
        params = {'route_id': route_id}
        return self._update_route(params, data)

    def update_route(self, data, route_id):
        params = {'route_id': route_id}
        return self._update_route(params, data)

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
            try:
                self.response = self.api._make_request(ROUTE_HOST,
                                                       params,
                                                       self.api._request_put,
                                                       json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ROUTE_HOST,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ROUTE_HOST,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(SHARE_ROUTE_HOST,
                                                       params,
                                                       self.api._request_post,
                                                       json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ROUTE_HOST,
                                                       params,
                                                       self.api._request_put,
                                                       json=kwargs,)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ROUTE_HOST,
                                                       params,
                                                       self.api._request_put,
                                                       json=addresses_data)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(MERGE_ROUTES_HOST,
                                                       self.params,
                                                       self.api._request_post,
                                                       data=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(RESEQUENCE_ROUTE,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ADDRESS_HOST,
                                                       params,
                                                       self.api._request_put,
                                                       json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
        self.response = self.api._make_request(EXPORTER,
                                               {},
                                               self.api._request_post,
                                               data=data)
        return self.response.content

    def _update_route(self, params, data):
        params.update({'api_key': self.api.key})
        try:
            response = self.api._make_request(ROUTE_HOST,
                                              params,
                                              self.api._request_put,
                                              data=data)
            return response.json()
        except APIException as e:
            return e.to_dict()

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
        try:
            self.response = self.api._make_request(EXPORTER_V5.format(route_id=route_id),
                                                   params,
                                                   self.api._request_post,
                                                   data=data)
            return self.response.content
        except APIException as e:
            return e.to_dict()


# codebeat:enable[TOO_MANY_FUNCTIONS]
