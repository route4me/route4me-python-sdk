# -*- coding: utf-8 -*-

# reimport enums for convenience:
from ..enums import AlgorithmTypeEnum
from ..enums import OptimizationStateEnum
from ..enums import RouteMetricEnum

from route4me.sdk._internals.utils import dict_property
from route4me.sdk._internals.utils import dict_enum_property


class BaseModel(dict):
	pass


class Optimization(BaseModel):
	"""
	Optimization problem (or simple *Optimization*)
	"""

	def __init__(self, raw=None):
		"""
		Create instance **LOCALLY**.

		Use :meth:`~route4me.sdk.resources.optimizations.Optimizations.create`
		to create new Optimization Problem in the Route4Me API

		:param raw: Raw values for new optimization, example: \
			`create optimization <https://route4me.io/docs/#create-an-optimization>`_, \
			defaults to None
		:type raw: dict, optional
		"""
		if raw is None:
			raw = {
				'parameters': {},
				'links': {},
			}
		super(BaseModel, self).__init__(raw)

	@property
	def ID(self):
		return self.get('optimization_problem_id')

	@dict_enum_property('parameters.algorithm_type', AlgorithmTypeEnum)
	def algorithm_type(self, value):
		"""
		The algorithm type to be used

		<AUTO>
		"""
		return value

	@dict_enum_property('state', OptimizationStateEnum)
	def state(self, value):
		"""
		The current state of the optimization

		<AUTO>
		"""
		return value

	@dict_enum_property('parameters.metric', RouteMetricEnum)
	def metric(self, value):
		"""
		Metric

		<AUTO>
		"""
		return value

	@dict_property('parameters.route_name', str)
	def name(self, value):
		"""
		The name of this optimization problem. This name will be accessible in
		the search API, and also will be displayed on the mobile device of
		a user

		<AUTO>
		"""
		return value

	@dict_property('parameters.parts', int)
	def parts(self, value):
		"""
		Legacy feature which permits a user to request an example number of
		optimized routes

		<AUTO>
		"""
		return value

	@dict_property('parameters.disable_optimization', bool)
	def disable_optimization(self, value):
		"""
		By disabling optimization, the route optimization engine will not
		resequence stops in your optimization problem

		<AUTO>
		"""
		return value

	# 	'travel_mode': 'Driving',
	# 	'store_route': 0,
	# 	'device_type': 'vehicle',
	# 	'optimize': 'Time',
	# 	'route_max_duration': 23 * 3600,
	# 'rt': round_trip,
	# 'member_id': member_id,
	# 'device_id': device_id,
	# 'route_time': route_timestamp,
	# 'optimization_quality': None,

	# addresses,
