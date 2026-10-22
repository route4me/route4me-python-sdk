"""The :class:`VehicleCapacityProfiles` resource (API V5): list, create, read, update and delete capacity profiles."""

from ._params import require
from ._url import path_segment
from .api_endpoints import VEHICLE_CAPACITY_PROFILES_V5
from .base import Base


class VehicleCapacityProfiles(Base):
    """Vehicle capacity profiles: how much weight, volume, revenue and items a vehicle carries (API V5).

    Use it as ``route4me.vehicle_capacity_profiles``. Every method sends a
    request under ``/modules/api/v5.0/vehicle-capacity-profiles`` on
    ``wh.route4me.com``. Query parameters and JSON bodies are passed as keyword
    arguments; in a query, a ``bool`` is sent as ``1`` or ``0``.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    @staticmethod
    def _profile_url(vehicle_capacity_profile_id):
        """Build a capacity profile URL with the ID encoded as one path segment.

        :param vehicle_capacity_profile_id: ID of the vehicle capacity profile.
        :return: the absolute URL.
        :raise ParamValueException: when ``vehicle_capacity_profile_id`` is
            empty.
        """
        segment = path_segment(vehicle_capacity_profile_id, "vehicle_capacity_profile_id")
        return f"{VEHICLE_CAPACITY_PROFILES_V5}/{segment}"

    def get_vehicle_capacity_profiles(self, **kwargs):
        """List the vehicle capacity profiles.

        Sends ``GET /modules/api/v5.0/vehicle-capacity-profiles``.

        :param kwargs: query parameters, e.g. ``page``, ``per_page``,
            ``merge_pages`` or ``filters``.
        :return: the decoded JSON reply: the capacity profiles, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(VEHICLE_CAPACITY_PROFILES_V5, "get", dict(kwargs))

    def create_vehicle_capacity_profile(self, **kwargs):
        """Create a vehicle capacity profile.

        Sends ``POST /modules/api/v5.0/vehicle-capacity-profiles`` with the
        keywords as the JSON body.

        :param kwargs: the profile fields: ``name``, ``max_weight``,
            ``max_weight_unit``, ``max_volume``, ``max_volume_unit``,
            ``max_revenue`` and ``max_items_number``. Required: ``name``.
        :return: the decoded JSON reply: the new profile, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``name`` is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["name"])
        return self._call_api(VEHICLE_CAPACITY_PROFILES_V5, "post", {}, body=kwargs)

    def get_vehicle_capacity_profile_by_id(self, vehicle_capacity_profile_id):
        """Get one vehicle capacity profile.

        Sends ``GET /modules/api/v5.0/vehicle-capacity-profiles/{id}``.

        :param vehicle_capacity_profile_id: ID of the vehicle capacity profile.
        :return: the decoded JSON reply: the profile, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicle_capacity_profile_id`` is
            empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._profile_url(vehicle_capacity_profile_id), "get", {})

    def update_vehicle_capacity_profile(self, vehicle_capacity_profile_id, **kwargs):
        """Update a vehicle capacity profile.

        Sends ``PATCH /modules/api/v5.0/vehicle-capacity-profiles/{id}`` with
        the keywords as the JSON body.

        :param vehicle_capacity_profile_id: ID of the vehicle capacity profile.
        :param kwargs: the fields to change, as for
            :meth:`create_vehicle_capacity_profile`.
        :return: the decoded JSON reply: the updated profile, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicle_capacity_profile_id`` is
            empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._profile_url(vehicle_capacity_profile_id), "patch", {}, body=kwargs)

    def delete_vehicle_capacity_profile(self, vehicle_capacity_profile_id):
        """Delete a vehicle capacity profile.

        Sends ``DELETE /modules/api/v5.0/vehicle-capacity-profiles/{id}``.

        :param vehicle_capacity_profile_id: ID of the vehicle capacity profile.
        :return: the decoded JSON reply: the deleted profile, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicle_capacity_profile_id`` is
            empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._profile_url(vehicle_capacity_profile_id), "delete", {})
