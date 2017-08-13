# import pytest

from . import Route4Me


class TestRoute4Me:
	def test_init(self):
		route4me = Route4Me()

		assert hasattr(Route4Me, 'version'), '`Route4Me.version` is present'

		assert isinstance(route4me, Route4Me)
		assert hasattr(route4me, 'version'), '`route4me.version` is present (on instance)'
