"""List the member configuration settings with API V5.

Calls :meth:`ConfigurationSettingsV5.get_member_configuration_settings
<route4me.configuration_settings_v5.ConfigurationSettingsV5.get_member_configuration_settings>`,
which sends ``GET /modules/api/v5.0/member-configuration-settings`` (API V5, on
``wh.route4me.com``), with ``config_key`` in the query when it is given, and prints each key and
value.

Run it with::

    python examples/configuration_settings/get_member_configuration_settings.py --api_key <your key> \\
        [--config_key <key>]
"""

import argparse

from route4me import Route4Me


def main(api_key, config_key=None):
    """Print the configuration settings.

    :param api_key: Route4Me API key.
    :param config_key: name of the key to filter by, or ``None`` for every key.
    """
    route4me = Route4Me(api_key)

    settings = route4me.configuration_settings_v5
    filters = {} if config_key is None else {"config_key": config_key}
    response = settings.get_member_configuration_settings(**filters)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        for setting in response.get("data", []):
            print(f"{setting.get('config_key')}: {setting.get('config_value')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Member Configuration Settings (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--config_key", dest="config_key", help="Configuration key", type=str)
    args = parser.parse_args()
    main(args.api_key, args.config_key)
