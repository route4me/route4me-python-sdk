"""The :class:`RouteStatus` resource (API V5): read, set and roll back the status of a route."""

from datetime import datetime

from .api_endpoints import ROUTE_STATUS_V5
from .base import Base
from .exceptions import APIException


class RouteStatus(Base):
    """Route status: where a route is in its life cycle (API V5).

    A route is planned, started, paused, resumed or completed; the values are
    in :data:`~route4me.constants.ROUTE_STATUS`. Use it as
    ``route4me.route_status``. Every method sends a request to
    ``/modules/api/v5.0/route-status/{route_id}`` on ``wh.route4me.com``.

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

    def get_route_status(self, route_id):
        """Get the current status of a route.

        Sends ``GET /modules/api/v5.0/route-status/{route_id}``.

        :param route_id: ID of the route.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        """
        try:
            response = self._request(f"{ROUTE_STATUS_V5}/{route_id}", self.params, "get")
            return response.json()
        except APIException as e:
            return e.to_dict()

    def get_route_status_history(self, route_id):
        """Get the status history of a route.

        Sends ``GET /modules/api/v5.0/route-status/{route_id}/history``.

        :param route_id: ID of the route.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        """
        try:
            response = self._request(f"{ROUTE_STATUS_V5}/{route_id}/history", self.params, "get")
            return response.json()
        except APIException as e:
            return e.to_dict()

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
        """
        if event_timestamp is None:
            event_timestamp = int(datetime.now().timestamp())
        data = {
            "status": status,
            "lat": lat,
            "lng": lng,
            "event_timestamp": event_timestamp,
        }
        try:
            response = self._request(f"{ROUTE_STATUS_V5}/{route_id}", self.params, "post", json=data)
            return response.json()
        except APIException as e:
            return e.to_dict()

    def rollback_route_status(self, route_id):
        """Roll the status of a route back to the previous one.

        Sends ``GET /modules/api/v5.0/route-status/{route_id}/rollback``.

        :param route_id: ID of the route.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        """
        try:
            response = self._request(f"{ROUTE_STATUS_V5}/{route_id}/rollback", self.params, "get")
            return response.json()
        except APIException as e:
            return e.to_dict()
