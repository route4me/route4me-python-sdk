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
        response = route.get_routes(limit=10, offset=5)
        self.assertFalse(hasattr(response, 'errors'))
        self.assertTrue(len(response) > 0)
        route_id = response[0].get('route_id', False)
        print(route_id)
        gps = self.route4me.gps
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params = {
            'format': FORMAT.SERIALIZED,
            'route_id': route_id,
            'lat': 38.141598,
            'lng': -85.793846,
            'course': 1,
            'speed': 120,
            'device_type': DEVICE_TYPE.IPHONE,
            'member_id': 1,
            'device_guid': 'qweqweqwe',
            'device_timestamp': now,
        }
        return self.assertTrue(gps.set_gps_track(**params))

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
