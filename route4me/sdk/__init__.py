# -*- coding: utf-8 -*-

"""
Official Python SDK for Route4Me

"""

import logging

from . import version
from ._net import NetworkClient

from .resources.geocodings import Geocodings
from .resources.members import Members
from .resources.optimizations import Optimizations
from .resources.telematics import Telematics

log = logging.getLogger(__name__)

__project__ = 'Route4Me Python SDK'
__copyright__ = '2016-2017 © Route4Me Python Team'
__author__ = 'Route4Me Python Team (SDK)'
__title__ = 'route4me-sdk'
__version__ = version.VERSION_STRING
__release__ = version.RELEASE_STRING
__build__ = version.BUILD
__commit__ = version.COMMIT


__all__ = [
	'ApiClient',
]


class ApiClient:
	"""
	Route4Me API client (implements all SDK features)

	Contains all methods and namespaces available to work with Route4Me API
	"""

	version = version.VERSION_STRING

	def __init__(self, api_key=None):
		log.info('Init Route4Me Python SDK [%s]', self.version)

		nc = NetworkClient(api_key=api_key)

		resource_params = {
			'api_key': api_key,
			'_network_client': nc,
		}

		self.activity_feed   = {}  # noqa: E221  # TODO: implement
		self.addresses       = {}  # noqa: E221  # TODO: implement
		self.address_book    = {}  # noqa: E221  # TODO: implement
		self.avoidance_zones = {}  # noqa: E221  # TODO: implement
		self._geocodings = Geocodings(**resource_params)
		self._members = Members(**resource_params)
		self.notes           = {}  # noqa: E221  # TODO: implement
		self._optimizations = Optimizations(**resource_params)
		self.orders          = {}  # noqa: E221  # TODO: implement
		self.routes          = {}  # noqa: E221  # TODO: implement
		self._telematics = Telematics(**resource_params)
		self.territories     = {}  # noqa: E221  # TODO: implement
		self.tracking        = {}  # noqa: E221  # TODO: implement
		self.vehicles        = {}  # noqa: E221  # TODO: implement

	@property
	def geocodings(self):
		"""
		Geocodings functions

		:returns: Geocoding namespace
		:rtype: :class:`~resources.geocodings.Geocodings`
		"""
		return self._geocodings

	@property
	def members(self):
		return self._members

	@property
	def optimizations(self):
		return self._optimizations

	@property
	def telematics(self):
		return self._telematics
