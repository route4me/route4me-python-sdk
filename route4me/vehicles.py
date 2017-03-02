# codebeat:disable[SIMILARITY, BLOCK_NESTING]
import json

from route4me.base import Base
from route4me.exceptions import ParamValueException, APIException
from route4me.api_endpoints import VEHICLES_HOST


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
            self.response = self.api._request_get(VEHICLES_HOST,
                                                  self.params)
            try:
                self.json_data = self.response.json()
                return self.json_data
            except ValueError:
                raise APIException(self.response.status_code,
                                   self.response.content,
                                   self.response.url)
        else:
            raise ParamValueException('params', 'Params are not complete')

# codebeat:enable[SIMILARITY, BLOCK_NESTING]
