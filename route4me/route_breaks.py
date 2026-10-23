"""The :class:`RouteBreaks` resource (API V5): add driver breaks to routes."""

from .api_endpoints import ROUTE_BREAKS_V5
from .base import Base
from .constants import enum

#: The kinds of driver break: the ``type`` of a break says what its ``params``
#: count before the break starts -- total elapsed time, travel time, service
#: time, a number of locations, or the time of day.
ROUTE_BREAK_TYPE = enum(
    APPROXIMATE_TIME_OF_DAY="approximate_time_of_day",
    CERTAIN_NUMBER_OF_TOTAL_ELAPSED_TIME="certain_number_of_total_elapsed_time",
    CERTAIN_NUMBER_OF_TRAVEL_TIME="certain_number_of_travel_time",
    CERTAIN_NUMBER_OF_SERVICE_TIME="certain_number_of_service_time",
    CERTAIN_NUMBER_OF_LOCATIONS="certain_number_of_locations",
)


class RouteBreaks(Base):
    """Route breaks: driver breaks inserted into existing routes (API V5).

    Use it as ``route4me.route_breaks``. The method sends a request to
    ``/modules/api/v5.0/route-breaks`` on ``wh.route4me.com``. It mirrors
    ``RouteManagerV5.InsertRouteBreaks`` of the C# SDK.

    .. versionadded:: 1.0.0
    """

    def insert_route_breaks(self, route_ids, breaks, replace_existing_breaks):
        """Add driver breaks to one or more routes.

        Sends ``POST /modules/api/v5.0/route-breaks`` with ``route_id``,
        ``breaks`` and ``replace_existing_breaks`` as the JSON body.

        One endpoint takes every kind of break; the ``type`` of each break
        picks the kind. For example, one break after a given travel time,
        with values of the size the C# SDK example uses::

            route4me.route_breaks.insert_route_breaks(
                [route_id],
                [{"type": ROUTE_BREAK_TYPE.CERTAIN_NUMBER_OF_TRAVEL_TIME, "duration": 900, "params": [7200]}],
                replace_existing_breaks=True,
            )

        :param route_ids: the IDs of the routes, as a list. A single ID string
            is sent as a list of one.
        :param breaks: the breaks, a list of dicts with ``type``, a
            :data:`ROUTE_BREAK_TYPE` value; ``duration``, the length of the
            break; and ``params``, a list of integers, the amount of the
            ``type`` after which the break starts. The C# and Java SDKs send
            one ``params`` value per route.
        :param replace_existing_breaks: ``True`` to replace the breaks the
            routes already have, ``False`` to add to them.
        :return: the decoded JSON reply, ``{"status": True}`` on success, or
            the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        if isinstance(route_ids, str):
            route_ids = [route_ids]
        body = {
            "route_id": list(route_ids),
            "breaks": breaks,
            "replace_existing_breaks": replace_existing_breaks,
        }
        return self._call_api(ROUTE_BREAKS_V5, "post", {}, body=body)
