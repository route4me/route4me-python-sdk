"""The :class:`OrdersGroup` resource (API V5): groups of orders and their optimization profiles."""

from .api_endpoints import ASSIGN_PROFILES_V5, ORDERS_GROUP_V5
from .base import Base
from .exceptions import APIException, ParamValueException
from .utils import is_valid_datetime


class OrdersGroup(Base):
    """Groups of orders, for building an optimization from orders (API V5).

    Use it as ``route4me.orders_group``, together with
    :meth:`Optimization.set_order_aggregation_groups
    <route4me.optimization.Optimization.set_order_aggregation_groups>`.
    Requests go to ``wh.route4me.com``.

    Unless stated otherwise, a method returns the decoded JSON reply, the raw
    body (``bytes``) when it is not JSON, or on an API error the
    ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    def _check_scheduled_for_range(self, scheduled_for_range):
        """Check that every date of the range is ``YYYY-MM-DD``.

        :param scheduled_for_range: the dates to check.
        :return: ``True`` when all of them are valid.
        """
        for s in scheduled_for_range:
            if not is_valid_datetime(s, "%Y-%m-%d"):
                return False
        return True

    def get_orders_group(self, scheduled_for_range, statuses):
        """Get the groups of the orders scheduled in a date range.

        Sends ``POST /modules/api/v5.0/orders/aggregation/combined`` with
        ``{"filters": {"scheduled_for_range": ..., "statuses": ...}}`` as the
        JSON body.

        :param scheduled_for_range: the dates, as ``["YYYY-MM-DD",
            "YYYY-MM-DD"]``.
        :param statuses: the order statuses to include, as
            :data:`~route4me.constants.ORDER_STATUS` values.
        :return: the list of groups (``data.items`` of the reply, ``[]`` when
            the reply has no ``data``), the raw body (``bytes``) when it is not
            JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a date is not ``YYYY-MM-DD``.
        """
        if not self._check_scheduled_for_range(scheduled_for_range):
            raise ParamValueException("scheduled_for_range", "Invalid Scheduled Range")
        data = {
            "filters": {
                "scheduled_for_range": scheduled_for_range,
                "statuses": statuses,
            }
        }
        try:
            response = self._request(ORDERS_GROUP_V5, self.params, "post", json=data)
        except APIException as e:
            return e.to_dict()
        try:
            payload = response.json()
        except ValueError:
            return response.content
        if not isinstance(payload, dict):
            return payload
        return payload["data"].get("items", []) if "data" in payload else []

    def assign_optimization_profile(self, optimization_profile_id, group_id):
        """Assign an optimization profile to a group of orders.

        Sends ``POST /modules/api/v5.0/orders/aggregation/assign-optimization-profile``
        with ``group_id`` and ``optimization_profile_id`` as the JSON body.

        :param optimization_profile_id: ID of the optimization profile, e.g.
            from :meth:`OptimizationProfiles.get_optimization_profiles
            <route4me.optimization_profiles.OptimizationProfiles.get_optimization_profiles>`.
        :param group_id: ID of the group of orders.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        """
        data = {
            "group_id": group_id,
            "optimization_profile_id": optimization_profile_id,
        }
        return self._request_decoded(ASSIGN_PROFILES_V5, self.params, "post", json=data)
