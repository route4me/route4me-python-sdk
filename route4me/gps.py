"""The :class:`GPS` resource: send device positions and read the location history."""

from .api_endpoints import DEVICE_LOCATION_URL, SET_GPS_HOST
from .base import Base


class GPS(Base):
    """GPS tracking: send a device's position and read its location history.

    Use it as ``route4me.gps``.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
    """

    requirements = (
        "api_key",
        "format",
        "member_id",
        "route_id",
        "course",
        "speed",
        "lat",
        "lng",
        "device_type",
        "device_guid",
        "device_timestamp",
    )

    def __init__(self, api):
        self.response = None
        self.params = {"api_key": api.key}
        Base.__init__(self, api)

    def set_gps_track(self, **kwargs):
        """Record one position of a device on a route.

        Sends ``GET /track/set.php``. Values set earlier with the setters, e.g.
        ``gps.lat(33.14384)``, or with :meth:`~route4me.base.Base.add` are sent
        as well, and take precedence over keywords.

        :param kwargs: query parameters. Required, as keywords or through the
            setters: ``format``, ``member_id``, ``route_id``, ``course``,
            ``speed``, ``lat``, ``lng``, ``device_type``, ``device_guid`` and
            ``device_timestamp`` (``YYYY-MM-DD HH:MM:SS``).
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        kwargs.update(self.params)
        return self._call_api(SET_GPS_HOST, "get", kwargs, required=self.requirements)

    def get_locations(self, **kwargs):
        """Get the location history of the devices on a route.

        Sends ``GET /api/track/get_device_location.php``.

        :param kwargs: query parameters. Required: ``format``, ``route_id``,
            ``member_id`` and ``time_period``.
        :return: the decoded JSON reply: the locations, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(
            DEVICE_LOCATION_URL, "get", kwargs, required=["api_key", "format", "route_id", "member_id", "time_period"]
        )
