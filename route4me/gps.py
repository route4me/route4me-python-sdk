"""The :class:`GPS` resource: send device positions and read the location history."""

from .api_endpoints import DEVICE_LOCATION_URL, SET_GPS_HOST, USER_LOCATIONS_HOST, VEHICLE_LOCATIONS_V5
from .base import Base
from .exceptions import ParamValueException


class GPS(Base):
    """GPS tracking: send device positions and read where devices, users and vehicles are.

    Use it as ``route4me.gps``. :meth:`get_vehicle_locations` uses API V5; the
    other methods use the V4 tracking endpoints.

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

    def set_tracking_pings(self, **kwargs):
        """Record one GPS ping of a device, or a batch of pings.

        Sends ``POST /track/set.php`` with the keywords as the JSON body. Unlike
        :meth:`set_gps_track`, which sends one ping in the query string, this
        takes a batch of up to 100 pings in one request.

        For one ping, give its fields at the top level. For a batch, give the
        shared fields (``member_id``, ``device_guid``, ``device_type``,
        ``vehicle_id``, ...) at the top level and the pings in ``items``; a
        field set inside an item wins over the top-level one, except the
        member, device and vehicle, which are read from the top level only.

        :param kwargs: the ping fields: ``lat`` and ``lng`` (required for one
            ping), ``member_id``, ``device_guid`` or ``device_id``,
            ``device_type``, ``route_id``, ``device_timestamp`` (Unix seconds
            or a date string), ``speed``, ``speed_unit`` (``"m/s"``,
            ``"km/h"`` or ``"mph"``), ``course``, ``altitude`` and
            ``custom_data``, among others; or, for a batch, ``items``, a list
            of 1 to 100 dicts that each have ``lat`` and ``lng``.
        :return: the decoded JSON reply: ``status`` and ``tx_id`` for one
            ping; ``status`` and ``items_errors``, the rejected items by
            index, for a batch; or the ``{"errors": ...}`` dict on an API
            error.
        :raise ParamValueException: when the body has neither ``items`` nor
            both ``lat`` and ``lng``.

        .. versionadded:: 1.0.0
        """
        if "items" not in kwargs:
            missing = self._missing(kwargs, ("lat", "lng"))
            if missing:
                raise ParamValueException(", ".join(missing), "Required unless the pings are sent in items")
        return self._call_api(SET_GPS_HOST, "post", {}, body=kwargs)

    def get_user_locations(self, **kwargs):
        """Get the last known location of each user of the account.

        Sends ``GET /api/track/view_user_locations.php``.

        :param kwargs: optional query parameters, sent as is, e.g. ``query``
            to search the users by text such as an email, a name or a member
            ID.
        :return: the decoded JSON reply: the users with their last position,
            or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(USER_LOCATIONS_HOST, "get", dict(kwargs))

    def get_vehicle_locations(self, vehicle_ids):
        """Get the latest known location of one or more vehicles (API V5).

        Sends ``GET /modules/api/v5.0/vehicles/location`` on ``wh.route4me.com``
        with ``ids[]`` in the query, once per vehicle. The spec names the
        parameter ``vehicle_ids``, but the API reads ``ids`` (it validates
        ``ids.0`` as a hex UUID), as the C# and Java SDKs send it.

        :param vehicle_ids: the vehicle IDs, as a list. A single ID string is
            sent as a list of one.
        :return: the decoded JSON reply: the vehicles with their location, or
            the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when no vehicle ID is given.

        .. versionadded:: 1.0.0
        """
        if not vehicle_ids:
            raise ParamValueException("vehicle_ids", "At least one vehicle ID is required")
        if isinstance(vehicle_ids, str):
            vehicle_ids = [vehicle_ids]
        return self._call_api(VEHICLE_LOCATIONS_V5, "get", {"ids": list(vehicle_ids)})
