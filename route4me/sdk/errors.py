# -*- coding: utf-8 -*-


class Route4MeError(Exception):
	"""
	Base (abstract) Exception
	"""
	def __init__(
		self,
		message,
		code='route4me.sdk.other',
		details=None,
		inner=None,
	):
		"""
		Constructor.

		Creates a new instance of Route4MeError.

		:param message: Error message
		:type message: str
		"""

		super(Route4MeError, self).__init__(message)

		self.code = code
		"""
		Unique error code. Helps to distinguish different errors.

		:type: str
		"""

		if details is not None:
			assert isinstance(details, dict)

		self.details = details
		"""
		Some error details

		:type: dict
		"""

		self.inner = inner
		"""
		Internal exception that describes an original error.

		:type: Exception
		"""
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


class Route4MeValidationError(Route4MeError):
	"""
	Route4Me Validation error.

	Variable has invalid format/data
	"""
	pass
