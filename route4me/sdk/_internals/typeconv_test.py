# -*- coding: utf-8 -*-

import pytest

from .typeconv import str2bool
from .typeconv import bool201


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


class Test_bool201(object):
	@pytest.mark.parametrize('b, exp', [
		(True, '1'),
		(False, '0'),
	])
	def test_normal(self, b, exp):
		act = bool201(b)

		assert act == exp

	@pytest.mark.parametrize('b', [
		(None),
	])
	def test_raises_TypeError(self, b):
		with pytest.raises(TypeError):
			bool201(b)


class TestFunctionCompositions(object):

	@pytest.mark.parametrize('b', [
		(u'0'),
		(u'1'),
	])
	def test_bool201_str2bool(self, b):
		act = bool201(str2bool(b))

		assert act == b

	@pytest.mark.parametrize('b', [
		(False),
		(True),
	])
	def test_str2bool_bool201(self, b):
		act = str2bool(bool201(b))

		assert act == b
