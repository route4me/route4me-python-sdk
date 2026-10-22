"""The :class:`RouteStatus` resource (API V5): read, set and roll back the status of a route, and set stop statuses."""

from datetime import datetime

from ._url import path_segment
from .api_endpoints import ROUTE_STATUS_V5, ROUTE_STOP_STATUS_V5
from .base import Base
from .exceptions import ParamValueException


class RouteStatus(Base):
    """Route status: where a route is in its life cycle (API V5).

    A route is planned, started, paused, resumed or completed; the values are
    in :data:`~route4me.constants.ROUTE_STATUS`. Use it as
    ``route4me.route_status``. Every method sends a request to
    ``/modules/api/v5.0/route-status/{route_id}`` on ``wh.route4me.com``,
    except :meth:`set_route_stop_status`, which sets the status of stops.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        self.params = {
            "api_key": api.key,
        }
        Base.__init__(self, api)

    @staticmethod
    def _status_url(route_id, suffix=""):
        """Build a route-status URL with ``route_id`` encoded as one path segment.

        :param route_id: ID of the route.
        :param suffix: path after the route ID, e.g. ``"/history"``.
        :return: the absolute URL.
        :raise ParamValueException: when ``route_id`` is empty.
        """
        return f"{ROUTE_STATUS_V5}/{path_segment(route_id, 'route_id')}{suffix}"

    def get_route_status(self, route_id):
        """Get the current status of a route.

        Sends ``GET /modules/api/v5.0/route-status/{route_id}``.

        :param route_id: ID of the route.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``route_id`` is empty.
        """
        return self._call_api(self._status_url(route_id), "get", self.params)

    def get_route_status_history(self, route_id):
        """Get the status history of a route.

        Sends ``GET /modules/api/v5.0/route-status/{route_id}/history``.

        :param route_id: ID of the route.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``route_id`` is empty.
        """
        return self._call_api(self._status_url(route_id, "/history"), "get", self.params)

    def set_route_status(self, route_id, status, lat, lng, event_timestamp=None):
        """Set the status of a route.

        Sends ``POST /modules/api/v5.0/route-status/{route_id}`` with
        ``status``, ``lat``, ``lng`` and ``event_timestamp`` as the JSON body.

        :param route_id: ID of the route.
        :param status: the new status, a :data:`~route4me.constants.ROUTE_STATUS`
            value such as ``"started"``.
        :param lat: latitude where the status changed.
        :param lng: longitude where the status changed.
        :param event_timestamp: when the status changed, as a Unix timestamp
            in seconds. ``None`` (the default) uses the current time.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``route_id`` is empty.
        """
        if event_timestamp is None:
            event_timestamp = int(datetime.now().timestamp())
        data = {
            "status": status,
            "lat": lat,
            "lng": lng,
            "event_timestamp": event_timestamp,
        }
        return self._call_api(self._status_url(route_id), "post", self.params, body=data)

    def rollback_route_status(self, route_id):
        """Roll the status of a route back to the previous one.

        Sends ``GET /modules/api/v5.0/route-status/{route_id}/rollback``.

        :param route_id: ID of the route.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``route_id`` is empty.
        """
        return self._call_api(self._status_url(route_id, "/rollback"), "get", self.params)

    def set_route_stop_status(self, status, *, destination_ids=None, destination_uuids=None, event_timestamp=None):
        """Set the status of one or more stops of routes.

        Sends ``POST /modules/api/v5.0/route-stop-status`` with ``status`` and
        the stops as the JSON body. Give the stops either by ID or by UUID.

        :param status: the new status: ``"Skipped"``, ``"Completed"``,
            ``"Failed"`` or ``"Empty"``.
        :param destination_ids: the route destination IDs, a list of integers.
        :param destination_uuids: the destination UUIDs, a list of 32-character
            hex strings.
        :param event_timestamp: when the status changed, as a Unix timestamp
            in seconds. ``None`` (the default) leaves it to the API.
        :return: the decoded JSON reply, with ``status``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``status`` is empty, or not exactly
            one of ``destination_ids`` and ``destination_uuids`` is given.

        .. versionadded:: 1.0.0
        """
        if not status:
            raise ParamValueException("status", "Missing required params")
        if (destination_ids is None) == (destination_uuids is None):
            raise ParamValueException("destination_ids, destination_uuids", "Give exactly one of them")
        data = {"status": status}
        if destination_ids is not None:
            data["destination_ids"] = destination_ids
        if destination_uuids is not None:
            data["destination_uuids"] = destination_uuids
        if event_timestamp is not None:
            data["event_timestamp"] = event_timestamp
        return self._call_api(ROUTE_STOP_STATUS_V5, "post", {}, body=data)
