# -*- coding: utf-8 -*-

"""
Geocoding is the process of converting addresses (like *"1600 Amphitheatre
Parkway, Mountain View, CA"*) into geographic coordinates (like *"latitude
37.423021 and longitude -122.083739"*), which you can use to place markers on
a map or position the map.

.. seealso:: https://route4me.io/docs/#geocoding

"""

from .._net import NetworkClient


class Geocodings(object):
	"""
	Geocondings stuff

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
