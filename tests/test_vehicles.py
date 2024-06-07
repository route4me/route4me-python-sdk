import unittest

from tests.base import Route4MeAPITestSuite


class Route4MeVehicleTests(Route4MeAPITestSuite):
    def test_get_vehicles(self):
        response = self.route4me.vehicles.get_vehicles()
        self.assertTrue(len(response) > 0)
        self.assertTrue('vehicle_id' in response[0].keys())
        self.assertTrue('vehicle_alias' in response[0].keys())
        self.assertTrue('member_id' in response[0].keys())
        self.assertTrue('created_time' in response[0].keys())


if __name__ == '__main__':
    unittest.main()
