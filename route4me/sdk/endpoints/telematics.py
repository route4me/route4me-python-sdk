# -*- coding: utf-8 -*-

from .._net import NetworkClient


class Telematics(object):
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


# import requests
# # import json

# from app.utils import profile
# from app.logger import get_logger
# log = get_logger(__name__)

# _API_HOST = 'https://www.route4me.com/api.v4/telematics'
# _PRODUCTION_API_TELEMATICS = "https://telematics-api/api"

# # R4M
# _TELEMATICS_REGISTER = '{0}/register.php'.format(_API_HOST)
# _TELEMATICS_CONNECTION = '{0}/connections.php'.format(_API_HOST)
# _TELEMATICS_VEHICLE = '{0}/connected-vehicles.php'.format(_API_HOST)

# _TELEMATICS_VENDORS = "{0}/vendors".format(_PRODUCTION_API_TELEMATICS)


# @profile
# def connection_vehicles(connection_token, api_token):
# 	params = {
# 		'api_token': api_token,
# 		'connection_token': connection_token,
# 	}
# 	response = requests.get(_TELEMATICS_VEHICLE, params=params)
# 	try:
# 		return response.json()

# 	except ValueError:
# 		return response.content


# @profile
# def member_registration(params):
# 	response = requests.request('GET', _TELEMATICS_REGISTER,
# 								params=params)
# 	try:
# 		return response.json()
# 	except ValueError:
# 		return response.content


# @profile
# def connection_create(params, verify=True):
# 	params['validate_remote_credentials'] = "true"
# 	try:
# 		response = requests.post(_TELEMATICS_CONNECTION, params=params, verify=verify)
# 		response = response.json()
# 		return response
# 	except ValueError:
# 		return {'error': 'Error creating connection'}


# @profile
# def connection_delete(connection_token, api_token):
# 	params = {
# 		'api_token': api_token,
# 		'connection_token': connection_token
# 	}
# 	response = requests.delete(_TELEMATICS_CONNECTION, params=params)

# 	try:
# 		return response.json()
# 	except ValueError:
# 		return {'error': 'Error deleting connection'}


# @profile
# def get_vendors(api_token):
# 	params = {
# 		'api_token': api_token,
# 	}

# 	# TODO: don't ignore SSL errors!!
# 	# see gh #333
# 	response = requests.get(_TELEMATICS_VENDORS, params=params, verify=False)
# 	try:
# 		return response.json()

# 	except ValueError:
# 		return response.content
