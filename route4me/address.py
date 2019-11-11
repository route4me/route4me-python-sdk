# -*- coding: utf-8 -*-
# codebeat:disable[ABC]

import json
import random
import time
import requests

from .api_endpoints import (
    ADD_ROUTE_NOTES_HOST,
    BATCH_GEOCODER,
    ADDRESS_HOST,
    SINGLE_GEOCODER,
)
from .base import Base
from .exceptions import ParamValueException


class Address(Base):
    """
    An Address is a destination in a route or optimization problem.
    Addresses can be depots, which means they are a departure points.
    Addresses can belong to only one route and one optimization problem,
    except for depots. One depot can be part of many routes if we have a
    VRP (multi-route) solution.
    """
    REQUIRED_FIELDS = ['address', 'lat', 'lng', ]

    def __init__(self, api, addresses=[]):
        """
        Address Instance
        :param api:
        :param addresses:
        :return:
        """
        self.addresses = addresses
        Base.__init__(self, api)

    def get_route_id(self):
        """
        Return Route ID
        :return:
        """
        return self.get_response()['route_id']

    def get_route_destination_id(self):
        """
        Return Destination ID
        :return:
        """
        return self.get_response()['route_destination_id']

    def get_addresses(self):
        """
        Return Addresses
        :return:
        """
        return self.addresses

    def add_address(self, **kwargs):
        """
        Add addresses to optimization
        :param kwargs:
        :return:
        """
        if self.check_required_params(kwargs, self.REQUIRED_FIELDS):
            self.addresses.append(kwargs)
            self.api.optimization.data['addresses'] = self.addresses
        else:
            raise ParamValueException('addresses', 'Params are not complete')

    def batch_fix_geocodes(self, addresses):
        geocoding_error = []
        params = {
            'format': 'json',
        }
        addresses_map = {x['address'].replace('/', ' - '): x for x in addresses}
        data = {'addresses': '||'.join([x['address'] for x in addresses])}
        try:
            json_data = self.get_batch_geocodes(params, data)
        except json.decoder.JSONDecodeError:
            print('Error Geocoding some of the Addresses. Please check the addresses and try again.')
            return addresses, []
        geocoded_addresses = []
        for address in json_data:
            try:
                original_address = addresses_map[address['original']]
                original_address.update({
                    'lat': address['lat'],
                    'lng': address['lng'],
                })
                geocoded_addresses.append(original_address)
            except (IndexError, ValueError):
                geocoding_error.append(address)
        return geocoding_error, addresses

    def get_geocode(self, params):
        """
        Get Geocodes from given address
        :param params:
        :return: response as a object
        """
        self.response = self.api._make_request(SINGLE_GEOCODER,
                                               params,
                                               [],
                                               self.api._request_get)
        return self.response.json()

    def get_batch_geocodes(self, params, data):
        """
        Get Geocodes from given addresses
        :param params:
        :param data:
        :return: response as a object
        """
        self.response = self.api._make_request(BATCH_GEOCODER,
                                               params,
                                               data,
                                               self.api._request_post)
        return self.response.json()

    def fix_geocode(self, address):
        geocoding_error = None
        params = {'format': 'json', 'address': address.get('address')}
        count = 0
        while True:
            try:
                json_data = self.get_geocode(params)
                address.update(json_data)
                return geocoding_error, address
            except (AttributeError, requests.exceptions.ConnectionError):
                count += 1
                if count > 5:
                    geocoding_error = address
                    break
                time.sleep(random.randrange(1, 5) * 0.5)

        return geocoding_error, address

    def request_address(self, params):
        params.update({'api_key': self.api.key})
        return self.api._make_request(ADDRESS_HOST,
                                      params,
                                      None,
                                      self.api._request_get)

    def get_address(self, route_id, route_destination_id):
        params = {'route_id': route_id,
                  'route_destination_id': route_destination_id
                  }
        response = self.request_address(params)
        return response.json()

    def get_address_notes(self, route_id, route_destination_id):
        params = {'route_id': route_id,
                  'route_destination_id': route_destination_id,
                  'notes': True,
                  }
        response = self.request_address(params)
        return response.json()

    def update_address(self, data, route_id, route_destination_id):
        params = {'route_id': route_id,
                  'route_destination_id': route_destination_id
                  }
        params.update({'api_key': self.api.key})
        data = json.dumps(data)
        response = self.api._make_request(ADDRESS_HOST,
                                          params,
                                          data,
                                          self.api._request_put)
        return response.json()

    def delete_address_from_route(self, route_id, route_destination_id):
        params = {'route_id': route_id,
                  'route_destination_id': route_destination_id
                  }
        params.update({'api_key': self.api.key})
        response = self.api._make_request(ADDRESS_HOST,
                                          params,
                                          None,
                                          self.api._request_delete)
        return response.json()

    def add_address_notes(self, note, **kwargs):
        """
        Add Address  Note using POST request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        if self.check_required_params(kwargs, ['address_id', 'route_id']):
            data = {'strUpdateType': kwargs.pop('activity_type'),
                    'strNoteContents': note}
            kwargs.update({'api_key': self.params['api_key'], })
            self.response = self.api._request_post(ADD_ROUTE_NOTES_HOST,
                                                   kwargs, data)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def geocode(self, **kwargs):
        """
        Bulk Geocoder using POST request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        if 'format' not in kwargs:
            kwargs.update({'format': 'csv'})
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['addresses', ]):
            response = self.api._request_post(BATCH_GEOCODER,
                                              kwargs)
            return response.content

        else:
            raise ParamValueException('params', 'Params are not complete')

# codebeat:enable[ABC]
