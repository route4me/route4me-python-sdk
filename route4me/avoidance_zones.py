"""The :class:`AvoidanceZones` resource: areas that routes must avoid."""

from .api_endpoints import AVOIDANCE
from .base import Base
from .exceptions import ParamValueException


class AvoidanceZones(Base):
    """Avoidance zones: areas that routes must avoid.

    Use it as ``route4me.avoidance_zones``. Every method sends a request to
    ``/api.v4/avoidance.php``.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
    """

    def __init__(self, api):
        self.json_data = {}
        Base.__init__(self, api)

    def get_avoidance_zones(self):
        """List all avoidance zones.

        Sends ``GET /api.v4/avoidance.php``.

        :return: the decoded JSON reply: the avoidance zones, or the
            ``{"errors": ...}`` dict on an API error.
        """
        return self._call_api(AVOIDANCE, "get", self.params, required=["api_key"])

    def get_avoidance_zone(self, **kwargs):
        """Get one avoidance zone by ID.

        Sends ``GET /api.v4/avoidance.php``.

        :param kwargs: query parameters. Required: ``territory_id``.
        :return: the decoded JSON reply: the avoidance zone, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``territory_id`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(AVOIDANCE, "get", kwargs, required=["api_key", "territory_id"])

    def add_avoidance_zone(self, **kwargs):
        """Create an avoidance zone.

        Sends ``POST /api.v4/avoidance.php`` with the keywords as the JSON body.

        :param kwargs: required: ``territory_name``; ``territory_color``, a
            hex colour such as ``"ff0000"``; and ``territory``, the shape, as
            ``{"type": ..., "data": [...]}`` where ``type`` is a
            :data:`~route4me.constants.TERRITORY_TYPE` value.
        :return: the decoded JSON reply: the new avoidance zone, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        if not self.check_required_params(kwargs, ["territory_name", "territory_color", "territory"]):
            raise ParamValueException("params", "Params are not complete")
        return self._call_api(AVOIDANCE, "post", self.params, body=kwargs)

    def delete_avoidance_zone(self, **kwargs):
        """Delete an avoidance zone.

        Sends ``DELETE /api.v4/avoidance.php``.

        :param kwargs: query parameters. Required: ``territory_id``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``territory_id`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(AVOIDANCE, "delete", kwargs, required=["territory_id"])

    def update_avoidance_zone(self, territory_id, **kwargs):
        """Update an avoidance zone.

        Sends ``PUT /api.v4/avoidance.php`` with ``territory_id`` in the query
        and the keywords as the JSON body.

        :param territory_id: ID of the avoidance zone.
        :param kwargs: the new values. Required: ``territory_name``,
            ``territory_color`` and ``territory``, as for
            :meth:`add_avoidance_zone`.
        :return: the decoded JSON reply: the updated avoidance zone, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        self.params.update({"territory_id": territory_id})
        if not self.check_required_params(kwargs, ["territory_name", "territory_color", "territory"]):
            raise ParamValueException("params", "Params are not complete")
        return self._call_api(AVOIDANCE, "put", self.params, body=kwargs)


# Backward-compatible alias for the old misspelled name
AvoindanceZones = AvoidanceZones
