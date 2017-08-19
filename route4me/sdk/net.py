# -*- coding: utf-8 -*-

"""
Internal module, provides HTTP access to API
"""

import requests
import platform
import logging

from .errors import Route4MeNetworkError

from .version import VERSION_STRING

log = logging.getLogger(__name__)


def _handle_subdomains(sd):
	if sd is None:
		sd = 'www'

	return sd + '.'


class NetworkClient:
	"""
	Internal API-client

	.. versionadded:: 0.1.0.dev5
	"""

	DEFAULT_TIMEOUT_SEC = 1  # 0.1

	def __init__(self, api_key=None, base_host='route4me.com'):

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

	def __get_headers(self):
		return {
			'user-agent': self.user_agent,
			'Route4Me-User-Agent': self.user_agent,
			'Accept': 'application/json',
		}

	def __get_session(self):

		s = requests.sessions.Session()
		s.max_redirects = 1
		s.verify = True
		s.headers = self.__get_headers()

		return s

	def __reqexc(self, req, timeout):
		with self.__get_session() as s:
			preq = s.prepare_request(req)
			try:
				log.debug('send request [%s] [%s]', req.method, req.url)
				return s.send(
					preq,
					timeout=timeout
				)
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
					details={
						'max_redirects': s.max_redirects,
					}
				)
				log.error(err, exc_info=True)
				raise err
			except requests.exceptions.Timeout as exc:
				err = Route4MeNetworkError(
					message='Network timeout (still no bytes received)',
					code='route4me.sdk.network.timeout',
					details={
						'timeout': timeout,
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

	def __request(self, method, subdomains, path, timeout_sec=None, **qargs):

		subdomains = _handle_subdomains(subdomains)

		# https://www.httpbin.org/get
		url = 'https://{subdomains}{base_host}/{path}'.format(
			subdomains=subdomains,
			base_host=self.base_host,
			path=path,
		)

		# payload/data settings
		payload = {}
		if qargs:
			payload.update(qargs)

		payload['api_key'] = self.api_key
		payload['format'] = 'json'

		# if (form) {
		# 	req.type("multipart/form-data")
		# 		.field(form)
		# } else {
		# 	req.type("application/json")
		# 		.send(body)
		# }

		# Timeout settings
		timeout = timeout_sec if timeout_sec is not None else self.DEFAULT_TIMEOUT_SEC

		log.debug('prepare request [%s] [%s]', method, url)
		req = requests.Request(
			method,
			url,
			params=payload,
		)
		res = self.__reqexc(req, timeout=timeout)

		# const req = request[method](apiUrl)
		# 	.redirects(1000)	// unlimited number of redirects

		# if r.status_code == requests.codes.ok:

		res.encoding = 'utf-8'
		json = res.json()
		return json

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

	def get(self, path, subdomains=None, **qargs):
		return self.__request(
			method='GET',
			subdomains=subdomains,
			path=path,
			**qargs
		)

	def post(self, path, subdomains=None, **qargs):
		return self.__request(
			method='POST',
			subdomains=subdomains,
			path=path,
			**qargs
		)

	def form(self, path, subdomains=None, **qargs):
		"""
		Posts form data as `multipart/form-data`.

		:param path str:         Path (part of URL) to API method
		:param subdomains [str]: Send request to other subdomain of the API
		:param **qargs: [description]
		:returns: API response, JSON converted to ..
		:rtype: {dict}
		"""
		return self.__request(
			method='POST',
			subdomains=subdomains,
			path=path,
			**qargs
		)
