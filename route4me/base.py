from route4me.utils import is_valid_datetime

from ._fields import ValidatedField
from .constants import (
    DEVICE_TYPE,
    DISTANCE_UNIT,
    FORMAT,
    OPTIMIZE,
    ROUTE_PATH_OUTPUT,
    TRAVEL_MODE,
    TRUCK_HAZARDOUS_GOODS,
)
from .exceptions import ParamValueException


class Base:
    """
    Base Class, with common methods.
    """

    # String → query params
    route_id = ValidatedField("route_id", str, "param", "Must be String")
    address_1 = ValidatedField("address_1", str, "param", "Must be String")
    tx_id = ValidatedField("tx_id", str, "param", "Must be String")
    device_guid = ValidatedField("device_guid", str, "param", "Must be String")
    app_version = ValidatedField("app_version", str, "param", "Must be String")
    optimization_problem_id = ValidatedField("optimization_problem_id", str, "param", "Must be String")
    optimized_callback_url = ValidatedField("optimized_callback_url", str, "param", "Must be String")

    # String → data body
    route_name = ValidatedField("route_name", str, "data", "Must be String")
    route_email = ValidatedField("route_email", str, "data", "Must be String")

    # Int → data body
    vehicle_id = ValidatedField("vehicle_id", int, "data", "Must be integer")
    route_time = ValidatedField("route_time", int, "data", "Must be integer")
    trailer_weight_t = ValidatedField("trailer_weight_t", int, "data", "Must be integer")
    route_date = ValidatedField("route_date", int, "data", "Must be integer")
    route_max_duration = ValidatedField("route_max_duration", int, "data", "Must be integer")
    vehicle_capacity = ValidatedField("vehicle_capacity", int, "data", "Must be integer")
    parts = ValidatedField("parts", int, "data", "Must be integer")
    vehicle_max_distance_mi = ValidatedField("vehicle_max_distance_mi", int, "data", "Must be integer")
    max_tour_size = ValidatedField("max_tour_size", int, "data", "Must be integer")
    min_tour_size = ValidatedField("min_tour_size", int, "data", "Must be integer")
    remote_ip = ValidatedField("remote_ip", int, "data", "Must be integer")

    # Float (int|float) → data body
    limited_weight_t = ValidatedField("limited_weight_t", "numeric", "data", "Must be integer")
    weight_per_axle_t = ValidatedField("weight_per_axle_t", "numeric", "data", "Must be integer")
    truck_height = ValidatedField("truck_height", "numeric", "data", "Must be integer")
    truck_width = ValidatedField("truck_width", "numeric", "data", "Must be integer")
    truck_length = ValidatedField("truck_length", "numeric", "data", "Must be integer")

    # Int → query params
    course = ValidatedField("course", int, "param", "Must be integer")
    speed = ValidatedField("speed", int, "param", "Must be Float")
    limit = ValidatedField("limit", int, "param", "Must be integer")
    offset = ValidatedField("offset", int, "param", "Must be integer")

    # Float strict (float only) → query params
    lat = ValidatedField("lat", "float_strict", "param", "Must be Float")
    lng = ValidatedField("lng", "float_strict", "param", "Must be Float")
    altitude = ValidatedField("altitude", "float_strict", "param", "Must be Float")

    # Aliases: cached_lat/cached_lng write to "lat"/"lng" keys
    cached_lat = ValidatedField("lat", "float_strict", "param", "Must be Float")
    cached_lng = ValidatedField("lng", "float_strict", "param", "Must be Float")

    # Enum → data body
    travel_mode = ValidatedField(
        "travel_mode", "enum", "data", "Must be DRIVING, WALKING, TRUCKING", enum_cls=TRAVEL_MODE
    )
    optimize = ValidatedField(
        "optimize", "enum", "data", "Must be DISTANCE, TIME, TIME_WITH_TRAFFIC", enum_cls=OPTIMIZE
    )
    distance_unit = ValidatedField("distance_unit", "enum", "data", "Must be MI or KM", enum_cls=DISTANCE_UNIT)
    truck_hazardous_goods = ValidatedField(
        "truck_hazardous_goods", "enum", "data", "Must be MI or KM", enum_cls=TRUCK_HAZARDOUS_GOODS
    )

    # Enum → query params
    route_path_output = ValidatedField(
        "route_path_output", "enum", "param", "Must be NONE or POINTS", enum_cls=ROUTE_PATH_OUTPUT
    )

    # Boolish 0/1 → data body
    store_route = ValidatedField("store_route", "boolish", "data", "Must be 0 or 1")
    lock_last = ValidatedField("lock_last", "boolish", "data", "Must be 0 or 1")
    disable_optimization = ValidatedField("disable_optimization", "boolish", "data", "Must be 0 or 1")
    shared_publicly = ValidatedField("shared_publicly", "boolish", "data", "Must be 0 or 1")
    share_route = ValidatedField("share_route", "boolish", "data", "Must be 0 or 1")
    rt = ValidatedField("rt", "boolish", "data", "Must be 0 or 1")
    has_trailer = ValidatedField("has_trailer", "boolish", "data", "Must be 0 or 1")

    # Boolish 0/1 → query params
    reoptimize = ValidatedField("reoptimize", "boolish", "param", "Must be 0 or 1")
    directions = ValidatedField("directions", "boolish", "param", "Must be 0 or 1")
    device_tracking_history = ValidatedField("device_tracking_history", "boolish", "param", "Must be 0 or 1")

    # Range/oneof → data body
    algorithm_type = ValidatedField(
        "algorithm_type",
        "oneof",
        "data",
        "Must be ALGORITHM_TYPE: TSP(1), VRP(2), CVRP_TW_SD(3), "
        "CVRP_TW_MD(4), TSP_TW(5), TSP_TW_CR(6), BBCVRP(7), "
        "NO OPTIMIZATION(100) or LEGACY_DISTRIBUTED(101)",
        valid_values=[1, 2, 3, 4, 5, 6, 7, 9, 100, 101],
    )
    metric = ValidatedField(
        "metric",
        "range",
        "data",
        "Must be METRIC: ROUTE4ME_METRIC_EUCLIDEAN , "
        "ROUTE4ME_METRIC_MANHATTAN, ROUTE4ME_METRIC_GEODESIC"
        "ROUTE4ME_METRIC_MATRIXROUTE4ME_METRIC_EXACT_2D",
        valid_range=(1, 7),
    )
    optimization_quality = ValidatedField(
        "optimization_quality", "range", "data", "Must be between 1 to 3", valid_range=(1, 3)
    )
    uturn = ValidatedField(
        "uturn", "range", "data", "Must be : UTURN_DEPART_SHORTEST or UTURN_DEPART_TO_RIGHT", valid_range=(1, 2)
    )
    leftturn = ValidatedField(
        "leftturn",
        "range",
        "data",
        "Must be : LEFTTURN_ALLOW or LEFTTURN_FORBID or LEFTTURN_MULTIAPPROACH",
        valid_range=(1, 3),
    )
    dm = ValidatedField(
        "dm",
        "oneof",
        "data",
        "Must be : R4M_PROPRIETARY_ROUTING or R4M_TRAFFIC_ENGINE or TRUCKING",
        valid_values=[1, 3, 6],
    )
    dirm = ValidatedField(
        "dirm", "oneof", "data", "Must be : R4M_PROPRIETARY_INTERNAL_NAVIGATION_SYSTEM orTRUCKING", valid_values=[1, 3]
    )

    def __init__(self, api):
        self.response = None
        self.api = api
        self.data = {
            "parameters": {},
        }
        self.params = {
            "api_key": api.key,
        }

    @staticmethod
    def check_string_type(obj):
        return isinstance(obj, str)

    def format(self, set_format):
        if set_format in FORMAT.reverse_mapping.keys():
            self._copy_param({"format": set_format})
        else:
            raise ParamValueException("format", "Must be CSV, SERIALIZED, XML")

    def member_id(self, member_id, target="data"):
        if isinstance(member_id, int):
            getattr(self, f"_copy_{target}")({"member_id": member_id})
        else:
            raise ParamValueException("member_id", "Must be integer")

    def device_type(self, device_type, target="data"):
        if device_type in DEVICE_TYPE.reverse_mapping.keys():
            getattr(self, f"_copy_{target}")({"device_type": device_type})
        else:
            raise ParamValueException(
                "device_type",
                "Must be WEB, IPHONE, IPAD, ANDROID_PHONE, ANDROID_TABLET",
            )

    def device_timestamp(self, device_timestamp):
        if is_valid_datetime(device_timestamp):
            self._copy_param({"device_timestamp": device_timestamp})
        else:
            raise ParamValueException("device_timestamp", "Must be YYYY-MM-DD HH:MM:SS format")

    def advanced_constraints(self, advanced_constraints):
        if not isinstance(advanced_constraints, list):
            raise ParamValueException(
                "advanced_constraints",
                "Must be: List of Advanced Constraints",
            )
        self._copy_data({"advanced_constraints": advanced_constraints})

    def bundling(self, bundling):
        if not isinstance(bundling, dict):
            raise ParamValueException(
                "bundling",
                "Must be: Bundling Object",
            )
        self._copy_data({"bundling": bundling})

    def _copy_data(self, params):
        self.data["parameters"].update(params)

    def _copy_param(self, params):
        self.params.update(params)

    def get_params(self):
        return self.params

    def required_params(self, requirements=None):
        if requirements is None:
            requirements = []
        return set(requirements).issubset(set(self.params.keys()))

    @staticmethod
    def check_required_params(params, requirements=None):
        if requirements is None:
            requirements = []
        return set(requirements).issubset(set(params.keys()))

    def validate_params(self, **kwargs):
        for k, v in kwargs.items():
            try:
                self.__getattribute__(k)(v)
            except ParamValueException as e:
                raise e
            except AttributeError:
                raise ParamValueException(k, "Not supported")
        return True

    def add(self, params=None, data=None):
        if params is None:
            params = {}
        if data is None:
            data = {}
        self.validate_params(**params)
        self.validate_params(**data)
        self.data.update(data)
        self.params.update(params)
