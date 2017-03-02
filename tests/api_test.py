import unittest
from route4me.exceptions import ParamValueException
from route4me import Route4Me
from route4me.constants import *

KEY = '11111111111111111111111111111111'


class Route4MeAPITestSuite(unittest.TestCase):
    """
    Route4Me Test Suite
    """

    def setUp(self):
        self.route4me = Route4Me(KEY)

    def test_api_key(self):
        """
        Test that API key is set
        :return:
        """
        return self.assertEquals(self.route4me.key, KEY)

    def test_route_name(self):
        """
        Test that route_name is set correctly
        :return:
        """
        route_name = 'Single Driver Round Trip'
        self.route4me.optimization.route_name(route_name)
        data = self.route4me.optimization.data['parameters']
        return self.assertEquals(route_name, data['route_name'])

    def test_route_name_validation(self):
        """
        Test route_name validation
        :return:
        """
        route_name = 234567890
        optimization = self.route4me.optimization
        return self.assertRaises(ParamValueException,
                                 optimization.route_name, route_name)

    def test_set(self):
        """
        Test Set GPS
        :return:
        """
        setGPS = self.route4me.setGPS
        setGPS.params.update({
            'format': FORMAT.CSV,
            'route_id': '7420A6120C1BA7B83C512E61416AECD0',
            'lat': 38.141598,
            'lng': -85.793846,
            'course': 1,
            'speed': 120,
            'device_type': DEVICE_TYPE.IPHONE,
            'member_id': 1,
            'device_guid': 'qweqweqwe',
            'device_timestamp': '2014-06-14 17:43:35',
        })
        return self.assertTrue(setGPS.set_gps_params())

    def test_set_valid_device_timestamp(self):
        """
        Valid Timestamp
        :return:
        """
        setGPS = self.route4me.setGPS
        device_timestamp = '2014-36-99 57:83:85'
        return self.assertRaises(ParamValueException,
                                 setGPS.device_timestamp, device_timestamp)

    def test_route(self):
        route = self.route4me.route
        response = route.get_routes(limit=10, Offset=5)
        if hasattr(response, 'errors'):
            print '. '.join(response.errors)
        else:
            route_id = response[0].route_id
            response = route.get_route(route_id=route_id)
            return self.assertEqual(response.route_id,
                                    route_id)

    def test_optimization(self):
        optimization = self.route4me.optimization
        address = self.route4me.address
        optimization.add(data={
            'algorithm_type': ALGORITHM_TYPE.TSP,
            'share_route': 0,
            'store_route': 0,
            'route_time': 0,
            'route_max_duration': 86400,
            'vehicle_capacity': 1,
            'vehicle_max_distance_mi': 10000,
            'route_name': 'Single Driver Round Trip',
            'optimize': OPTIMIZE.DISTANCE,
            'distance_unit': DISTANCE_UNIT.MI,
            'device_type': DEVICE_TYPE.WEB,
            'travel_mode': TRAVEL_MODE.DRIVING,
        })
        address.add_address(
            address='754 5th Ave New York, NY 10019',
            lat=40.7636197,
            lng=-73.9744388,
            alias='Bergdorf Goodman',
            is_depot=1,
            time=0
        )
        address.add_address(
            address='717 5th Ave New York, NY 10022',
            lat=40.7669692,
            lng=-73.9693864,
            alias='Giorgio Armani',
            time=0
        )
        address.add_address(
            address='888 Madison Ave New York, NY 10014',
            lat=40.7715154,
            lng=-73.9669241,
            alias='Ralph Lauren Women\'s and Home',
            time=0
        )
        address.add_address(
            address='1011 Madison Ave New York, NY 10075',
            lat=40.7772129,
            lng=-73.9669,
            alias='Yigal Azrou\u00ebl',
            time=0
        )
        address.add_address(
            address='440 Columbus Ave New York, NY 10024',
            lat=40.7808364,
            lng=-73.9732729,
            alias='Frank Stella Clothier',
            time=0
        )
        address.add_address(
            address='324 Columbus Ave #1 New York, NY 10023',
            lat=40.7803123,
            lng=-73.9793079,
            alias='Liana',
            time=0
        )
        address.add_address(
            address='110 W End Ave New York, NY 10023',
            lat=40.7753077,
            lng=-73.9861529,
            alias='Toga Bike Shop',
            time=0
        )
        address.add_address(
            address='555 W 57th St New York, NY 10019',
            lat=40.7718005,
            lng=-73.9897716,
            alias='BMW of Manhattan',
            time=0
        )
        address.add_address(
            address='57 W 57th St New York, NY 10019',
            lat=40.7558695,
            lng=-73.9862019,
            alias='Verizon Wireless',
            time=0
        )
        response = self.route4me.run_optimization()
        return self.assertEqual(4, response.state)

    def test_param_dict_validation(self):
        gps = self.route4me.setGPS
        return self.assertRaises(ParamValueException,
                                 gps.add, {'xxxx': 100})

    def test_addresses_params(self):
        addresses = self.route4me.address
        return self.assertRaises(ParamValueException,
                                 addresses.add_address,
                                 address='754 5th Ave New York, NY 10019')

if __name__ == '__main__':
    unittest.main()
