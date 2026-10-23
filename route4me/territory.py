"""The :class:`Territory` resource: create, read, update and delete territories."""

from .api_endpoints import TERRITORY_HOST
from .base import Base
from .exceptions import ParamValueException


class Territory(Base):
    """Territories: named areas of the map.

    Use it as ``route4me.territory``. Every method sends a request to
    ``/api.v4/territory.php``.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
    """

    def __init__(self, api):
        self.json_data = {}
        Base.__init__(self, api)

    def get_territories(self):
        """List all territories.

        Sends ``GET /api.v4/territory.php``.

        :return: the decoded JSON reply: the territories, or the
            ``{"errors": ...}`` dict on an API error.
        """
        return self._call_api(TERRITORY_HOST, "get", self.params, required=["api_key"])

    def get_territory(self, **kwargs):
        """Get one territory by ID.

        Sends ``GET /api.v4/territory.php``.

        :param kwargs: query parameters. Required: ``territory_id``.
        :return: the decoded JSON reply: the territory, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``territory_id`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(TERRITORY_HOST, "get", kwargs, required=["api_key", "territory_id"])

    def add_territory(self, **kwargs):
        """Create a territory.

        Sends ``POST /api.v4/territory.php`` with the keywords as the JSON body.

        :param kwargs: required: ``territory_name``; ``territory_color``, a
            hex colour such as ``"ff0000"``; and ``territory``, the shape, as
            ``{"type": ..., "data": [...]}`` where ``type`` is a
            :data:`~route4me.constants.TERRITORY_TYPE` value.
        :return: the decoded JSON reply: the new territory, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        if not self.check_required_params(kwargs, ["territory_name", "territory_color", "territory"]):
            raise ParamValueException("params", "Params are not complete")
        return self._call_api(TERRITORY_HOST, "post", self.params, body=kwargs)

    def delete_territory(self, **kwargs):
        """Delete a territory.

        Sends ``DELETE /api.v4/territory.php``.

        :param kwargs: query parameters. Required: ``territory_id``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``territory_id`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(TERRITORY_HOST, "delete", kwargs, required=["territory_id"])

    def update_territory(self, territory_id, **kwargs):
        """Update a territory.

        Sends ``PUT /api.v4/territory.php`` with ``territory_id`` in the query
        and the keywords as the JSON body.

        :param territory_id: ID of the territory.
        :param kwargs: the new values. Required: ``territory_name``,
            ``territory_color`` and ``territory``, as for
            :meth:`add_territory`.
        :return: the decoded JSON reply: the updated territory, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        if not self.check_required_params(kwargs, ["territory_name", "territory_color", "territory"]):
            raise ParamValueException("params", "Params are not complete")
        params = {"api_key": self.api.key, "territory_id": territory_id}
        return self._call_api(TERRITORY_HOST, "put", params, body=kwargs)
