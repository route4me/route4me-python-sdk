import unittest

from route4me import Route4Me


class Route4MeAPITestSuite(unittest.TestCase):
    """
    Route4Me Test Suite Base
    """

    def setUp(self):
        KEY = '11111111111111111111111111111111'
        self.route4me = Route4Me(KEY)
