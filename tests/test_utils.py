import json
import unittest

from route4me.utils import clean_dict, is_valid_datetime, json2obj
from tests.base import Route4MeAPITestSuite


class Route4MeUtilsTests(Route4MeAPITestSuite):
    """
    Route4Me Utils Tests
    """

    def test_json2obj(self):
        json_data = json.dumps({"variable1": "test_value"})
        json_obj = json2obj(json_data)
        self.assertTrue(hasattr(json_obj, "variable1"))
        self.assertEqual(json_obj.variable1, "test_value")

    def test_json2obj_nested_objects(self):
        """Nested dicts become nested namedtuples, not raw dicts."""
        json_obj = json2obj(json.dumps({"outer": {"inner": {"leaf": 42}}}))
        self.assertEqual(json_obj.outer.inner.leaf, 42)

    def test_json2obj_digit_leading_keys_are_prefixed(self):
        """`d_` prefix branch: a key starting with a digit is not a valid
        Python identifier, so `_json_object_hook` renames it."""
        json_obj = json2obj(json.dumps({"1st_stop": "depot", "normal": "x"}))
        self.assertEqual(json_obj.d_1st_stop, "depot")
        self.assertEqual(json_obj.normal, "x")
        self.assertFalse(hasattr(json_obj, "1st_stop"))

    def test_json2obj_objects_inside_lists(self):
        json_obj = json2obj(json.dumps({"stops": [{"seq": 0}, {"seq": 1}]}))
        self.assertEqual([s.seq for s in json_obj.stops], [0, 1])

    def test_json2obj_empty_object(self):
        """An empty dict yields a zero-field namedtuple, not an error."""
        self.assertEqual(len(json2obj(json.dumps({}))._fields), 0)

    def test_json2obj_passes_scalars_and_arrays_through(self):
        self.assertEqual(json2obj(json.dumps([1, 2, 3])), [1, 2, 3])
        self.assertEqual(json2obj(json.dumps("plain")), "plain")

    def test_is_valid_datetime(self):
        self.assertTrue(is_valid_datetime("2024-06-24 13:45:00"))
        self.assertFalse(is_valid_datetime("2014-36-99 57:83:85"))
        self.assertFalse(is_valid_datetime("not a date"))
        self.assertTrue(is_valid_datetime("2024-06-24", date_format="%Y-%m-%d"))
        # Non-string input is coerced with str() before parsing.
        self.assertFalse(is_valid_datetime(12345))

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


if __name__ == "__main__":
    unittest.main()
