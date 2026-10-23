"""The :class:`AccountProfile` resource (API V5): the profile of the API key's member."""

from .api_endpoints import ACCOUNT_PROFILE_V5
from .base import Base


class AccountProfile(Base):
    """Account profile: who the API key belongs to (API V5).

    Use it as ``route4me.account_profile``. Requests go to
    ``/modules/api/v5.0/profile-api`` on ``wh.route4me.com``.

    Every method returns the decoded JSON reply, or on an API error the
    ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    def get_account_profile(self):
        """Get the profile of the member the API key belongs to.

        Sends ``GET /modules/api/v5.0/profile-api``.

        :return: the decoded JSON reply: the profile, with ``member_id``,
            ``root_member_id``, ``email``, ``preferred_units`` and more, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ACCOUNT_PROFILE_V5, "get", {})
