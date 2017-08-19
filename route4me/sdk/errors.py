# -*- coding: utf-8 -*-


class Route4MeError(Exception):
	"""
	Base (abstract) Exception

	@private
	"""
	def __init__(
		self,
		message,
		code='route4me.sdk.other',
		details=None,
		inner=None,
	):
		super(Route4MeError, self).__init__(message)

		self.code = code

		if details is not None:
			assert isinstance(details, dict)

		self.details = details
		self.inner = inner

	def get_message(self):
		return super().__str__()

	def __str__(self):

		s = '{tp}: [{code}] {message}'.format(
			tp=type(self).__name__,
			code=self.code,
			message=self.get_message(),
		)
		return s


class Route4MeNetworkError(Route4MeError):
	pass


class Route4MeValidationError(Route4MeError):
	"""
	Route4Me Validation error.

	Variable has invalid format/data
	"""
	pass
