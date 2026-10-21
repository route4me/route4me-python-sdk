"""The :class:`Optimization` resource: build, list, update and delete optimization problems."""

from .api_endpoints import ADDRESS_HOST, API_HOST
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
            list of address dicts; and ``reoptimize``, ``1`` to re-optimize
            after adding them.
        :return: the decoded JSON reply: the updated problem, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.

        .. versionchanged:: 1.0.0
           The body is JSON and the API key is no longer copied into it; the
           problem ID and ``reoptimize`` moved to the query, as the API expects.
        """
        if not self.check_required_params(kwargs, ["optimization_problem_id", "addresses", "reoptimize"]):
            raise ParamValueException("params", "Params are not complete")
        body = dict(kwargs)
        params = {
            "api_key": self.params["api_key"],
            "optimization_problem_id": body.pop("optimization_problem_id"),
            "reoptimize": body.pop("reoptimize"),
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
