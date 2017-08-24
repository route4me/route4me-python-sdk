# -*- coding: utf-8 -*-

"""
Official Python SDK for Route4Me

Contains all required functions to work with Route4Me from Python's environment.
"""

import logging

from ._net import NetworkClient

from .resources.geocodings import Geocodings
from .resources.members import Members
from .resources.optimizations import Optimizations
from .resources.telematics import Telematics

from .version import PROJECT
from .version import COPYRIGHT
from .version import AUTHOR
from .version import TITLE
from .version import LICENSE
from .version import VERSION_STRING
from .version import RELEASE_STRING
from .version import BUILD
from .version import COMMIT

log = logging.getLogger(__name__)


__project__ = PROJECT
__copyright__ = COPYRIGHT
__author__ = AUTHOR
__title__ = TITLE
__license__ = LICENSE
__version__ = VERSION_STRING
__release__ = RELEASE_STRING
__build__ = BUILD
__commit__ = COMMIT


__all__ = [
	'ApiClient',
]


class ApiClient(object):
	"""
	Route4Me API client

	Provides an access to API's endpoints through a convenient interface. In
	other words, all the power of Route4Me API is accessible through this
	class.
	"""

	version = __version__

	def __init__(self, api_key=None):
		log.info(
			'Init Route4Me Python SDK [%s] build [%s] commit [%s]',
			self.version,
			__build__,
			__commit__,
		)

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
