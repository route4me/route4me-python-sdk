"""The :class:`TeamV5` resource (API V5): the sub-users of the account."""

from ._url import path_segment
from .api_endpoints import TEAM_USERS_BULK_INSERT_V5, TEAM_USERS_V5
from .base import Base
from .exceptions import ParamValueException

#: Fields the API requires to create a team member.
CREATE_REQUIRED = ("member_first_name", "member_last_name", "member_email", "member_type", "OWNER_MEMBER_ID")


class TeamV5(Base):
    """Team management: list, create, update and remove the sub-users of the account (API V5).

    The V5 counterpart of the V4 user methods of :class:`~route4me.members.Members`.
    Use it as ``route4me.team_v5``. Every method sends a request to
    ``/modules/api/v5.0/team/...`` on ``wh.route4me.com``.

    Every method returns the decoded JSON reply, or on an API error the
    ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    @staticmethod
    def _user_url(user_id):
        """Build the URL of one sub-user, with ``user_id`` encoded as one path segment.

        :param user_id: ID of the sub-user.
        :return: the absolute URL.
        :raise ParamValueException: when ``user_id`` is empty.
        """
        return f"{TEAM_USERS_V5}/{path_segment(user_id, 'user_id')}"

    def _require(self, body, names):
        """Raise when a required body field is missing.

        :param body: the request body.
        :param names: the fields that must be present.
        :raise ParamValueException: naming the missing fields.
        """
        missing = self._missing(body, names)
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")

    def get_team_members(self, **kwargs):
        """List the sub-users of the account.

        Sends ``GET /modules/api/v5.0/team/users``.

        :param kwargs: optional query parameters: ``query``, a search phrase;
            ``drivers_only``; ``optimization_problem_id``; ``order_by``; and
            ``facility_ids``, a list sent as one ``facility_ids`` parameter per
            ID.
        :return: the decoded JSON reply: a list of members, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(TEAM_USERS_V5, "get", dict(kwargs))

    def get_team_member_by_id(self, user_id):
        """Get one sub-user.

        Sends ``GET /modules/api/v5.0/team/users/{user_id}``.

        :param user_id: ID of the sub-user.
        :return: the decoded JSON reply: the member, or the ``{"errors": ...}``
            dict on an API error.
        :raise ParamValueException: when ``user_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._user_url(user_id), "get", {})

    def create_team_member(self, **kwargs):
        """Create a sub-user.

        Sends ``POST /modules/api/v5.0/team/users`` with the keywords as the
        JSON body.

        :param kwargs: the member. Required: ``member_first_name``,
            ``member_last_name``, ``member_email``, ``member_type`` (e.g.
            ``"SUB_ACCOUNT_DRIVER"``) and ``OWNER_MEMBER_ID``. Optional fields
            include ``new_password``, ``member_phone``, ``timezone``,
            ``custom_data``, ``facility_ids`` and the permission flags such as
            ``READONLY_USER``.
        :return: the decoded JSON reply: the new member, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        self._require(kwargs, CREATE_REQUIRED)
        return self._call_api(TEAM_USERS_V5, "post", {}, body=dict(kwargs))

    def bulk_create_team_members(self, **kwargs):
        """Create up to 100 sub-users in one request.

        Sends ``POST /modules/api/v5.0/team/users/bulk-insert`` with the
        keywords as the JSON body.

        :param kwargs: required: ``users``, a non-empty list of members, each a
            dict with the fields of :meth:`create_team_member` (a member may
            give ``owner_email`` instead of ``OWNER_MEMBER_ID``). Optional:
            ``conflicts``, what to do when a member exists already:
            ``"fail"``, ``"overwrite"`` or ``"skip"``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``users`` is missing or empty.

        .. versionadded:: 1.0.0
        """
        self._require(kwargs, ("users",))
        if not kwargs["users"]:
            raise ParamValueException("users", "Must hold at least one member")
        return self._call_api(TEAM_USERS_BULK_INSERT_V5, "post", {}, body=dict(kwargs))

    def update_team_member(self, user_id, **kwargs):
        """Update a sub-user.

        Sends ``PATCH /modules/api/v5.0/team/users/{user_id}`` with the
        keywords as the JSON body.

        To add skills to a driver, send them comma-separated in
        ``custom_data``: ``custom_data={"driver_skills": "Forklift,Hazmat"}``.

        :param user_id: ID of the sub-user.
        :param kwargs: the fields to change. Required: ``member_email``. The
            other fields are those of :meth:`create_team_member`.
        :return: the decoded JSON reply: the updated member, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``user_id`` is empty or
            ``member_email`` is missing.

        .. versionadded:: 1.0.0
        """
        url = self._user_url(user_id)
        self._require(kwargs, ("member_email",))
        return self._call_api(url, "patch", {}, body=dict(kwargs))

    def remove_team_member(self, user_id):
        """Remove a sub-user.

        Sends ``DELETE /modules/api/v5.0/team/users/{user_id}``.

        :param user_id: ID of the sub-user.
        :return: the decoded JSON reply: the removed member, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``user_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._user_url(user_id), "delete", {})
