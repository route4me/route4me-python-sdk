# -*- coding: utf-8 -*-

"""
Internal module, provides HTTP access to API
"""

import re
import requests
import platform
import logging

from .errors import Route4MeNetworkError
from .errors import Route4MeApiError

from .version import VERSION_STRING
from .version import RELEASE_STRING
from .version import BUILD
from .version import COMMIT

log = logging.getLogger(__name__)


class FluentRequest:
	def __init__(self):
		self._r = requests.Request(
			method='GET'
		)
		self.__timeout = 0.1

		# self.method = method
		# self.url = url
		# self.headers = headers
		# self.files = files
		# self.data = data
		# self.json = json
		# self.params = params
		# self.auth = auth
		# self.cookies = cookies

	@staticmethod
	def __cut_qs(url):
		return re.sub(r'\?.*', '?***', url)

	def timeout(self, timeout):
		self.__timeout = float(timeout)
		return self

	def header(self, name, value):
		n = name.upper()
		self._r.headers[n] = value
		return self

	def user_agent(self, value):
		return self.header('user-agent', value)

	def accept(self, value):
		return self.header('accept', value)

	def method(self, method):
		m = method.upper()
		self._r.method = m
		return self

	def url(self, url):
		self._r.url = url
		return self

	def qs(self, query):
		if query:
			self._r.params.update(query)
		return self

	def form(self, form):
		self.header('Content-Type', 'application/x-www-form-urlencoded')
		self._r.data = form
		return self

	def json(self, json):
		self.header('Content-Type', 'application/json')
		self._r.json = json
		return self

	def send(self):
		with requests.sessions.Session() as s:
			s.max_redirects = 1
			s.verify = True

			preq = s.prepare_request(self._r)
			log.debug(
				'send prepared request [%s] [%s]',
				preq.method,
				FluentRequest.__cut_qs(preq.url)
			)

			return s.send(
				preq,
				timeout=self.__timeout
			)

	def __repr__(self):
		return '<FluentRequest, [{method}] [{url}]>'.format(
			method=self._r.method,
			url=self._r.url,
		)


class NetworkClient:
	"""
	Internal API-client

	.. versionadded:: 0.1.0
	"""

	DEFAULT_TIMEOUT_SEC = 0.1

	def __init__(self, api_key, base_host='route4me.com'):

		user_agent = (
			'requests/{requests_version} '
			'({platform_name} {platform_version}) '
			'Route4Me-Python-SDK/{sdk_version} '
			'{python_implementation}/{python_version}'
		).format(
			requests_version=requests.__version__,
			platform_name=platform.system(),
			platform_version=platform.release(),
			sdk_version=VERSION_STRING,
			python_version=platform.python_version(),
			python_implementation=platform.python_implementation(),
		)

		self._user_agent = user_agent
		self.base_host = base_host
		self.api_key = api_key

	@property
	def user_agent(self):
		"""
		The value of `User-Agent` HTTP-header.

		Example:

		.. code-block:: python

		    'requests/2.18.3 (Linux 4.8.0-53-generic) Route4Me-Python-SDK/0.1.0-dev.4 CPython/3.5.2'

		:rtype: {str}
		"""  # noqa: E101
		return self._user_agent

	def __url(self, path, subdomain):
		subdomain = subdomain + '.' if subdomain else ''

		# remove leading slashes from path
		path = re.sub(r'^/+', '', path)

		url = 'https://{subdomain}{base_host}/{path}'.format(
			subdomain=subdomain,
			base_host=self.base_host,
			path=path,
		)
		return url

	def __read_response(self, req):
		res = self.__handle_net_exceptions(req)

		if res.status_code >= 300:
			print(res.status_code)

			# TODO: need more details!
			raise Route4MeApiError(
				'Error on Route4Me API',
				code='route4me.sdk.api_error',
				details={
					'req': req.__repr__(),
					'status_code': res.status_code,
				}
			)
		res.encoding = 'utf-8'
		return res.json()

	def __handle_net_exceptions(self, req):
		req.user_agent(self.user_agent)
		req.header('Route4Me-Agent', self.user_agent)
		req.header('Route4Me-Agent-Release', RELEASE_STRING)
		req.header('Route4Me-Agent-Commit', COMMIT)
		req.header('Route4Me-Agent-Build', BUILD)
		req.accept('application/json')
		req.header('Route4Me-Api-Key', self.api_key)

		req.qs({
			'api_key': self.api_key,    # TODO: security issue
			'format': 'json',
		})

		try:
			return req.send()

		except requests.exceptions.SSLError as exc:
			err = Route4MeNetworkError(
				message='SSL check failed',
				code='route4me.sdk.security.invalid_certificate',
				inner=exc,
			)
			log.error(err, exc_info=True)
			raise err
		except requests.exceptions.TooManyRedirects as exc:
			err = Route4MeNetworkError(
				message='Too many redirects',
				code='route4me.sdk.network.many_redirects',
				inner=exc,
				# details={
				# 	'max_redirects': req.max_redirects,
				# }
			)
			log.error(err, exc_info=True)
			raise err
		except requests.exceptions.Timeout as exc:
			err = Route4MeNetworkError(
				message='Network timeout (still no bytes received)',
				code='route4me.sdk.network.timeout',
				details={
					'timeout': req.timeout,
					'timeout_unit': 'sec',
				},
				inner=exc,
			)
			log.error(err, exc_info=True)
			raise err
		except requests.exceptions.ConnectionError as exc:
			err = Route4MeNetworkError(
				message='Can not connect, check your connection settings',
				code='route4me.sdk.network.no_connection',
				inner=exc,
			)
			log.error(err, exc_info=True)
			raise err

	def get(self, path, query=None, subdomain=None, timeout_sec=None):

		url = self.__url(path, subdomain=subdomain)

		req = FluentRequest()
		req.method('GET')
		req.url(url)
		req.qs(query)

		if timeout_sec is not None:
			req.timeout(timeout_sec)

		return self.__read_response(req)

	def delete(self, path, query=None, data=None, subdomain=None, timeout_sec=None):

		url = self.__url(path, subdomain=subdomain)

		req = FluentRequest()
		req.method('DELETE')
		req.url(url)
		req.qs(query)
		req.json(data)

		if timeout_sec is not None:
			req.timeout(timeout_sec)

		return self.__read_response(req)

	def post(self, path, query=None, data=None, subdomain=None, timeout_sec=None):

		url = self.__url(path, subdomain=subdomain)

		req = FluentRequest()
		req.method('POST')
		req.url(url)
		req.qs(query)
		req.json(data)

		if timeout_sec is not None:
			req.timeout(timeout_sec)

		return self.__read_response(req)

	def form(self, path, query=None, data=None, subdomain=None, timeout_sec=None):
		"""
		Posts form data as `multipart/form-data`.

		:param path str:         Path (part of URL) to API method
		:param subdomains [str]: Send request to other subdomain of the API
		:param **qargs: [description]
		:returns: API response, JSON converted to ..
		:rtype: {dict}
		"""
		url = self.__url(path, subdomain=subdomain)

		req = FluentRequest()
		req.method('POST')
		req.url(url)
		req.qs(query)
		req.form(data)

		if timeout_sec is not None:
			req.timeout(timeout_sec)

		return self.__read_response(req)
