import unittest

from route4me.exceptions import ParamValueException
from tests.base import Route4MeAPITestSuite


class Route4MeGPSTests(Route4MeAPITestSuite):
    """
    Route4Me Optimization Tests
    """

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
