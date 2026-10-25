"""The :class:`ConfigurationSettingsV5` resource (API V5): the member configuration settings."""

from .api_endpoints import MEMBER_CONFIGURATION_SETTINGS_V5
from .base import Base


class ConfigurationSettingsV5(Base):
    """Member configuration settings (API V5).

    The V5 counterpart of :class:`~route4me.configuration_settings.ConfigurationSettings`.
    Use it as ``route4me.configuration_settings_v5``. Requests go to
    ``/modules/api/v5.0/member-configuration-settings`` on ``wh.route4me.com``.

    Every method returns the decoded JSON reply, or on an API error the
    ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    def get_member_configuration_settings(self, **kwargs):
        """List the member's configuration settings.

        Sends ``GET /modules/api/v5.0/member-configuration-settings``.

        :param kwargs: optional query parameters: ``mcs``, the configuration
            settings key, and ``config_key``, a key to filter by. The API also
            takes ``organization_api_key`` to list the settings of every member
            of an organization; it travels in the URL, so keep it out of logs.
        :return: the decoded JSON reply, ``{"status": ..., "data": [...]}``,
            or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(MEMBER_CONFIGURATION_SETTINGS_V5, "get", dict(kwargs))
