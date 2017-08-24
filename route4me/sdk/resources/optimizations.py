# -*- coding: utf-8 -*-

"""
An Optimization Problem refers to a collection of addresses that need to be
visited.

The optimization problem takes into consideration all of the addresses that
need to be visited and all the constraints associated with each address and
depot.

It is preferable to create an optimization problem with as many orders in it
as possible, so that the optimization engine is able to consider the entire
problem set.

This is different from a :class:`~route4me.sdk.resources.routes.Route`, which
is a sequence of addresses that need to be visited by a single vehicle and
driver in a fixed time period. Solving an Optimization Problem results in
a number of routes. (Possibly recurring in the future)

.. seealso:: https://route4me.io/docs/#optimizations

"""

from .._net import NetworkClient
from ..models import Optimization


class Optimizations:
	"""
	Optimizations resource
	"""

	def __init__(self, api_key=None, _network_client=None):
		nc = _network_client
		if nc is None:
			nc = NetworkClient(api_key)
		self.__nc = nc

	def create(
		self,
		optimization_data,
		optimized_callback_url=None,
	):
		"""
		Create a new optimization through the Route4Me API

		You could pass any valid URL as :paramref:`optimized_callback_url`
		parameter.

		The callback URL is a URL that gets called when the optimization is
		solved, or if there is an error. The callback is called with a
		``POST`` request. The POST data sent is:

		- ``timestamp`` (seconds)
		- ``optimization_problem_id``
		- ``state`` (id  of the optimization state)

		The state is a value from the enumeration
		:class:`route4me.sdk.enums.OptimizationStateEnum`

		:param optimization_data: Optimization data
		:type optimization_data: ~route4me.sdk.models.Optimization
		:param optimized_callback_url: *Optimization done* callback URL
		:type optimized_callback_url: str or None
		:returns: New optimization
		:rtype: ~route4me.sdk.models.Optimization
		"""

		query = None
		if optimized_callback_url:
			query = {
				'optimized_callback_url': str(optimized_callback_url),
			}

		print(self.__nc)

		res = self.__nc.post(
			'/api.v4/optimization_problem.php',
			subdomain='www',
			query=query,
			data=optimization_data,
		)
		return Optimization(res)

	def get(self, ID):
		"""
		GET a single optimization by ID.

		:param ID: Optimization Problem ID
		:type ID: str
		:returns: Optimization data
		:rtype: ~route4me.sdk.models.Optimization

		:raises ~route4me.sdk.errors.Route4MeEntityNotFoundError: if optimization was not found
		"""

		res = self.__nc.get(
			'/api.v4/optimization_problem.php',
			subdomain='www',
			query={
				'optimization_problem_id': str(ID),
			}
		)

		return Optimization(res)

	def list(self):
		pass

	def update(self):
		pass

	def remove(self):
		pass
