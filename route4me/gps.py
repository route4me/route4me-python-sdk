from route4me.base import Base
from route4me.exceptions import ParamValueException
from route4me.api_endpoints import SET_GPS_HOST


class SetGPS(Base):
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
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, self.requirements):
            self.response = self.api._request_get(SET_GPS_HOST,
                                                  self.params)
            response = self.response.json()
            return response.get('status')
        else:
            raise ParamValueException('params', 'Params are not complete')
