# -*- coding: utf-8 -*-

from .._net import NetworkClient


class Geocodings(object):
	"""
	Geocondings stuff

	.. seealso:: https://route4me.io/docs/#geocoding
	"""
	def __init__(self, api_key=None, _network_client=None):
		nc = _network_client
		if nc is None:
			nc = NetworkClient(api_key)

	def create(self):
		pass

	def get(self):
		pass

	def list(self):
		pass

	def update(self):
		pass

	def remove(self):
		pass
