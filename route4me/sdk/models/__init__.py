# -*- coding: utf-8 -*-

# reimport enums for convenience:
from ..enums import AlgorithmTypeEnum
from ..enums import OptimizationStateEnum
from ..enums import OptimizationQualityEnum
from ..enums import OptimizationFactorEnum
from ..enums import RouteMetricEnum
from ..enums import TravelModeEnum
from ..enums import DeviceTypeEnum

from ..enums import AddressStopTypeEnum

from route4me.sdk._internals.utils import dict_property
from route4me.sdk._internals.utils import dict_enum_property


class BaseModel(dict):
	def __init__(self, raw=None):
		super(BaseModel, self).__init__(raw)

	@property
	def raw(self):
		"""
		Provides access to raw model data, as it would be sent to Route4Me API

		:getter: Get, property is readonly
		:rtype: dict
		"""
		return self


class Optimization(BaseModel):
	"""
	Optimization problem (or simple *Optimization*)

	.. seealso::
		- **schema**: https://github.com/route4me/route4me-json-schemas/blob/master/Optimization_response.dtd

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
				'parameters': {
					'store_route': True,
					'route_max_duration': 24 * 60 * 60,
				},
				'links': {},
				'addresses': []
			}
		super(Optimization, self).__init__(raw=raw)

	# ==========================================================================

	@property
	def ID(self):
		return self.raw.get('optimization_problem_id')

	@dict_property('parameters.route_name', str)
	def name(self, value):
		"""
		The name of this optimization problem. This name will be accessible in
		the search API, and also will be displayed on the mobile device of
		a user

		<AUTO>
		"""
		return value

	# ==========================================================================

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

	@dict_enum_property('parameters.optimization_quality', OptimizationQualityEnum)
	def quality(self, value):
		"""
		Optimization quality

		There are 3 types of optimization qualities that are optimizations
		goals, see :class:`~route4me.sdk.enums.OptimizationQualityEnum`

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

	@dict_enum_property('parameters.travel_mode', TravelModeEnum)
	def travel_mode(self, value):
		"""
		Travel mode

		The mode of travel that the directions should be optimized for

		<AUTO>
		"""
		return value

	@dict_enum_property('parameters.device_type', DeviceTypeEnum)
	def device_type(self, value):
		"""
		Device type

		The type of the device that is creating this Optimization Problem

		<AUTO>
		"""
		return value

	@dict_enum_property('parameters.optimize', OptimizationFactorEnum)
	def optimization_factor(self, value):
		"""
		The driving directions can be generated biased for this selection. This
		has no impact on route sequencing.

		.. note::

			In Route4Me API this enum also known as ``optimize``

		<AUTO>
		"""
		return value

	# ==========================================================================

	# @dict_property('parameters.store_route', bool)
	# def store_route(self, value):
	# 	"""
	# 	Store Route

	# 	<AUTO>
	# 	"""
	# 	return value

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

	@dict_property('parameters.route_max_duration', int)
	def route_max_duration_sec(self, value):
		"""
		Route maximum duration

		How many seconds a route can last at most.
		Default is 86400 seconds = 24 hours

		<AUTO>
		"""
		return value

	@dict_property('parameters.rt', bool)
	def round_trip(self, value):
		"""
		Round Trip

		The tour type of this route. The optimization engine changes its
		behavior for round trip routes

		.. note::

			In Route4Me API this parameter is also known as ``parameters.rt``


		<AUTO>
		"""
		return value

	@dict_property('parameters.member_id', str)
	def member_id(self, value):
		"""
		Member ID

		User ID who is assigned to this Optimization Problem

		<AUTO>
		"""
		return value

	@dict_property('parameters.device_id', str)
	def device_id(self, value):
		"""
		Device ID

		32 Character MD5 String ID of the device that was used to plan this
		route

		<AUTO>
		"""
		return value

	@dict_property('parameters.vehicle_id', str)
	def vehicle_id(self, value):
		"""
		Vehicle ID

		The unique internal id of a vehicle

		<AUTO>
		"""
		return value

	# 'route_time': route_timestamp,

	# addresses,





class Address(BaseModel):
	"""
	Single *Address*, also known as *Route Destination*

	.. seealso::
		- **api doc**: https://route4me.io/docs/#addresses
		- **schema**: https://github.com/route4me/route4me-json-schemas/blob/master/Address.dtd
	"""

	def __init__(self, raw=None):
		"""
		Create instance **LOCALLY**.

		Use :meth:`~route4me.sdk.resources.optimizations.Optimizations.add_address`
		or :meth:`~route4me.sdk.resources.routes.Routes.add_address`
		to create new Address in the Route4Me API

		:param raw: Raw values for new address, example: \
			`add address to optimization \
			<https://route4me.io/docs/#insert-an-address-into-an-optimization>`_, \
			defaults to :data:`None`
		:type raw: dict, optional
		"""
		if raw is None:
			raw = {
				'manifest': {},
				'path_to_next': [],
				'directions': [],
			}
		super(Address, self).__init__(raw=raw)

	@property
	def ID(self):
		"""
		Route Destination ID

		Internal unique address identifier

		:getter: Gets value
		:setter: Sets value
		:rtype: str
		"""
		return self.raw.get('route_destination_id')

	@dict_property('alias', str)
	def name(self, value):
		"""
		Address Alias / Address Name

		.. note::

			In Route4Me API this field is known as ``alias``

		<AUTO>
		"""
		return value

	# ==========================================================================

	@dict_enum_property('address_stop_type', AddressStopTypeEnum)
	def address_stop_type(self, value):
		"""
		Address stop type

		<AUTO>
		"""
		return value

	# ==========================================================================

	@dict_property('address', str)
	def address_string(self, value):
		"""
		The route Address Line

		.. note::

			In Route4Me API this field is known as ``address``

		<AUTO>
		"""
		return value

	@dict_property('lat', float)
	def latitude(self, value):
		"""
		Latitude

		Shoud be -90.0 ≤ lat ≤ 90

		.. note::

			In Route4Me API this field is known as ``lat``

		<AUTO>
		"""
		return value

	@dict_property('lng', float)
	def longitude(self, value):
		"""
		Longitude

		Shoud be -180.0 ≤ lng ≤ 180

		.. note::

			In Route4Me API this field is known as ``lng``

		<AUTO>
		"""
		return value

	@dict_property('sequence_no', int)
	def sequence_no(self, value):
		"""
		The sequence number for the address

		<AUTO>
		"""
		return value

	@dict_property('time', int)
	def service_time_sec(self, value):
		"""
		Service time (seconds)

		.. note::

			In Route4Me API this field is known as ``time``

		<AUTO>
		"""
		return value

	@dict_property('is_depot', bool)
	def is_depot(self, value):
		"""
		Indicates that this address is a depot

		<AUTO>
		"""
		return value

	@dict_property('geocoded', bool)
	def geocoded(self, value):
		"""
		:data:`True` means the :attr:`address_string` field was successfully geocoded

		<AUTO>
		"""
		return value

	@dict_property('failed_geocoding', bool)
	def failed_geocoding(self, value):
		"""
		:data:`True` means there was a geocoding attempt which failed. \
		:data:`False` means success or no geocoding

		<AUTO>
		"""
		return value
