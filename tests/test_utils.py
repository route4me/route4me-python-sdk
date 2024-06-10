import json
import unittest

from route4me.utils import json2obj
from route4me.utils import clean_dict
from tests.base import Route4MeAPITestSuite


class Route4MeUtilsTests(Route4MeAPITestSuite):
    """
    Route4Me Utils Tests
    """

    def test_json2obj(self):
        json_data = json.dumps({'variable1': 'test_value'})
        json_obj = json2obj(json_data)
        self.assertTrue(hasattr(json_obj, 'variable1'))

    def test_clean_dict(self):
        # None and "" values
        input_dict = {"key1": "value1", "key2": None, "key3": "", "key4": ["", None, "value4"]}
        cleaned_dict = clean_dict(input_dict)
        expected_dict = {"key1": "value1", "key4": ["", "value4"]}
        self.assertEqual(cleaned_dict, expected_dict)

        # empty dict and list values
        input_dict = {"key1": "value1", "key2": {}, "key3": []}
        cleaned_dict = clean_dict(input_dict)
        expected_dict = {"key1": "value1"}
        self.assertEqual(cleaned_dict, expected_dict)

        # None and "" values
        input_list = ["value1", None, "", ["", None, "value2"]]
        cleaned_list = clean_dict(input_list)
        expected_list = ["value1", "", ["", "value2"]]
        self.assertEqual(cleaned_list, expected_list)

        # empty dict and list values
        input_list = ["value1", {}, []]
        cleaned_list = clean_dict(input_list)
        expected_list = ["value1"]
        self.assertEqual(cleaned_list, expected_list)


if __name__ == '__main__':
    unittest.main()
