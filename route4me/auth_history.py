"""The :class:`AuthHistory` resource (API V5): the member authentication history."""

from .api_endpoints import AUTH_HISTORY_API_CONFIG_V5
from .base import Base


class AuthHistory(Base):
    """Authentication history: the log-ins of the account's members (API V5).

    Use it as ``route4me.auth_history``. Requests go to
    ``/modules/api/v5.0/auth-history`` on ``wh.route4me.com``.

    Every method returns the decoded JSON reply, or on an API error the
    ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    def get_api_config(self):
        """Get the configuration of the authentication history API.

        Sends ``GET /modules/api/v5.0/auth-history/apiconf``.

        :return: the decoded JSON reply: ``api_capabilities`` (the sortable and
            filterable fields, and whether search works) and
            ``api_preferences``, or the ``{"errors": ...}`` dict on an API
            error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(AUTH_HISTORY_API_CONFIG_V5, "get", {})
