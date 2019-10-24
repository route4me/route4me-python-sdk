# -*- coding: utf-8 -*-
# codebeat:disable[TOTAL_LOC, TOO_MANY_FUNCTIONS, TOTAL_COMPLEXITY]

import re

from .constants import (
    TRAVEL_MODE,
    OPTIMIZE, DEVICE_TYPE,
    DISTANCE_UNIT,
    ROUTE_PATH_OUTPUT,
    TRUCK_HAZARDOUS_GOODS,
    FORMAT,
)
from .exceptions import ParamValueException


class Base(object):
    """
    Base Class, with common methods.
    """

    def __init__(self, api):
        """
        Base instance
        :param api:
        :return:
        """
        self.response = None
        self.api = api
        self.data = {'parameters': {},
                     'addresses': {},
                     }
        self.params = {'api_key': api.key, }

    @staticmethod
    def check_string_type(obj):
        """
        Check if an object is string type
        :param obj:
        :return:
        """
        try:
            return isinstance(obj, basestring)
        except NameError:
            return isinstance(obj, str)

    def format(self, set_format):
        """
        Add format to params.
        :param set_format:
        :return:
        :raise: ParamValueException if set_format is not in FORMAT
        """
        if set_format in FORMAT.reverse_mapping.keys():
            self._copy_param({'format': set_format})
        else:
            raise ParamValueException('format', 'Must be CSV, SERIALIZED, XML')

    def member_id(self, member_id, target='data'):
        """
        Set member_id in params or data
        :param member_id:
        :param target:
        :return:
        :raise: ParamValueException if member_id is not Integer
        """
        if isinstance(member_id, int):
            getattr(self, '_copy_%s' % target)({'member_id': member_id})
        else:
            raise ParamValueException('member_id', 'Must be integer')

    def route_id(self, route_id):
        """
        Set route_id in params or data
        :param route_id:
        :return:
        :raise: ParamValueException if route_id is not String
        """
        if self.check_string_type(route_id):
            self._copy_param({'route_id': route_id})
        else:
            raise ParamValueException('route_id', 'Must be String')

    def address_1(self, address_1):
        """
        Set address_1 in params or data
        :param address_1:
        :return:
        :raise: ParamValueException if address_1 is not String
        """
        if self.check_string_type(address_1):
            self._copy_param({'address_1': address_1})
        else:
            raise ParamValueException('address_1', 'Must be String')

    def tx_id(self, tx_id):
        """
        Set tx_id param
        :param tx_id:
        :return:
        """
        if self.check_string_type(tx_id):
            self._copy_param({'tx_id': tx_id})
        else:
            raise ParamValueException('tx_id', 'Must be String')

    def vehicle_id(self, vehicle_id):
        """
        Set vehicle_id param
        :param vehicle_id:
        :return:
        """
        if isinstance(vehicle_id, int):
            self._copy_data({'vehicle_id': vehicle_id})
        else:
            raise ParamValueException('vehicle_id', 'Must be integer')

    def course(self, course):
        """
        Set course param
        :param course:
        :return:
        """
        if isinstance(course, int):
            self._copy_param({'course': course})
        else:
            raise ParamValueException('course', 'Must be integer')

    def speed(self, speed):
        """
        Set speed param
        :param speed:
        :return:
        """
        if isinstance(speed, int):
            self._copy_param({'speed': speed})
        else:
            raise ParamValueException('speed', 'Must be Float')

    def lat(self, lat):
        """
        Set lat param
        :param lat:
        :return:
        """
        if isinstance(lat, float):
            self._copy_param({'lat': lat})
        else:
            raise ParamValueException('lat', 'Must be Float')

    def lng(self, lng):
        """
        Set lng param
        :param lng:
        :return:
        """
        if isinstance(lng, float):
            self._copy_param({'lng': lng})
        else:
            raise ParamValueException('lng', 'Must be Float')

    def cached_lat(self, lat):
        """
        Set lat param
        :param lat:
        :return:
        """
        if isinstance(lat, float):
            self._copy_param({'lat': lat})
        else:
            raise ParamValueException('lat', 'Must be Float')

    def cached_lng(self, lng):
        """
        Set lng param
        :param lng:
        :return:
        """
        if isinstance(lng, float):
            self._copy_param({'lng': lng})
        else:
            raise ParamValueException('lng', 'Must be Float')

    def altitude(self, altitude):
        """
        Set altitude param
        :param altitude:
        :return:
        """
        if isinstance(altitude, float):
            self._copy_param({'altitude': altitude})
        else:
            raise ParamValueException('altitude', 'Must be Float')

    def device_guid(self, device_guid):
        """
        Set device_guid param
        :param device_guid:
        :return:
        """
        if self.check_string_type(device_guid):
            self._copy_param({'device_guid': device_guid})
        else:
            raise ParamValueException('device_guid', 'Must be String')

    def app_version(self, app_version):
        """
        Set app_version param
        :param app_version:
        :return:
        """
        if self.check_string_type(app_version):
            self._copy_param({'app_version': app_version})
        else:
            raise ParamValueException('app_version', 'Must be String')

    def device_timestamp(self, device_timestamp):
        """
        Set device_timestamp param. Must be a valid date time
        with this format:  YYYY-MM-DD HH:MM:SS
        :param device_timestamp:
        :return:
        """
        pattern = r'^(\d{4})-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$'
        if re.match(pattern, device_timestamp):
            self._copy_param({'device_timestamp': device_timestamp})
        else:
            raise ParamValueException('device_timestamp',
                                      'Must be YYYY-MM-DD HH:MM:SS format')

    def algorithm_type(self, algorithm_type):
        """
        Set algorithm_type. Choices are:
        TSP, VRP, CVRP_TW_SD
        CVRP_TW_MD, TSP_TW,
        TSP_TW_CR and BBCVRP
        :param: algorithm_type:
        :return:
        """
        VALID = [1, 2, 3, 4, 5, 6, 7, 100, 101, ]
        if algorithm_type in VALID:
            self._copy_data({'algorithm_type': algorithm_type})
        else:
            raise ParamValueException('algorithm_type',
                                      'Must be ALGORITHM_TYPE: '
                                      'TSP(1), VRP(2), CVRP_TW_SD(3), '
                                      'CVRP_TW_MD(4), TSP_TW(5), '
                                      'TSP_TW_CR(6), BBCVRP(7), '
                                      'NO OPTIMIZATION(100) or '
                                      'LEGACY_DISTRIBUTED(101)')

    def route_name(self, route_name):
        """
        Set route_name param
        :param route_name:
        :return:
        """
        if self.check_string_type(route_name):
            self._copy_data({'route_name': route_name})
        else:
            raise ParamValueException('route_name', 'Must be String')

    def optimization_problem_id(self, optimization_problem_id):
        """
        Set optimization_problem_id param
        :param optimization_problem_id:
        :return:
        """
        if self.check_string_type(optimization_problem_id):
            self._copy_param({'optimization_problem_id':
                              optimization_problem_id})
        else:
            raise ParamValueException('optimization_problem_id',
                                      'Must be String')

    def optimized_callback_url(self, optimized_callback_url):
        """
        Set optimized_callback_url param
        :param optimized_callback_url:
        :return:
        """
        if self.check_string_type(optimized_callback_url):
            self._copy_param({'optimized_callback_url': optimized_callback_url})
        else:
            raise ParamValueException('optimized_callback_url',
                                      'Must be String')

    def remote_ip(self, remote_ip):
        """
        Set remote_ip param
        :param remote_ip:
        :return:
        """
        if isinstance(remote_ip, int):
            self._copy_data({'remote_ip': remote_ip})
        else:
            raise ParamValueException('remote_ip', 'Must be integer')

    def travel_mode(self, travel_mode):
        """
        Set travel_mode. Options are:
        DRIVING, WALKING, TRUCKING
        :param travel_mode:
        :return:
        """
        if travel_mode in TRAVEL_MODE.reverse_mapping.keys():
            self._copy_data({'travel_mode': travel_mode})
        else:
            raise ParamValueException('travel_mode', 'Must be DRIVING, '
                                                     'WALKING, TRUCKING')

    def optimize(self, optimize):
        """
        Set optimize param
        :param optimize:
        :return:
        """
        if optimize in OPTIMIZE.reverse_mapping.keys():
            self._copy_data({'optimize': optimize})
        else:
            raise ParamValueException('optimize', 'Must be DISTANCE, TIME, '
                                                  'TIME_WITH_TRAFFIC')

    def distance_unit(self, distance_unit):
        """
        Set distance_unit param
        :param distance_unit:
        :return:
        """
        if distance_unit in DISTANCE_UNIT.reverse_mapping.keys():
            self._copy_data({'distance_unit': distance_unit})
        else:
            raise ParamValueException('distance_unit', 'Must be MI or KM')

    def device_type(self, device_type, target='data'):
        """
        Set device_type. Options are: WEB, IPHONE, IPAD, ANDROID_PHONE,
        ANDROID_TABLET
        :param device_type:
        :param target:
        :return:
        """
        if device_type in DEVICE_TYPE.reverse_mapping.keys():
            getattr(self, '_copy_%s' % target)({'device_type': device_type})
        else:
            raise ParamValueException('device_type', 'Must be WEB, IPHONE, '
                                                     'IPAD, ANDROID_PHONE, '
                                                     'ANDROID_TABLET')

    def route_path_output(self, route_path_output):
        """
        Set device_type. Options are: WEB, IPHONE, IPAD, ANDROID_PHONE,
        ANDROID_TABLET
        :param route_path_output:
        :param target:
        :return:
        """
        if route_path_output in ROUTE_PATH_OUTPUT.reverse_mapping.keys():
            self._copy_param({'route_path_output': route_path_output})
        else:
            raise ParamValueException('route_path_output', 'Must be NONE or '
                                                           'POINTS')

    def route_time(self, route_time):
        """
        Set route_time param
        :param route_time:
        :return:
        """
        if isinstance(route_time, int):
            self._copy_data({'route_time': route_time})
        else:
            raise ParamValueException('route_time', 'Must be integer')

    def trailer_weight_t(self, trailer_weight_t):
        """
        Set trailer_weight_t param
        :param trailer_weight_t:
        :return:
        """
        if isinstance(trailer_weight_t, int):
            self._copy_data({'trailer_weight_t': trailer_weight_t})
        else:
            raise ParamValueException('trailer_weight_t',
                                      'Must be integer')

    def limited_weight_t(self, limited_weight_t):
        """
        Set limited_weight_t param
        :param limited_weight_t:
        :return:
        """
        if isinstance(limited_weight_t, float) or \
           isinstance(limited_weight_t, int):
            self._copy_data({'limited_weight_t': limited_weight_t})
        else:
            raise ParamValueException('limited_weight_t',
                                      'Must be integer')

    def weight_per_axle_t(self, weight_per_axle_t):
        """
        Set weight_per_axle_t param
        :param weight_per_axle_t:
        :return:
        """
        if isinstance(weight_per_axle_t, float) or \
           isinstance(weight_per_axle_t, int):
            self._copy_data({'weight_per_axle_t': weight_per_axle_t})
        else:
            raise ParamValueException('weight_per_axle_t',
                                      'Must be integer')

    def truck_height(self, truck_height):
        """
        Set truck_height param
        :param truck_height:
        :return:
        """
        if isinstance(truck_height, float) or \
           isinstance(truck_height, int):
            self._copy_data({'truck_height': truck_height})
        else:
            raise ParamValueException('truck_height', 'Must be integer')

    def truck_width(self, truck_width):
        """
        Set truck_width param
        :param truck_width:
        :return:
        """
        if isinstance(truck_width, float) or \
           isinstance(truck_width, int):
            self._copy_data({'truck_width': truck_width})
        else:
            raise ParamValueException('truck_width', 'Must be integer')

    def truck_length(self, truck_length):
        """
        Set truck_length param
        :param truck_length:
        :return:
        """
        if isinstance(truck_length, float) or \
           isinstance(truck_length, int):
            self._copy_data({'truck_length': truck_length})
        else:
            raise ParamValueException('truck_length', 'Must be integer')

    def min_tour_size(self, min_tour_size):
        """
        Set min_tour_size param
        :param min_tour_size:
        :return:
        """
        if isinstance(min_tour_size, int):
            self._copy_data({'min_tour_size': min_tour_size})
        else:
            raise ParamValueException('min_tour_size',
                                      'Must be integer')

    def route_date(self, route_date):
        """
        Set route_date param
        :param route_date:
        :return:
        """
        if isinstance(route_date, int):
            self._copy_data({'route_date': route_date})
        else:
            raise ParamValueException('route_date', 'Must be integer')

    def route_max_duration(self, route_max_duration):
        """
        Set route_max_duration param
        :param route_max_duration:
        :return:
        """
        if isinstance(route_max_duration, int):
            self._copy_data({'route_max_duration': route_max_duration})
        else:
            raise ParamValueException('route_max_duration',
                                      'Must be integer')

    def vehicle_capacity(self, vehicle_capacity):
        """
        Set vehicle_capacity param
        :param vehicle_capacity:
        :return:
        """
        if isinstance(vehicle_capacity, int):
            self._copy_data({'vehicle_capacity': vehicle_capacity})
        else:
            raise ParamValueException('vehicle_capacity',
                                      'Must be integer')

    def parts(self, parts):
        """
        Set parts param
        :param parts:
        :return:
        """
        if isinstance(parts, int):
            self._copy_data({'parts': parts})
        else:
            raise ParamValueException('parts',
                                      'Must be integer')

    def limit(self, limit):
        """
        Set limit param
        :param limit:
        :return:
        """
        if isinstance(limit, int):
            self._copy_param({'limit': limit})
        else:
            raise ParamValueException('limit',
                                      'Must be integer')

    def offset(self, offset):
        """
        Set offset param
        :param offset:
        :return:
        """
        if isinstance(offset, int):
            self._copy_param({'offset': offset})
        else:
            raise ParamValueException('offset',
                                      'Must be integer')

    def vehicle_max_distance_mi(self, vehicle_max_distance_mi):
        """
        Set vehicle_max_distance_mi
        :param vehicle_max_distance_mi:
        :return:
        """
        if isinstance(vehicle_max_distance_mi, int):
            self._copy_data({'vehicle_max_distance_mi':
                             vehicle_max_distance_mi})
        else:
            raise ParamValueException('vehicle_max_distance_mi',
                                      'Must be integer')

    def max_tour_size(self, max_tour_size):
        """
        Set max_tour_size
        :param max_tour_size:
        :return:
        """
        if isinstance(max_tour_size, int):
            self._copy_data({'max_tour_size':
                             max_tour_size})
        else:
            raise ParamValueException('max_tour_size',
                                      'Must be integer')

    def route_email(self, route_email):
        """
        Set route_email param
        :param route_email:
        :return:
        """
        if self.check_string_type(route_email):
            self._copy_data({'route_email': route_email})
        else:
            raise ParamValueException('route_email', 'Must be String')

    def metric(self, metric):
        """
        Set metric Param. Must be:
        ROUTE4ME_METRIC_EUCLIDEA
        ROUTE4ME_METRIC_MANHATTA
        ROUTE4ME_METRIC_GEODESIC
        ROUTE4ME_METRIC_MATRIX
        ROUTE4ME_METRIC_EXACT_2D
        :param metric:
        :return:
        """
        if 1 <= metric <= 7:
            self._copy_data({'metric': metric})
        else:
            raise ParamValueException('metric',
                                      'Must be METRIC: '
                                      'ROUTE4ME_METRIC_EUCLIDEAN , '
                                      'ROUTE4ME_METRIC_MANHATTAN, '
                                      'ROUTE4ME_METRIC_GEODESIC'
                                      'ROUTE4ME_METRIC_MATRIX'
                                      'ROUTE4ME_METRIC_EXACT_2D')

    def store_route(self, store_route):
        """
        Set store_route param
        :param store_route:
        :return:
        """
        if 0 <= store_route <= 1:
            self._copy_data({'store_route': store_route})
        else:
            raise ParamValueException('store_route', 'Must be 0 or 1')

    def lock_last(self, lock_last):
        """
        Set lock_last param
        :param lock_last:
        :return:
        """
        if 0 <= lock_last <= 1:
            self._copy_data({'lock_last': lock_last})
        else:
            raise ParamValueException('lock_last', 'Must be 0 or 1')

    def disable_optimization(self, disable_optimization):
        """
        Set disable_optimization param
        :param disable_optimization:
        :return:
        """
        if 0 <= disable_optimization <= 1:
            self._copy_data({'disable_optimization': disable_optimization})
        else:
            raise ParamValueException('disable_optimization', 'Must be 0 or 1')

    def shared_publicly(self, shared_publicly):
        """
        Set shared_publicly param
        :param shared_publicly:
        :return:
        """
        if 0 <= shared_publicly <= 1:
            self._copy_data({'shared_publicly': shared_publicly})
        else:
            raise ParamValueException('shared_publicly', 'Must be 0 or 1')

    def reoptimize(self, reoptimize):
        """
        Set reoptimize param
        :param reoptimize:
        :return:
        """
        if 0 <= reoptimize <= 1:
            self._copy_param({'reoptimize': reoptimize})
        else:
            raise ParamValueException('reoptimize', 'Must be 0 or 1')

    def share_route(self, share_route):
        """
        Set share_route param
        :param share_route:
        :return:
        """
        if 0 <= share_route <= 1:
            self._copy_data({'share_route': share_route})
        else:
            raise ParamValueException('share_route', 'Must be 0 or 1')

    def rt(self, rt):
        """
        Set rt param.
        :param rt:
        :return:
        """
        if 0 <= rt <= 1:
            self._copy_data({'rt': rt})
        else:
            raise ParamValueException('rt', 'Must be 0 or 1')

    def has_trailer(self, has_trailer):
        """
        Set has_trailer param.
        :param has_trailer:
        :return:
        """
        if 0 <= has_trailer <= 1:
            self._copy_data({'has_trailer': has_trailer})
        else:
            raise ParamValueException('has_trailer', 'Must be 0 or 1')

    def optimization_quality(self, optimization_quality):
        """
        Set optimization_quality param.
        :param optimization_quality:
        :return:
        """
        if 1 <= optimization_quality <= 3:
            self._copy_data({'optimization_quality': optimization_quality})
        else:
            raise ParamValueException('optimization_quality',
                                      'Must be between 1 to 3')

    def directions(self, directions):
        """
        Set directions param.
        :param directions:
        :return:
        """
        if 0 <= directions <= 1:
            self._copy_param({'directions': directions})
        else:
            raise ParamValueException('directions', 'Must be 0 or 1')

    def device_tracking_history(self, device_tracking_history):
        """
        Set device_tracking_history param.
        :param device_tracking_history:
        :return:
        """
        if 0 <= device_tracking_history <= 1:
            self._copy_param({
                'device_tracking_history': device_tracking_history
            })
        else:
            raise ParamValueException('device_tracking_history',
                                      'Must be 0 or 1')

    def uturn(self, uturn_type):
        """
        Set uturn_type. Choices are:
        UTURN_DEPART_SHORTEST or
        UTURN_DEPART_TO_RIGHT
        :param: uturn_type:
        :return:
        """
        if 1 <= uturn_type <= 2:
            self._copy_data({'uturn': uturn_type})
        else:
            raise ParamValueException('uturn',
                                      'Must be : '
                                      'UTURN_DEPART_SHORTEST or '
                                      'UTURN_DEPART_TO_RIGHT')

    def leftturn(self, left_turn_type):
        """
        Set leftturn. Choices are:
        LEFTTURN_ALLOW or
        LEFTTURN_FORBID or
        LEFTTURN_MULTIAPPROACH
        :param: leftturn:
        :return:
        """
        if 1 <= left_turn_type <= 3:
            self._copy_data({'leftturn': left_turn_type})
        else:
            raise ParamValueException('leftturn',
                                      'Must be : '
                                      'LEFTTURN_ALLOW or '
                                      'LEFTTURN_FORBID or '
                                      'LEFTTURN_MULTIAPPROACH')

    def dm(self, dm):
        """
        Set dm. Choices are:
        R4M_PROPRIETARY_ROUTING or
        R4M_TRAFFIC_ENGINE or
        TRUCKING
        :param: dm:
        :return:
        """
        if dm in [1, 3, 6]:
            self._copy_data({'dm': dm})
        else:
            raise ParamValueException(
                'dm',
                'Must be : '
                'R4M_PROPRIETARY_ROUTING or '
                'R4M_TRAFFIC_ENGINE or '
                'TRUCKING'
            )

    def dirm(self, dirm):
        """
        Set dirm. Choices are:
        R4M_PROPRIETARY_INTERNAL_NAVIGATION_SYSTEM or
        TRUCKING
        :param: dirm:
        :return:
        """
        if dirm in [1, 3]:
            self._copy_data({'dirm': dirm})
        else:
            raise ParamValueException(
                'dirm',
                'Must be : '
                'R4M_PROPRIETARY_INTERNAL_NAVIGATION_SYSTEM or'
                'TRUCKING'
            )

    def _copy_data(self, params):
        """
        Copy params to data
        :param params:
        :return:
        """
        self.data['parameters'].update(params)

    def _copy_param(self, params):
        """
        Copy params to params
        :param params:
        :return:
        """
        self.params.update(params)

    def get_params(self):
        """
        Get params
        :return:  params
        """
        return self.params

    def required_params(self, requirements=[]):
        """
        Check if required params are set
        :param requirements:
        :return:
        """
        return set(requirements).issubset(set(self.params.keys()))

    @staticmethod
    def check_required_params(params, requirements=[]):
        """
        Check if required params are set
        :param requirements:
        :return:
        """
        return set(requirements).issubset(set(params.keys()))

    def validate_params(self, **kwargs):
        """
        Validate params
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            try:
                self.__getattribute__(k)(v)
            except ParamValueException as e:
                raise e
            except AttributeError:
                raise ParamValueException(k, 'Not supported')
        return True

    def add(self, params={}, data={}):
        """
        Add params and data
        :param params:
        :param data:
        :return:
        """
        self.validate_params(**params)
        self.validate_params(**data)
        self.data.update(data)
        self.params.update(params)

    def truck_hazardous_goods(self, hazardous_goods):
        """
        Set truck_hazardous_goods param
        :param truck_hazardous_goods:
        :return:
        """
        if hazardous_goods in TRUCK_HAZARDOUS_GOODS.reverse_mapping.keys():
            self._copy_data({'truck_hazardous_goods': hazardous_goods})
        else:
            raise ParamValueException('truck_hazardous_goods',
                                      'Must be MI or KM')

# codebeat:enable[TOTAL_LOC, TOO_MANY_FUNCTIONS, TOTAL_COMPLEXITY]
