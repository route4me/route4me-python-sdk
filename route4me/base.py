"""Base class of every resource: validated parameter setters and request helpers."""

import copy
import json

from route4me.utils import is_valid_datetime

from ._fields import ValidatedField
from .advanced_constraint import AdvancedConstraint
from .bundling import Bundling
from .constants import (
    DEVICE_TYPE,
    DISTANCE_UNIT,
    FORMAT,
    OPTIMIZE,
    ROUTE_PATH_OUTPUT,
    TRAVEL_MODE,
    TRUCK_HAZARDOUS_GOODS,
)
from .exceptions import APIException, ParamValueException


class Base:
    """Base class of every resource.

    A resource keeps two dicts between calls: ``params``, the query parameters,
    which always include ``api_key``; and ``data``, the request body, whose
    ``data["parameters"]`` holds the route parameters.

    Each class attribute declared with
    :class:`~route4me._fields.ValidatedField` is a setter that validates one
    value and stores it in ``params`` or ``data["parameters"]``, e.g.
    ``optimization.route_name("Monday")``. A setter raises
    :class:`~route4me.exceptions.ParamValueException` for an invalid value.

    :param api: the :class:`~route4me.api.Route4Me` client that sends this
        resource's requests.
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
    limited_weight_t = ValidatedField("limited_weight_t", "numeric", "data", "Must be a number")
    weight_per_axle_t = ValidatedField("weight_per_axle_t", "numeric", "data", "Must be a number")
    truck_height = ValidatedField("truck_height", "numeric", "data", "Must be a number")
    truck_width = ValidatedField("truck_width", "numeric", "data", "Must be a number")
    truck_length = ValidatedField("truck_length", "numeric", "data", "Must be a number")

    # Int → query params
    course = ValidatedField("course", int, "param", "Must be integer")
    speed = ValidatedField("speed", int, "param", "Must be integer")
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
        "truck_hazardous_goods", "enum", "data", "Must be a TRUCK_HAZARDOUS_GOODS value", enum_cls=TRUCK_HAZARDOUS_GOODS
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
        "ADVANCED_CVRP_TW(9), NO OPTIMIZATION(100) or LEGACY_DISTRIBUTED(101)",
        valid_values=[1, 2, 3, 4, 5, 6, 7, 9, 100, 101],
    )
    metric = ValidatedField(
        "metric",
        "range",
        "data",
        "Must be METRIC: ROUTE4ME_METRIC_EUCLIDEAN, "
        "ROUTE4ME_METRIC_MANHATTAN, ROUTE4ME_METRIC_GEODESIC, "
        "ROUTE4ME_METRIC_MATRIX or ROUTE4ME_METRIC_EXACT_2D",
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
        "dirm",
        "oneof",
        "data",
        "Must be R4M_PROPRIETARY_INTERNAL_NAVIGATION_SYSTEM (1) or TRUCKING (3)",
        valid_values=[1, 3],
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
        """Check whether a value is a string.

        :param obj: the value to check.
        :return: ``True`` if ``obj`` is a ``str``.
        """
        return isinstance(obj, str)

    def format(self, set_format):
        """Set the ``format`` query parameter.

        :param set_format: a :data:`~route4me.constants.FORMAT` value, e.g.
            ``FORMAT.JSON``.
        :raise ParamValueException: when the value is not a ``FORMAT`` value.
        """
        if set_format in FORMAT.reverse_mapping:
            self._copy_param({"format": set_format})
        else:
            raise ParamValueException("format", "Must be CSV, SERIALIZED, XML or JSON")

    def member_id(self, member_id, target="data"):
        """Set ``member_id``.

        :param member_id: the member ID.
        :param target: ``"data"`` to store it in the route parameters (the
            default), or ``"param"`` to send it in the query string.
        :raise ParamValueException: when ``member_id`` is not an ``int``.
        """
        if isinstance(member_id, int):
            getattr(self, f"_copy_{target}")({"member_id": member_id})
        else:
            raise ParamValueException("member_id", "Must be integer")

    def device_type(self, device_type, target="data"):
        """Set ``device_type``.

        :param device_type: a :data:`~route4me.constants.DEVICE_TYPE` value,
            e.g. ``DEVICE_TYPE.WEB``.
        :param target: ``"data"`` to store it in the route parameters (the
            default), or ``"param"`` to send it in the query string.
        :raise ParamValueException: when the value is not a ``DEVICE_TYPE``
            value.
        """
        if device_type in DEVICE_TYPE.reverse_mapping:
            getattr(self, f"_copy_{target}")({"device_type": device_type})
        else:
            raise ParamValueException(
                "device_type",
                "Must be WEB, IPHONE, IPAD, ANDROID_PHONE, ANDROID_TABLET",
            )

    def device_timestamp(self, device_timestamp):
        """Set the ``device_timestamp`` query parameter.

        :param device_timestamp: the time, as ``YYYY-MM-DD HH:MM:SS``.
        :raise ParamValueException: when the value is not in that format.
        """
        if is_valid_datetime(device_timestamp):
            self._copy_param({"device_timestamp": device_timestamp})
        else:
            raise ParamValueException("device_timestamp", "Must be YYYY-MM-DD HH:MM:SS format")

    def advanced_constraints(self, advanced_constraints):
        """Set the ``advanced_constraints`` route parameter.

        :param advanced_constraints: a list of constraints:
            :class:`~route4me.advanced_constraint.AdvancedConstraint` objects,
            or dicts such as ``constraint.to_dict()``.
        :raise ParamValueException: when the value is not a list.

        .. versionchanged:: 1.0.0
           :class:`~route4me.advanced_constraint.AdvancedConstraint` objects are
           converted with ``to_dict()``; they used to fail when the request was
           serialised.
        """
        if not isinstance(advanced_constraints, list):
            raise ParamValueException(
                "advanced_constraints",
                "Must be: List of Advanced Constraints",
            )
        constraints = [c.to_dict() if isinstance(c, AdvancedConstraint) else c for c in advanced_constraints]
        self._copy_data({"advanced_constraints": constraints})

    def bundling(self, bundling):
        """Set the ``bundling`` route parameter.

        :param bundling: the bundling settings: a
            :class:`~route4me.bundling.Bundling` object, or a dict such as
            ``Bundling().to_dict()``.
        :raise ParamValueException: when the value is neither.

        .. versionchanged:: 1.0.0
           A :class:`~route4me.bundling.Bundling` object is accepted (#43).
        """
        if isinstance(bundling, Bundling):
            bundling = bundling.to_dict()
        if not isinstance(bundling, dict):
            raise ParamValueException(
                "bundling",
                "Must be: Bundling object or dict",
            )
        self._copy_data({"bundling": bundling})

    def _request(self, endpoint, params, method, **kwargs):
        """Send one request through the client that owns this resource.

        Every resource goes through here, so timeouts, retry, the circuit
        breaker and ``api_key`` handling apply the same way to all of them.

        :param endpoint: absolute URL of the API endpoint.
        :param params: query parameters; the client adds ``api_key`` itself.
        :param method: ``"get"``, ``"post"``, ``"put"`` or ``"delete"``.
        :param kwargs: ``data``, ``json``, ``files`` or ``timeout``, passed through.
        :return: the :class:`requests.Response`.
        :raise APIException: when the API answers outside the 200-399 range.
        """
        send = getattr(self.api, f"_request_{method}")
        # The resources and the client are one package: _make_request is internal
        # to it, and this is the only place a resource reaches into the client.
        return self.api._make_request(endpoint, params, send, **kwargs)  # pylint: disable=protected-access

    def _call_api(self, endpoint, method, params, *, required=None, body=None, body_key="json"):
        """Validate required parameters, send the request and decode the reply.

        :param endpoint: absolute URL of the API endpoint.
        :param method: ``"get"``, ``"post"``, ``"put"`` or ``"delete"``.
        :param params: query parameters.
        :param required: names that must be present in ``params``.
        :param body: request body, or ``None`` for no body.
        :param body_key: how to send ``body``: ``"json"`` or ``"data"`` (form).
        :return: the decoded JSON reply, or the error dict from
            :meth:`APIException.to_dict` when the API answers with an error.
        :raise ParamValueException: when a required parameter is missing.
        """
        if required and not self.check_required_params(params, required):
            raise ParamValueException("params", "Params are not complete")
        kwargs = {} if body is None else {body_key: body}
        try:
            self.response = self._request(endpoint, params, method, **kwargs)
            return self.response.json()
        except APIException as e:
            return e.to_dict()

    def _request_decoded(self, endpoint, params, method, **kwargs):
        """Send a request and decode the reply, tolerating a body that is not JSON.

        :param endpoint: absolute URL of the API endpoint.
        :param params: query parameters; the client adds ``api_key`` itself.
        :param method: ``"get"``, ``"post"``, ``"put"`` or ``"delete"``.
        :param kwargs: ``data``, ``json``, ``files`` or ``timeout``, passed through.
        :return: the decoded JSON reply, the raw body as bytes when it is not
            JSON, or the error dict from :meth:`APIException.to_dict` when the
            API answers with an error.
        """
        try:
            response = self._request(endpoint, params, method, **kwargs)
        except APIException as e:
            return e.to_dict()
        try:
            return json.loads(response.content)
        except ValueError:
            return response.content

    def _copy_data(self, params):
        """Merge values into the route parameters, ``data["parameters"]``.

        :param params: name-to-value mapping.
        """
        self.data["parameters"].update(params)

    def _copy_param(self, params):
        """Merge values into the query parameters, ``params``.

        :param params: name-to-value mapping.
        """
        self.params.update(params)

    def get_params(self):
        """Return the query parameters collected so far.

        :return: the ``params`` dict itself, not a copy.
        """
        return self.params

    def required_params(self, requirements=None):
        """Check that the query parameters contain every required name.

        :param requirements: names that must be keys of ``params``.
        :return: ``True`` when all of them are present.
        """
        if requirements is None:
            requirements = []
        return set(requirements).issubset(set(self.params.keys()))

    @staticmethod
    def check_required_params(params, requirements=None):
        """Check that a mapping contains every required name.

        :param params: the mapping to check, e.g. a method's ``kwargs``.
        :param requirements: names that must be keys of ``params``.
        :return: ``True`` when all of them are present.
        """
        if requirements is None:
            requirements = []
        return set(requirements).issubset(set(params.keys()))

    @staticmethod
    def _missing(params, requirements):
        """Return the names in ``requirements`` that ``params`` lacks.

        :param params: the parameters given.
        :param requirements: the names that must be present.
        :return: the missing names, in the order of ``requirements``.
        """
        return [name for name in requirements if name not in params]

    def validate_params(self, **kwargs):
        """Validate and apply each ``name=value`` via its field setter.

        :param kwargs: parameter names mapped to values. Each name must be a
            setter of this resource, e.g. ``route_id`` or ``limit``.
        :return: ``True``.
        :raise ParamValueException: for an unknown parameter name, a name that
            does not resolve to a setter, or a value the setter rejects.

        .. versionchanged:: 0.3.1
           Only the attribute *lookup* is guarded. The previous version wrapped
           the setter call too, so an ``AttributeError`` raised by a bug *inside*
           a setter was reported as ``ParamValueException(name, "Not supported")``
           -- turning an SDK bug into a misleading "unsupported parameter"
           message. The redundant ``except ParamValueException: raise e`` is
           also gone.
        """
        for k, v in kwargs.items():
            try:
                setter = getattr(self, k)
            except AttributeError:
                raise ParamValueException(k, "Not supported") from None
            if not callable(setter):
                raise ParamValueException(k, "Not a settable parameter")
            # Deliberately outside the try: errors from the setter itself must
            # surface as themselves.
            setter(v)
        return True

    def validated_params(self, **kwargs):
        """Validate keywords with the field setters and return the query they produce.

        Works like :meth:`validate_params`, but on a copy: the resource itself is
        left unchanged, so one call's values can never leak into the next request.

        :param kwargs: parameter names mapped to values, as for :meth:`validate_params`.
        :return: a new dict holding this resource's query parameters plus the
            validated keywords.
        :raise ParamValueException: when a keyword is not a supported parameter
            or has an invalid value.
        """
        saved_params, saved_data = self.params, self.data
        self.params, self.data = dict(saved_params), copy.deepcopy(saved_data)
        try:
            self.validate_params(**kwargs)
            return self.params
        finally:
            self.params, self.data = saved_params, saved_data

    def add(self, params=None, data=None):
        """Validate and apply several parameters at once.

        Every name in ``params`` and ``data`` goes through its setter, which
        stores the value in the query or the route parameters. Then ``params``
        is also merged into the query parameters and ``data`` into the top level
        of the request body.

        :param params: parameter names mapped to values.
        :param data: parameter names mapped to values, also merged into
            ``data``.
        :raise ParamValueException: for an unknown parameter name or a value
            its setter rejects.
        """
        if params is None:
            params = {}
        if data is None:
            data = {}
        self.validate_params(**params)
        self.validate_params(**data)
        self.data.update(data)
        self.params.update(params)
