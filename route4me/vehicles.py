# -*- coding: utf-8 -*-
# codebeat:disable[SIMILARITY, BLOCK_NESTING]

from .api_endpoints import VEHICLES_HOST
from .base import Base
from .exceptions import ParamValueException, APIException


class Vehicle(Base):
    """
    Vehicles Management
    """

    def __init__(self, api):
        """
        Vehicle Instance
        :param api:
        :return:
        """
        self.json_data = {}
        Base.__init__(self, api)

    def get_vehicles(self):
        """
        Get vehicles using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        if self.check_required_params(self.params, ['api_key', ]):
            try:
                self.response = self.api._make_request(VEHICLES_HOST,
                                                       self.params,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Params are not complete')

# codebeat:enable[SIMILARITY, BLOCK_NESTING]
