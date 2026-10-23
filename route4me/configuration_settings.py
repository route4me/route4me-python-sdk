"""The :class:`ConfigurationSettings` resource: the account's configuration keys (API V4)."""

from .api_endpoints import CONFIGURATION_SETTINGS
from .base import Base


class ConfigurationSettings(Base):
    """Configuration settings: key-value pairs stored on the member (API V4).

    Use it as ``route4me.configuration_settings``. Every method sends a request
    to ``/api.v4/configuration-settings.php``. For the API V5 member
    configuration settings, see
    :class:`~route4me.configuration_settings_v5.ConfigurationSettingsV5`.

    Every method returns the decoded JSON reply, or on an API error the
    ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    def create_new_configuration_key(self, config_key, config_value):
        """Create a configuration key.

        Sends ``POST /api.v4/configuration-settings.php`` with ``config_key``
        and ``config_value`` as the JSON body.

        :param config_key: name of the key.
        :param config_value: its value.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        body = {"config_key": config_key, "config_value": config_value}
        return self._call_api(CONFIGURATION_SETTINGS, "post", {}, body=body)

    def get_configuration_data(self, config_key=None):
        """Get one configuration key, or all of them.

        Sends ``GET /api.v4/configuration-settings.php``, with ``config_key``
        in the query when it is given.

        :param config_key: name of the key to get. ``None`` (the default) gets
            every key of the member.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        params = {} if config_key is None else {"config_key": config_key}
        return self._call_api(CONFIGURATION_SETTINGS, "get", params)

    def update_configuration_key(self, config_key, config_value):
        """Change the value of a configuration key.

        Sends ``PUT /api.v4/configuration-settings.php`` with ``config_key``
        and ``config_value`` as the JSON body.

        :param config_key: name of the key.
        :param config_value: its new value.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        body = {"config_key": config_key, "config_value": config_value}
        return self._call_api(CONFIGURATION_SETTINGS, "put", {}, body=body)

    def remove_configuration_key(self, config_key):
        """Delete a configuration key.

        Sends ``DELETE /api.v4/configuration-settings.php`` with
        ``config_key`` as the JSON body.

        :param config_key: name of the key.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(CONFIGURATION_SETTINGS, "delete", {}, body={"config_key": config_key})
