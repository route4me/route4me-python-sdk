# -*- coding: utf-8 -*-


class Route4MeError(Exception):
	"""
	Base (abstract) error-class
	"""
	def __init__(
		self,
		message,
		code='route4me.sdk.other',
		details=None,
		inner=None,
	):
		super(Route4MeError, self).__init__(message)

		#: Unique error code. Helps to distinguish different errors.
		#:
		#: :type: str
		self.code = code

		if details is not None:
			assert isinstance(details, dict)

		#: Some error details
		#:
		#: :type: dict
		self.details = details

		#: Internal exception that describes an original error.
		#:
		#: :type: Exception
		self.inner = inner

	def get_message(self):
		return super(Route4MeError, self).__str__()

	def __str__(self):

		s = '{tp}: [{code}] {message}'.format(
			tp=type(self).__name__,
			code=self.code,
			message=self.get_message(),
		)
		return s


class Route4MeNetworkError(Route4MeError):
	"""
	Route4Me SDK network/connection errors.

	Occurs on:

	- invalid SSL
	- network timeout
	- wrong redirects (Route4Me API doesn't send redirect responses)
	- no connection, no path to route (DNS)

	More details could be observed using :py:attr:`~.Route4MeError.code` and
	:py:attr:`~.Route4MeError.details`
	"""
	pass


class Route4MeApiError(Route4MeError):
	"""
	Error on Route4Me SDK

	.. todo::
		Make this exception more detailed

	"""
	def __init__(
		self,
		message,
		code='route4me.sdk.other',
		details=None,
		inner=None,

		method=None,
		url=None,
	):
		super(Route4MeApiError, self).__init__(
			message,
			code,
			details,
			inner
		)

		self.method = method
		self.url = url


class Route4MeValidationError(Route4MeError):
	"""
	Route4Me Validation error.

	Variable has invalid format/data
	"""
	pass


class Route4MeEntityNotFoundError(Route4MeError):
	"""
	Requested entity was not found on Route4Me
	"""
	pass
