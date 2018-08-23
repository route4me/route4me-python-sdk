# -*- coding: utf-8 -*-

from six import iteritems


def enum(**enums):
    """
    Create enums with custom values to help user set their params
    :param enums:
    :return:
    """
    reverse = dict((value, key) for key, value in iteritems(enums))
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)


def auto_enum(*sequential, **named):
    """
    Create enum
    :param sequential:
    :param named:
    :return:
    """
    enums = dict(zip(sequential, range(1, len(sequential) + 1)), **named)
    return enum(**enums)


TYPE_OF_MATRIX = enum(R4M_PROPRIETARY_ROUTING=1,
                      R4M_TRAFFIC_ENGINE=3,
                      TRUCKING=6)

DIRECTIONS_METHOD = enum(R4M_PROPRIETARY_INTERNAL_NAVIGATION_SYSTEM=1,
                         TRUCKING=3)

ALGORITHM_TYPE = enum(TSP=1,
                      VRP=2,
                      CVRP_TW_SD=3,
                      CVRP_TW_MD=4,
                      TSP_TW=5,
                      TSP_TW_CR=6,
                      BBCVRP=7,
                      ALG_LEGACY_DISTRIBUTED=101,
                      ALG_NONE=100)

TRAVEL_MODE = enum(DRIVING='Driving',
                   WALKING='Walking',
                   TRUCKING='Trucking')

DISTANCE_UNIT = enum(MI='mi',
                     KM='km')

AVOID = enum(HIGHWAYS='Highways',
             TOLLS='Tolls',
             MINIMIZE_HIGHWAYS='minimizeHighways',
             MINIMIZE_TOLLS='minimizeTolls',
             NONE='')

OPTIMIZE = enum(DISTANCE='Distance',
                TIME='Time',
                TIME_WITH_TRAFFIC='timeWithTraffic')

METRIC = auto_enum('ROUTE4ME_METRIC_EUCLIDEAN',
                   'ROUTE4ME_METRIC_MANHATTAN',
                   'ROUTE4ME_METRIC_GEODESIC',
                   'ROUTE4ME_METRIC_MATRIX',
                   'ROUTE4ME_METRIC_EXACT_2D', )

DEVICE_TYPE = enum(WEB="web",
                   IPHONE="iphone",
                   IPAD="ipad",
                   ANDROID_PHONE="android_phone",
                   ANDROID_TABLET="android_tablet")

FORMAT = enum(CSV='csv',
              SERIALIZED='serialized',
              XML='xml',
              JSON='json')

OPTIMIZATION_STATE = auto_enum('OPTIMIZATION_STATE_INITIAL',
                               'OPTIMIZATION_STATE_MATRIX_PROCESSING',
                               'OPTIMIZATION_STATE_OPTIMIZING',
                               'OPTIMIZATION_STATE_OPTIMIZED',
                               'OPTIMIZATION_STATE_ERROR',
                               'OPTIMIZATION_STATE_COMPUTING_DIRECTIONS', )

ROUTE_PATH_OUTPUT = enum(NONE='None',
                         POINTS='Points')

UTURN = auto_enum('UTURN_DEPART_SHORTEST',
                  'UTURN_DEPART_TO_RIGHT')

LEFT_TURN = auto_enum('LEFTTURN_ALLOW',
                      'LEFTTURN_FORBID',
                      'LEFTTURN_MULTIAPPROACH')

TRUCK_HAZARDOUS_GOODS = enum(NONE='',
                             EXPLOSIVE='explosive',
                             GAS='gas',
                             FLAMMABLE='flammable',
                             COMBUSTIBLE='combustible',
                             ORGANIC='organic',
                             POISON='poison',
                             RADIOACTIVE='radioActive',
                             CORROSIVE='corrosive',
                             POISONOUSINHALATION='poisonousInhalation',
                             HARMFULTOWATER='harmfulToWater',
                             OTHER='other',
                             ALLHAZARDOUSGOODS='allHazardousGoods')

TERRITORY_TYPE = enum(CIRCLE='circle',
                      POLY='poly',
                      RECT='rect', )
