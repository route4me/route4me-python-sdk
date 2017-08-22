# -*- coding: utf-8 -*-

import pytest

from . import ApiClient


class TestApiClient:
	def test_init(self):
		route4me = ApiClient()

		assert hasattr(ApiClient, 'version'), '`ApiClient.version` is present'

		assert isinstance(route4me, ApiClient)
		assert hasattr(route4me, 'version'), '`route4me.version` is present (on instance)'

	@pytest.mark.parametrize('resource_name', [
		# ('activity_feed'),
		# ('addresses'),
		# ('address_book'),
		# ('avoidance_zones'),
		('geocodings'),
		('members'),
		# ('notes'),
		('optimizations'),
		# ('orders'),
		# ('routes'),
		('telematics'),
		# ('territories'),
		# ('tracking'),
		# ('vehicles'),
	])
	def test_has_resource_attr(self, resource_name):
		route4me = ApiClient(api_key='11111111111111111111111111111111')

		assert hasattr(route4me, resource_name)
