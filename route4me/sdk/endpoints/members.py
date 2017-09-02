# -*- coding: utf-8 -*-

from .._net import NetworkClient


class Members(object):
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
