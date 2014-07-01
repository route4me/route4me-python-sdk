def enum(**enums):
    """
    Create enums with custom values to help user set their params
    :param enums:
    :return:
    """
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)


def auto_enum(*sequential, **named):
    """
    Create enum
    :param sequential:
    :param named:
    :return:
    """
    enums = dict(zip(sequential, range(1, len(sequential)+1)), **named)
    return enum(**enums)


ALGORITHM_TYPE = auto_enum('TSP', 'VRP', 'CVRP_TW_SD', 'CVRP_TW_MD', 'TSP_TW',
                           'TSP_TW_CR', 'BBCVRP')

TRAVEL_MODE = enum(DRIVING='Driving', WALKING='Walking', TRUCKING='Trucking')

DISTANCE_UNIT = enum(MI='mi', KM='km')

AVOID = enum(HIGHWAYS='Highways', TOLLS='Tolls',
             MINIMIZE_HIGHWAYS='minimizeHighways',
             MINIMIZE_TOLLS='minimizeTolls',
             NONE='')

OPTIMIZE = enum(DISTANCE='Distance', TIME='Time',
                TIME_WITH_TRAFFIC='timeWithTraffic')

METRIC = auto_enum('ROUTE4ME_METRIC_EUCLIDEAN', 'ROUTE4ME_METRIC_MANHATTAN',
                   'ROUTE4ME_METRIC_GEODESIC', 'ROUTE4ME_METRIC_MATRIX',
                   'ROUTE4ME_METRIC_EXACT_2D',)

DEVICE_TYPE = enum(WEB="web", IPHONE="iphone", IPAD="ipad",
                   ANDROID_PHONE="android_phone",
                   ANDROID_TABLET="android_tablet")

FORMAT = enum(CSV='csv', SERIALIZED='serialized', XML='xml')

OPTIMIZATION_STATE = auto_enum('OPTIMIZATION_STATE_INITIAL',
                          'OPTIMIZATION_STATE_MATRIX_PROCESSING',
                          'OPTIMIZATION_STATE_OPTIMIZING',
                          'OPTIMIZATION_STATE_OPTIMIZED',
                          'OPTIMIZATION_STATE_ERROR',
                          'OPTIMIZATION_STATE_COMPUTING_DIRECTIONS',)

ROUTE_PATH_OUTPUT = enum(NONE='None', POINTS='Points')