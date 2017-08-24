# -*- coding: utf-8 -*-

import re
import pytest
import json

from ._net import NetworkClient
from .errors import Route4MeNetworkError
from .errors import Route4MeApiError


class TestNetworkClient:
	def test_constructor(self):

		api_key = '11111111111111111111111111111111'

		nc = NetworkClient(api_key=api_key)

		assert nc is not None
		assert isinstance(nc, NetworkClient)

	def test_default_fields(self):
		api_key = '11111111111111111111111111111111'

		nc = NetworkClient(api_key=api_key)

		assert re.match(r'^requests\/.*Route4Me-Python-SDK\/.*$', nc.user_agent), (
			'user_agent contains `requests` and `Route4Me`'
		)


@pytest.mark.network
class TestNetworkClientRequestsOverHttpbin:

	def test_ctor(self):
		nc = NetworkClient(api_key='AAAA', base_host='httpbin.org')

		assert isinstance(nc, NetworkClient)

	# ==========================================================================
	# GET
	# ==========================================================================

	def test_get(self):
		nc = NetworkClient(api_key='AAAA', base_host='httpbin.org')
		res = nc.get('anything', timeout_sec=8)

		# https://www.httpbin.org/get?param3=345&api_key=AAAA&param1=1&param4=False&format=json&param2=str'
		url = res['url']
		assert url in (
			'https://httpbin.org/anything?api_key=AAAA&format=json',
			'https://httpbin.org/anything?format=json&api_key=AAAA'
		)

		# requests/2.18.3 (Linux 4.8.0-53-generic) Route4Me-Python-SDK/0.1.0-dev.4 CPython/3.5.2
		user_agent = res['headers']['Route4Me-Agent']
		assert re.match(r'^requests\/.*Route4Me-Python-SDK\/.*$', user_agent), (
			'user_agent contains `requests` and `Route4Me`'
		)

		accept = res['headers']['Accept']
		assert accept == 'application/json'
		assert res['method'] == 'GET'

	@pytest.mark.parametrize('subdomain, exp_prefix', [
		(None, 'https://httpbin.org/anything'),
		('', 'https://httpbin.org/anything'),
		('www', 'https://www.httpbin.org/anything'),
	])
	def test_get_with_subdomains(self, subdomain, exp_prefix):
		nc = NetworkClient(api_key='AAAA', base_host='httpbin.org')
		res = nc.get('anything', subdomain=subdomain, timeout_sec=8)

		# https://www.httpbin.org/anything?param3=345&api_key=AAAA&param1=1&param4=False&format=json&param2=str'
		url = res['url']
		assert url.startswith(exp_prefix)
		assert 'api_key=AAAA' in url
		assert 'format=json' in url

	def test_get_with_params(self):
		nc = NetworkClient(api_key='AAAA', base_host='httpbin.org')
		res = nc.get(
			path='anything',
			timeout_sec=8,
			subdomain='www',

			query={
				'param1': 1,
				'param2': 'str',
				'param3': '345',
				'param4': False,
			}
		)

		# https://www.httpbin.org/get?param3=345&api_key=AAAA&param1=1&param4=False&format=json&param2=str'
		url = res['url']
		assert url.startswith('https://www.httpbin.org/anything')
		assert 'api_key=AAAA' in url
		assert 'format=json' in url
		assert 'param1=1' in url
		assert 'param2=str' in url
		assert 'param3=345' in url
		assert 'param4=False' in url

	# ==========================================================================
	# POST
	# ==========================================================================

	@pytest.mark.slow
	def test_post_with_params(self):
		nc = NetworkClient(api_key='AAAA', base_host='httpbin.org')
		res = nc.post(
			path='anything',
			timeout_sec=8,
			data={
				'param1': 1,
				'param2': 'str',
				'param3': '345',
				'param4': False,
			}
		)

		print(res)

		# https://www.httpbin.org/anything?param3=345&api_key=AAAA&param1=1&param4=False&format=json&param2=str'
		url = res['url']
		assert url.startswith('https://httpbin.org/anything')
		assert 'api_key=AAAA' in url
		assert 'format=json' in url
		assert res['method'] == 'POST'

		assert res['headers']['Content-Type'] == 'application/json'

		assert res['json'] == {
			'param1': 1,
			'param2': 'str',
			'param3': '345',
			'param4': False,
		}

		raw_data = res['data']
		data = json.loads(raw_data)

		assert data == {
			'param1': 1,
			'param2': 'str',
			'param3': '345',
			'param4': False,
		}

		assert res['form'] == {}

	# ==========================================================================
	# FORM
	# ==========================================================================

	@pytest.mark.slow
	def test_post_form_with_params(self):
		nc = NetworkClient(api_key='AAAA', base_host='httpbin.org')
		res = nc.form(
			path='anything',
			timeout_sec=8,
			data={
				'param1': 1,
				'param2': 'str',
				'param3': '345',
				'param4': False,
			}
		)

		print(res)

		url = res['url']
		assert url.startswith('https://httpbin.org/anything')
		assert 'api_key=AAAA' in url
		assert 'format=json' in url

		# 'multipart/form-data'
		assert res['headers']['Content-Type'] == 'application/x-www-form-urlencoded'

		assert res['json'] is None
		assert res['data'] == ''

		assert res['form'] == {
			'param1': '1',
			'param2': 'str',
			'param3': '345',
			'param4': 'False',
		}

	# ==========================================================================
	# EXCEPTIONS
	# ==========================================================================
	@pytest.mark.slow
	def test_get_raises_on_timeout(self):
		nc = NetworkClient(api_key='AAAA', base_host='httpbin.org')
		with pytest.raises(Route4MeNetworkError) as exc_info:
			nc.get('delay/10')

		exc = exc_info.value
		assert exc is not None
		assert exc.code == 'route4me.sdk.network.timeout'

	@pytest.mark.slow
	def test_get_raises_on_many_redirect(self):
		nc = NetworkClient(api_key='AAAA', base_host='httpbin.org')
		with pytest.raises(Route4MeNetworkError) as exc_info:
			nc.get('relative-redirect/10', timeout_sec=10)

		exc = exc_info.value
		print(exc)
		assert exc is not None
		assert exc.code == 'route4me.sdk.network.many_redirects'

	def test_get_raises_on_no_connection(self):
		nc = NetworkClient(api_key='AAAA', base_host='no.such.host.httpbin.org')
		with pytest.raises(Route4MeNetworkError) as exc_info:
			nc.get('get/1', timeout_sec=8)

		exc = exc_info.value
		assert exc is not None
		assert exc.code == 'route4me.sdk.network.no_connection'

	def test_get_raises_on_ssl_compromised(self):
		nc = NetworkClient(api_key='BBBB', base_host='expired.badssl.com')
		with pytest.raises(Route4MeNetworkError) as exc_info:
			nc.get('get/1', timeout_sec=8)

		exc = exc_info.value
		print(exc)
		assert exc is not None
		assert exc.code == 'route4me.sdk.security.invalid_certificate'

	# --------------------------------------------------------------------------

	def test_get_raises_on_status_400(self):
		nc = NetworkClient(api_key='AAAABBBB', base_host='httpbin.org')
		with pytest.raises(Route4MeApiError) as exc_info:
			nc.get('status/404', timeout_sec=15)

		exc = exc_info.value
		assert exc is not None
		assert exc.code == 'route4me.sdk.api_error'
