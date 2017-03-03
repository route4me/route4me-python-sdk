# codebeat:disable[ABC]
import json
import random
import time

import requests
import xmltodict

from route4me.api_endpoints import (
    ADD_ROUTE_NOTES_HOST,
    BATCH_GEOCODER,
    ADDRESS_HOST,
    SINGLE_GEOCODER,
)
from route4me.base import Base
from route4me.exceptions import ParamValueException
from route4me.utils import json2obj


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
        param_address = 'addresses='
        for a in addresses:
            param_address = '{0}{1}||'.format(param_address, a.get('address'))
        params = {'format': 'xml', 'addresses': param_address}
        content = self.get_batch_geocodes(params)
        obj = xmltodict.parse(content)
        geocoded_addresses = []
        for i, d in enumerate(obj.get('destinations').get('destination')):
            try:
                address = dict([('lat', float(d.get('@lat'))),
                                ('lng', float(d.get('@lng'))),
                                ('time', addresses[i].get('time')),
                                ('alias', addresses[i].get('alias')),
                                ('address', d.get('@destination'))])
                if addresses[i].get('is_depot') == 1:
                    address.update(dict([('is_depot', 1)]))
                geocoded_addresses.append(address)
            except IndexError:
                geocoding_error.append(d)
        return geocoding_error, geocoded_addresses

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
        return self.response.content

    def get_batch_geocodes(self, params):
        """
        Get Geocodes from given addresses
        :param params:
        :return: response as a object
        """
        self.response = self.api._make_request(BATCH_GEOCODER,
                                               params,
                                               [],
                                               self.api._request_get)
        return self.response.content

    def fix_geocode(self, address):
        geocoding_error = None
        params = {'format': 'xml', 'address': address.get('address')}
        count = 0
        while True:
            try:
                content = self.get_geocode(params)
                obj = xmltodict.parse(content)
                obj = obj.get('result')
                address.update(dict([('lat', float(obj.get('@lat'))),
                                     ('lng', float(obj.get('@lng'))), ]))
                return geocoding_error, address
            except (AttributeError, requests.exceptions.ConnectionError):
                count += 1
                if count > 5:
                    geocoding_error = address
                    break
                time.sleep(random.randrange(1, 5) * 0.5)

        return geocoding_error, address

    def request_address(self, params):
        params.update({'api_key': self.key})
        return self._make_request(ADDRESS_HOST,
                                  params,
                                  None,
                                  self._request_get)

    def get_address(self, route_id, route_destination_id):
        params = {'route_id': route_id,
                  'route_destination_id': route_destination_id
                  }
        response = self.api.request_address(params)
        return json2obj(response.content)

    def get_address_notes(self, route_id, route_destination_id):
        params = {'route_id': route_id,
                  'route_destination_id': route_destination_id,
                  'notes': True,
                  }
        response = self.api.request_address(params)
        return json2obj(response.content)

    def update_address(self, data, route_id, route_destination_id):
        params = {'route_id': route_id,
                  'route_destination_id': route_destination_id
                  }
        params.update({'api_key': self.key})
        data = json.dumps(data)
        response = self.api._make_request(ADDRESS_HOST,
                                          params,
                                          data,
                                          self.api._request_put)
        return json2obj(response.content)

    def delete_address_from_route(self, route_id, route_destination_id):
        params = {'route_id': route_id,
                  'route_destination_id': route_destination_id
                  }
        params.update({'api_key': self.key})
        response = self.api._make_request(ADDRESS_HOST,
                                          params,
                                          None,
                                          self.api._request_delete)

        return json2obj(response.content)

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
            response = json2obj(self.response.content)
            return response

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
