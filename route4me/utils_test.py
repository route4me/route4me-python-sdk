import pytest

import utils


class TestUtils(object):

    def test_json2obj(self):
        """
        simple json
        """
        act = utils.json2obj('{"key": 123}')
        exp = {
            "key": 123
        }
        assert act == exp

    def test_json2obj_non_letter_keys(self):
        """
        non-letters among keys
        """

        act = utils.json2obj('{"key#11": 12}')
        exp = {
            "key#11" : 12
        }
        assert act == exp
