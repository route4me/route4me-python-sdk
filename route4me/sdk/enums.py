# -*- coding: utf-8 -*-

from enum import Enum


class AlgorithmTypeEnum(Enum):
	"""
	The algorithm type to be used.
	"""

	TSP = 1
	"""
	TSP

	.. todo::
		add clear and understandable description
	"""

	VRP = 2
	"""
	VRP

	.. todo::
		add clear and understandable description
	"""

	CVRP_TW_SD = 3
	"""
	CVRP_TW_SD

	.. todo::
		add clear and understandable description
	"""

	CVRP_TW_MD = 4
	"""
	CVRP_TW_MD

	.. todo::
		add clear and understandable description
	"""

	TSP_TW = 5
	"""
	TSP_TW

	.. todo::
		add clear and understandable description
	"""

	TSP_TW_CR = 6
	"""
	TSP_TW_CR

	.. todo::
		add clear and understandable description
	"""

	BBCVRP = 7
	"""
	BBCVRP

	.. todo::
		add clear and understandable description
	"""

	ALG_LEGACY_DISTRIBUTED = 101
	"""
	ALG_LEGACY_DISTRIBUTED

	.. todo::
		add clear and understandable description
	"""

	ALG_NONE = 100
	"""
	ALG_NONE

	.. todo::
		add clear and understandable description
	"""


class OptimizationFactorEnum(Enum):
	"""
	The driving directions can be generated biased for this selection. This
	has no impact on route sequencing.

	.. note::

		In Route4Me API this enum also known as ``optimize``

	"""

	#: Optimize by distance
	DISTANCE = 'Distance'

	#: Optimize by time
	TIME = 'Time'

	#: Optimize by time and traffic
	TIME_TRAFFIC = 'timeWithTraffic'


class DistanceUnitEnum(Enum):
	"""
	:class:`~.Optimization` problem can be at one state at any given time
	"""

	#: Miles
	MILE = 'mi'

	#: Kilometers
	KILOMETER = 'km'


class OptimizationStateEnum(Enum):
	"""
	The distance measurement unit
	"""

	#: Initial
	INITIAL = 1

	#: Matrix Processing
	MATRIX_PROCESSING = 2

	#: Optimizing
	OPTIMIZING = 3

	#: Optimized
	OPTIMIZED = 4

	#: Error
	ERROR = 5

	#: Computing Directions
	COMPUTING_DIRECTIONS = 6


class OptimizationQualityEnum(Enum):
	"""
	Optimization Quality
	"""

	#: Generate Optimized Routes As Quickly as Possible
	FAST = 1

	#: Generate Routes That Look Better On A Map
	MEDIUM = 2

	#: Generate The Shortest And Quickest Possible Routes
	BEST = 3


class DeviceTypeEnum(Enum):
	"""
	Device Type

	The type of the device that is creating this route
	"""

	#: Web
	WEB = "web"

	#: IPhone
	IPHONE = "iphone"

	#: IPad
	IPAD = "ipad"

	#: Android phone
	ANDROID_PHONE = "android_phone"

	#: Android tablet
	ANDROID_TABLET = "android_tablet"


class TravelModeEnum(Enum):
	"""
	Travel Mode

	The mode of travel that the directions should be optimized for
	"""

	#: Driving
	DRIVING = 'Driving'

	#: Walking
	WALKING = 'Walking'

	#: Trucking
	TRUCKING = 'Trucking'

	#: Cycling
	CYCLING = 'Cycling'

	#: Transit
	TRANSIT = 'Transit'


class RouteMetricEnum(Enum):
	"""
	Metric
	"""

	#: Euclidean
	EUCLIDEAN = 1

	#: Manhattan
	MANHATTAN = 2

	#: Geodesic
	GEODESIC = 3

	#: Matrix
	MATRIX = 4

	#: Exact 2d
	EXACT2D = 5


# TYPE_OF_MATRIX = enum(R4M_PROPRIETARY_ROUTING=1,
#                       R4M_TRAFFIC_ENGINE=3,
#                       TRUCKING=6)

# DIRECTIONS_METHOD = enum(R4M_PROPRIETARY_INTERNAL_NAVIGATION_SYSTEM=1,
#                          TRUCKING=3)

# AVOID = enum(HIGHWAYS='Highways',
#              TOLLS='Tolls',
#              MINIMIZE_HIGHWAYS='minimizeHighways',
#              MINIMIZE_TOLLS='minimizeTolls',
#              NONE='')


# FORMAT = enum(CSV='csv',
#               SERIALIZED='serialized',
#               XML='xml',
#               JSON='json')


# ROUTE_PATH_OUTPUT = enum(NONE='None',
#                          POINTS='Points')

# UTURN = auto_enum('UTURN_DEPART_SHORTEST',
#                   'UTURN_DEPART_TO_RIGHT')

# LEFT_TURN = auto_enum('LEFTTURN_ALLOW',
#                       'LEFTTURN_FORBID',
#                       'LEFTTURN_MULTIAPPROACH')

# TRUCK_HAZARDOUS_GOODS = enum(NONE='',
#                              EXPLOSIVE='explosive',
#                              GAS='gas',
#                              FLAMMABLE='flammable',
#                              COMBUSTIBLE='combustible',
#                              ORGANIC='organic',
#                              POISON='poison',
#                              RADIOACTIVE='radioActive',
#                              CORROSIVE='corrosive',
#                              POISONOUSINHALATION='poisonousInhalation',
#                              HARMFULTOWATER='harmfulToWater',
#                              OTHER='other',
#                              ALLHAZARDOUSGOODS='allHazardousGoods')

# TERRITORY_TYPE = enum(CIRCLE='circle',
#                       POLY='poly',
#                       RECT='rect', )
