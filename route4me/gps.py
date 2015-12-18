from base import Base
from exceptions import ParamValueException
from utils import json2obj
from api_endpoints import SET_GPS_HOST


class SetGPS(Base):
    """
        Set GPS position of the device
    """

    requirements = [
            'api_key',
            'format',
            'member_id',
            'route_id',
            'course',
            'speed',
            'lat',
            'lng',
            'device_type',
            'device_guid',
    ]

    def __init__(self, api):
        self.response = None
        self.params = {'api_key': api.key, }
        Base.__init__(self, api)

    @staticmethod
    def _build_set_url():
        """
        Return SET HOST
        :return:
        """
        return SET_GPS_HOST + '?'

    def set_gps_params(self):
        """
        Set GPS position of device using GET request
        :return: Response status
        :raise: ParamValueException if any required param is not set
        """
        if self.required_params(self.requirements):
            self.response = self.api._request_get(self._build_set_url(),
                                                  self.params)
            response = json2obj(self.response.content)
            return response.status
        else:
            raise ParamValueException('params', 'Params are not complete')
