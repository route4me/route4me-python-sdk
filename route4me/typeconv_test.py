# -*- coding: utf-8 -*-

import pytest

from .typeconv import str2bool


class Test_str2bool(object):
	@pytest.mark.parametrize('s, d, exp', [
		(True, None, True),
		('1', None, True),
		('t', None, True),
		('yEs', None, True),
		('true', None, True),
		('TRUE', None, True),
		('oN', None, True),

		(False, None, False),
		('0', None, False),
		('f', None, False),
		('n', None, False),
		('FaLse', None, False),
		('nO', None, False),
		('Off', None, False),
	])
	def test_str2bool_ignore_default(self, s, d, exp):
		act = str2bool(s)
		assert act == exp

		act = str2bool(s, d)
		assert act == exp

	@pytest.mark.parametrize("s, d, exp", [
		(None,   3,  3),   # noqa: E241
		('01',  -1, -1),   # noqa: E241
		('fka', -2, -2),   # noqa: E241
		('-1',  -3, -3),   # noqa: E241
	])
	def test_str2bool_meaningful_defaults(self, s, d, exp):
		act = str2bool(s, default=d)
		assert act == exp
