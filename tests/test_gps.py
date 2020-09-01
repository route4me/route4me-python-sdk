import datetime
import unittest

from route4me.constants import FORMAT, DEVICE_TYPE
from route4me.exceptions import ParamValueException
from tests.base import Route4MeAPITestSuite


class Route4MeGPSTests(Route4MeAPITestSuite):
    """
    Route4Me Optimization Tests
    """

    def test_set(self):
        """
        Test Set GPS
        :return:
        """
        route = self.route4me.route
        response = route.get_routes(limit=1, offset=0)
        self.assertFalse(isinstance(response, dict) and 'errors' in response.keys())
        self.assertTrue(len(response) == 1)
        route_id = response[0].get('route_id', False)
        now = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()
        device_timestamp = response[0].get('route_date', now)
        gps = self.route4me.gps
        params = {
            'format': FORMAT.SERIALIZED,
            'route_id': route_id,
            'lat': 38.141598,
            'lng': -85.793846,
            'course': 1,
            'speed': 40,
            'device_type': DEVICE_TYPE.WEB,
            'member_id': 1,
            'device_guid': '111111',
            'device_timestamp': device_timestamp,
        }
        response = gps.set_gps_track(**params)
        return self.assertTrue(response['status'])

    def test_set_valid_device_timestamp(self):
        """
        Valid Timestamp
        :return:
        """
        gps = self.route4me.gps
        device_timestamp = '2014-36-99 57:83:85'
        return self.assertRaises(ParamValueException,
                                 gps.device_timestamp, device_timestamp)

    def test_param_dict_validation(self):
        gps = self.route4me.gps
        self.assertRaises(ParamValueException,
                          gps.add, {'xxxx': 100})


if __name__ == '__main__':
    unittest.main()
