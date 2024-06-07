# -*- coding: utf-8 -*-

from .api_endpoints import SET_GPS_HOST, DEVICE_LOCATION_URL
from .base import Base
from .exceptions import ParamValueException


class GPS(Base):
    """
        Set GPS position of the device
    """

    requirements = ('api_key',
                    'format',
                    'member_id',
                    'route_id',
                    'course',
                    'speed',
                    'lat',
                    'lng',
                    'device_type',
                    'device_guid',
                    'device_timestamp',
                    )

    def __init__(self, api):
        self.response = None
        self.params = {'api_key': api.key, }
        Base.__init__(self, api)

    def set_gps_track(self, **kwargs):
        """
        Set GPS position of device using GET request
        :return: Response status
        :raise: ParamValueException if any required param is not set
        """
        kwargs.update(self.params)
        if self.check_required_params(kwargs, self.requirements):
            self.response = self.api._request_get(SET_GPS_HOST,
                                                  kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_locations(self, **kwargs):
        """
        Get GPS tracks of a vehicle using GET request
        :return: Response status
        :raise: ParamValueException if any required param is not set
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, [
            'api_key',
            'format',
            'route_id',
            'member_id',
            'time_period',
        ]):
            self.response = self.api._request_get(DEVICE_LOCATION_URL,
                                                  kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')
