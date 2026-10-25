"""The :class:`OptimizationProfiles` resource (API V5): optimization profiles and their entities."""

from ._params import require
from ._url import path_segment
from .api_endpoints import (
    OPTIMIZATION_PROFILES_BASE_V5,
    OPTIMIZATION_PROFILES_DELETE_ENTITIES_V5,
    OPTIMIZATION_PROFILES_SAVE_ENTITIES_V5,
    OPTIMIZATION_PROFILES_V5,
)
from .base import Base


class OptimizationProfiles(Base):
    """Optimization profiles: saved optimization settings (API V5).

    Use it as ``route4me.optimization_profiles``. Requests go to
    ``/modules/api/v5.0/optimization-profiles`` on ``wh.route4me.com``. JSON
    bodies are passed as keyword arguments.

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
    def _profile_url(optimization_profile_id):
        """Build an optimization profile URL with the ID encoded as one path segment.

        :param optimization_profile_id: ID of the optimization profile.
        :return: the absolute URL.
        :raise ParamValueException: when ``optimization_profile_id`` is empty.
        """
        segment = path_segment(optimization_profile_id, "optimization_profile_id")
        return f"{OPTIMIZATION_PROFILES_BASE_V5}/{segment}"

    def get_optimization_profiles(self):
        """List the optimization profiles.

        Sends ``GET /modules/api/v5.0/optimization-profiles/data-list``.

        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        """
        return self._request_decoded(OPTIMIZATION_PROFILES_V5, self.params, "get")

    def create_optimization_profile(self, **kwargs):
        """Create an optimization profile.

        Sends ``POST /modules/api/v5.0/optimization-profiles`` with the keywords
        as the JSON body.

        :param kwargs: the profile settings, e.g. ``profile_name``,
            ``is_default``, ``optimization_type`` (``"multi"``, ``"single"``
            or ``"off"``), ``route_end_mode``, ``avoid_tolls``,
            ``max_stops_count`` or ``depots``. Required: ``profile_name``.
        :return: the decoded JSON reply: the new profile, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``profile_name`` is missing.

        .. versionadded:: 1.0.0
        """
        require(kwargs, ["profile_name"])
        return self._call_api(OPTIMIZATION_PROFILES_BASE_V5, "post", {}, body=kwargs)

    def get_optimization_profile_by_id(self, optimization_profile_id):
        """Get one optimization profile.

        Sends ``GET /modules/api/v5.0/optimization-profiles/{optimization_profile_id}``.

        :param optimization_profile_id: ID of the optimization profile.
        :return: the decoded JSON reply: the profile, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``optimization_profile_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._profile_url(optimization_profile_id), "get", {})

    def update_optimization_profile(self, optimization_profile_id, **kwargs):
        """Update an optimization profile.

        Sends ``PUT /modules/api/v5.0/optimization-profiles/{optimization_profile_id}``
        with the keywords as the JSON body.

        :param optimization_profile_id: ID of the optimization profile.
        :param kwargs: the profile settings, as for
            :meth:`create_optimization_profile`. Required: ``profile_name``.
        :return: the decoded JSON reply: the updated profile, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``optimization_profile_id`` is empty
            or ``profile_name`` is missing.

        .. versionadded:: 1.0.0
        """
        url = self._profile_url(optimization_profile_id)
        require(kwargs, ["profile_name"])
        return self._call_api(url, "put", {}, body=kwargs)

    def delete_optimization_profile(self, optimization_profile_id):
        """Delete an optimization profile.

        Sends ``DELETE /modules/api/v5.0/optimization-profiles/{optimization_profile_id}``.

        :param optimization_profile_id: ID of the optimization profile.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``optimization_profile_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._profile_url(optimization_profile_id), "delete", {})

    def save_entities(self, **kwargs):
        """Save the entities (the setting parts) of optimization profiles.

        Sends ``POST /modules/api/v5.0/optimization-profiles/save-entities``
        with the keywords as the JSON body.

        :param kwargs: ``items``, a list of ``{"id": ..., "guid": ...,
            "parts": [{"guid": ..., "data": {...}, "config": {...}}]}`` dicts,
            one per optimization profile.
        :return: the decoded JSON reply: the saved items, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(OPTIMIZATION_PROFILES_SAVE_ENTITIES_V5, "post", {}, body=kwargs)

    def delete_entities(self, **kwargs):
        """Delete optimization profile entities.

        Sends ``POST /modules/api/v5.0/optimization-profiles/delete-entities``
        with the keywords as the JSON body.

        :param kwargs: ``items``, a list of ``{"id": ...}`` dicts, each the ID
            of an optimization profile.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(OPTIMIZATION_PROFILES_DELETE_ENTITIES_V5, "post", {}, body=kwargs)
