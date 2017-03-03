import unittest

from route4me.exceptions import ParamValueException
from tests.base import Route4MeAPITestSuite


class Route4MeAddressesTests(Route4MeAPITestSuite):
    """
    Route4Me Addresses Tests
    """

    def test_addresses_params(self):
        addresses = self.route4me.address
        self.assertRaises(ParamValueException,
                          addresses.add_address,
                          address='754 5th Ave New York, NY 10019')


if __name__ == '__main__':
    unittest.main()
