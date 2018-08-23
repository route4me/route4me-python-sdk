# -*- coding: utf-8 -*-
# codebeat:disable[SIMILARITY, BLOCK_NESTING]

import json

from .api_endpoints import TERRITORY_HOST
from .base import Base
from .exceptions import ParamValueException


class Territory(Base):
    """
    Territory Management
    """

    def __init__(self, api, addresses=[]):
        """
        Territory Instance
        :param api:
        :return:
        """
        self.json_data = {}
        Base.__init__(self, api)

    def get_territories(self):
        """
        Get territories using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        if self.check_required_params(self.params, ['api_key', ]):
            self.response = self.api._request_get(TERRITORY_HOST,
                                                  self.params)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_territory(self, **kwargs):
        """
        Get Territory using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['api_key', 'territory_id']):
            self.response = self.api._request_get(TERRITORY_HOST,
                                                  kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def add_territory(self, **kwargs):
        """
        Add territory using POST request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        if self.check_required_params(kwargs, ['territory_name',
                                               'territory_color',
                                               'territory']):
            self.response = self.api._request_post(TERRITORY_HOST,
                                                   self.params,
                                                   data=json.dumps(kwargs))
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def delete_territory(self, **kwargs):
        """
        Delete territory using DELETE request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['territory_id']):
            self.response = self.api._request_delete(TERRITORY_HOST,
                                                     kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def update_territory(self, territory_id, **kwargs):
        """
        Delete territory using DELETE request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        self.params.update({'territory_id': territory_id})
        if self.check_required_params(kwargs, ['territory_name',
                                               'territory_color',
                                               'territory']):
            self.response = self.api._request_put(TERRITORY_HOST,
                                                  self.params,
                                                  data=json.dumps(kwargs))
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

# codebeat:enable[SIMILARITY, BLOCK_NESTING]
