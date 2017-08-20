"""
Official Python SDK for Route4Me

"""

import logging

from . import version

log = logging.getLogger(__name__)


__version__ = version.VERSION_STRING
__build__ = version.BUILD
__commit__ = version.COMMIT
__title__ = 'route4me-sdk'


class Route4Me:
	"""
	Route4Me API client (implements all SDK features)

	Contains all methods and namespaces available to work with Route4Me API
	"""

	version = version.VERSION_STRING

	def __init__(self, api_key=None):
		log.info('Init Route4Me Python SDK [%s]', self.version)
