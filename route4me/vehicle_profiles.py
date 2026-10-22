"""The :class:`VehicleProfiles` resource (API V5): list, create, read, update and delete vehicle profiles."""

from ._url import path_segment
from ._v5_params import query, require
from .api_endpoints import VEHICLE_PROFILES_V5
from .base import Base


class VehicleProfiles(Base):
    """Vehicle profiles: the size, weight, fuel and hazmat data of a kind of vehicle (API V5).

    Use it as ``route4me.vehicle_profiles``. Every method sends a request under
    ``/modules/api/v5.0/vehicle-profiles`` on ``wh.route4me.com``. Query
    parameters and JSON bodies are passed as keyword arguments; in a query, a
    ``bool`` is sent as ``1`` or ``0``.

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
    def _profile_url(vehicle_profile_id):
        """Build a vehicle profile URL with the ID encoded as one path segment.

        :param vehicle_profile_id: ID of the vehicle profile.
        :return: the absolute URL.
        :raise ParamValueException: when ``vehicle_profile_id`` is empty.
        """
        return f"{VEHICLE_PROFILES_V5}/{path_segment(vehicle_profile_id, 'vehicle_profile_id')}"

    def get_vehicle_profiles(self, **kwargs):
        """List the vehicle profiles.

        Sends ``GET /modules/api/v5.0/vehicle-profiles``.

        :param kwargs: query parameters: ``with_pagination`` (``True`` for one
            page at a time), ``page`` and ``per_page``. Required:
            ``with_pagination``.
        :return: the decoded JSON reply: the vehicle profiles, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``with_pagination`` is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["with_pagination"])
        return self._call_api(VEHICLE_PROFILES_V5, "get", query(kwargs))

    def create_vehicle_profile(self, **kwargs):
        """Create a vehicle profile.

        Sends ``POST /modules/api/v5.0/vehicle-profiles`` with the keywords as
        the JSON body.

        :param kwargs: the profile fields, e.g. ``name``, ``fuel_type``,
            ``fuel_consumption_city``, ``fuel_consumption_highway``,
            ``hazmat_type``, ``vehicle_axle_count`` or
            ``vehicle_profile_code``, with their ``*_unit`` fields. Required:
            ``name``.
        :return: the decoded JSON reply: the new profile, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``name`` is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["name"])
        return self._call_api(VEHICLE_PROFILES_V5, "post", {}, body=kwargs)

    def get_vehicle_profile_by_id(self, vehicle_profile_id):
        """Get one vehicle profile.

        Sends ``GET /modules/api/v5.0/vehicle-profiles/{vehicle_profile_id}``.

        :param vehicle_profile_id: ID of the vehicle profile.
        :return: the decoded JSON reply: the profile, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicle_profile_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._profile_url(vehicle_profile_id), "get", {})

    def update_vehicle_profile(self, vehicle_profile_id, **kwargs):
        """Update a vehicle profile.

        Sends ``PATCH /modules/api/v5.0/vehicle-profiles/{vehicle_profile_id}``
        with the keywords as the JSON body.

        :param vehicle_profile_id: ID of the vehicle profile.
        :param kwargs: the fields to change, as for
            :meth:`create_vehicle_profile`.
        :return: the decoded JSON reply: the updated profile, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vehicle_profile_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._profile_url(vehicle_profile_id), "patch", {}, body=kwargs)

    def delete_vehicle_profile(self, vehicle_profile_id):
        """Delete a vehicle profile.

        Sends ``DELETE /modules/api/v5.0/vehicle-profiles/{vehicle_profile_id}``.

        :param vehicle_profile_id: ID of the vehicle profile.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``vehicle_profile_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._profile_url(vehicle_profile_id), "delete", {})
