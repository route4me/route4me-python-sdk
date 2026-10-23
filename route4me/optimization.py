"""The :class:`Optimization` resource: build, list, update and delete optimization problems."""

from .api_endpoints import (
    ADDRESS_HOST,
    API_HOST,
    HYBRID_OPTIMIZATION,
    HYBRID_OPTIMIZATION_DEPOTS,
    OPTIMIZATION_TIME_PREDICTION,
)
from .base import Base
from .exceptions import ParamValueException
from .slowdowns import Slowdowns
from .utils import is_valid_datetime


class Optimization(Base):
    """Optimization problems: collections of addresses to be routed.

    An optimization problem is a collection of addresses that need to be
    visited. This is distinct from a route, which is a sequence of addresses
    that need to be visited by a single vehicle and a single driver in a fixed
    time period. Solving an optimization problem results in a number of routes.
    Use it as ``route4me.optimization``.

    The setters inherited from :class:`~route4me.base.Base` build the request
    that :meth:`Route4Me.run_optimization
    <route4me.api.Route4Me.run_optimization>` sends. Unless stated otherwise, a
    request method returns the decoded JSON reply, or on an API error the
    ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
    """

    def __init__(self, api):
        Base.__init__(self, api)

    def get_optimizations(self, **kwargs):
        """List optimization problems, a page at a time.

        Sends ``GET /api.v4/optimization_problem.php``.

        :param kwargs: query parameters. Required: ``limit`` and ``offset``.
        :return: the decoded JSON reply, with the problems under
            ``optimizations``, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``limit`` or ``offset`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(API_HOST, "get", kwargs, required=["limit", "offset"])

    def get_optimization(self, **kwargs):
        """Get an optimization problem by ID.

        Sends ``GET /api.v4/optimization_problem.php``. Unlike
        :meth:`Route4Me.get_optimization <route4me.api.Route4Me.get_optimization>`,
        this returns the error dict instead of raising.

        :param kwargs: query parameters. Required: ``optimization_problem_id``.
        :return: the decoded JSON reply: the problem, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``optimization_problem_id`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(API_HOST, "get", kwargs, required=["optimization_problem_id"])

    def update_optimization(self, **kwargs):
        """Add addresses to an optimization problem, optionally re-optimizing it.

        Sends ``PUT /api.v4/optimization_problem.php`` with
        ``optimization_problem_id`` and ``reoptimize`` in the query and the
        other keywords, ``addresses`` included, as the JSON body.

        :param kwargs: required: ``optimization_problem_id``; ``addresses``, a
            list of address dicts; and ``reoptimize``, ``1`` (or ``True``) to
            re-optimize after adding them.
        :return: the decoded JSON reply: the updated problem, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.

        .. versionchanged:: 1.0.0
           The body is JSON and the API key is no longer copied into it; the
           problem ID and ``reoptimize`` moved to the query, as the API expects.
           A boolean ``reoptimize`` is sent as ``1`` or ``0``, not ``"True"``.
        """
        if not self.check_required_params(kwargs, ["optimization_problem_id", "addresses", "reoptimize"]):
            raise ParamValueException("params", "Params are not complete")
        body = dict(kwargs)
        reoptimize = body.pop("reoptimize")
        params = {
            "api_key": self.params["api_key"],
            "optimization_problem_id": body.pop("optimization_problem_id"),
            "reoptimize": int(reoptimize) if isinstance(reoptimize, bool) else reoptimize,
        }
        return self._call_api(API_HOST, "put", params, body=body)

    def delete_optimization(self, **kwargs):
        """Delete optimization problems.

        Sends ``DELETE /api.v4/optimization_problem.php`` with the keywords as
        the JSON body.

        :param kwargs: required: ``optimization_problem_ids``, a list of IDs.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``optimization_problem_ids`` is
            missing.
        """
        if not self.check_required_params(kwargs, ["optimization_problem_ids"]):
            raise ParamValueException("params", "Params are not complete")
        return self._call_api(API_HOST, "delete", self.params, body=kwargs)

    def delete_address_from_optimization(self, **kwargs):
        """Remove one address from an optimization problem.

        Sends ``DELETE /api.v4/address.php``.

        :param kwargs: query parameters. Required: ``optimization_problem_id``
            and ``route_destination_id``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(
            ADDRESS_HOST, "delete", kwargs, required=["optimization_problem_id", "route_destination_id"]
        )

    def get_hybrid_optimization(self, **kwargs):
        """Get the hybrid optimization of a date.

        Sends ``GET /api.v4/hybrid_date_optimization.php`` with the keywords
        as the query.

        :param kwargs: query parameters: ``target_date_string``, the date as
            ``YYYY-MM-DD``, and ``timezone_offset_minutes``.
        :return: the decoded JSON reply: the optimization problem, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(HYBRID_OPTIMIZATION, "get", dict(kwargs))

    def add_depots_to_hybrid_optimization(self, **kwargs):
        """Add depots to a hybrid optimization, or replace its depots.

        Sends ``POST /api/change_hybrid_optimization_depot.php`` with the
        keywords as the JSON body.

        :param kwargs: the body: ``optimization_problem_id``, the hybrid
            optimization; ``new_depots``, a list of address dicts; and
            ``delete_old_depots``, ``True`` to remove the current depots first.
        :return: the decoded JSON reply, e.g. ``{"status": true}``, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(HYBRID_OPTIMIZATION_DEPOTS, "post", {}, body=dict(kwargs))

    def get_optimization_prediction(self, **kwargs):
        """Predict how long an optimization will take.

        Sends ``POST /api.v4/predict-optimization-time.php`` with the
        keywords as the JSON body: the same ``parameters`` and ``addresses``
        an optimization is created with.

        :param kwargs: the body: ``parameters``, the route parameters dict,
            and ``addresses``, a list of address dicts.
        :return: the decoded JSON reply, with the predictions under
            ``time-prediction``, or the ``{"errors": ...}`` dict on an API
            error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(OPTIMIZATION_TIME_PREDICTION, "post", {}, body=dict(kwargs))

    def reset(self):
        """Clear everything staged on this optimization, so the client can build another one.

        Resets the query parameters (keeping the API key), the body data and the
        addresses staged with :meth:`route4me.address.Address.add_address`.

        .. versionadded:: 1.0.0
        """
        self.params = {"api_key": self.api.key}
        self.data = {"parameters": {}}
        self.api.address.addresses = []

    def set_slowdowns(self, service_time, travel_time):
        """Set the ``slowdowns`` route parameter.

        :param service_time: service-time slowdown, an integer percentage from
            0 to 50.
        :param travel_time: travel-time slowdown, an integer percentage from 0
            to 50.
        :raise ValueError: when either value is not an integer from 0 to 50.
        """
        slowdowns = Slowdowns(service_time, travel_time)
        self._copy_data({"slowdowns": slowdowns.to_dict()})

    def set_order_aggregation_groups(
        self,
        scheduled_for_range,
        aggregations_id,
        order_status,
        aggregation_profile_overrides,
        split=True,
    ):
        """Build the optimization from groups of orders.

        Sets ``order_aggregation_groups`` at the top level of the request body.

        :param scheduled_for_range: the order dates to include, as
            ``["YYYY-MM-DD", "YYYY-MM-DD"]``.
        :param aggregations_id: IDs of the order groups, e.g. the ``group_id``
            values from :meth:`OrdersGroup.get_orders_group
            <route4me.orders_group.OrdersGroup.get_orders_group>`.
        :param order_status: the order statuses to include, as
            :data:`~route4me.constants.ORDER_STATUS` values.
        :param aggregation_profile_overrides: maps a group ID to the ID of the
            optimization profile to use for it.
        :param split: sent as ``split``.
        """
        order_aggregation_groups = {
            "split": split,
            "aggregations_id": aggregations_id,
            "filters": {
                "scheduled_for_range": scheduled_for_range,
                "order_status": order_status,
            },
            "aggregation_profile_overrides": aggregation_profile_overrides,
        }
        self.data.update({"order_aggregation_groups": order_aggregation_groups})

    def route_start_date_local(self, route_start_date_local):
        """Set the ``route_start_date_local`` route parameter.

        :param route_start_date_local: the start date, as ``YYYY-MM-DD``.
        :raise ParamValueException: when the value is not in that format.
        """
        if not is_valid_datetime(route_start_date_local, "%Y-%m-%d"):
            raise ParamValueException(
                "params",
                "Route Start Date Local is invalid, must be YYYY-MM-DD date format",
            )
        self._copy_data({"route_start_date_local": route_start_date_local})
