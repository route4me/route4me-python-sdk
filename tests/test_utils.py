import json
import unittest

from route4me.utils import json2obj
from tests.base import Route4MeAPITestSuite


class Route4MeUtilsTests(Route4MeAPITestSuite):
    """
    Route4Me Utils Tests
    """

    def test_json2obj(self):
        json_data = json.dumps({'variable1': 'test_value'})
        json_obj = json2obj(json_data)
        self.assertTrue(hasattr(json_obj, 'variable1'))


if __name__ == '__main__':
    unittest.main()
