# import pytest

from . import Route4Me


class TestRoute4Me:
	def test_init(self):
		route4me = Route4Me()

		assert isinstance(route4me, Route4Me)
