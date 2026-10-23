"""Get one configuration key of the member, or all of them.

Calls :meth:`ConfigurationSettings.get_configuration_data
<route4me.configuration_settings.ConfigurationSettings.get_configuration_data>`, which sends
``GET /api.v4/configuration-settings.php``, with ``config_key`` in the query when it is given, and
prints the reply.

Run it with::

    python examples/configuration_settings/get_configuration_data.py --api_key <your key> [--config_key <key>]
"""

import argparse
import json

from route4me import Route4Me


def main(api_key, config_key=None):
    """Print the configuration data.

    :param api_key: Route4Me API key.
    :param config_key: name of the key, or ``None`` for every key.
    """
    route4me = Route4Me(api_key)

    settings = route4me.configuration_settings
    response = settings.get_configuration_data(config_key)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Configuration Data")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--config_key", dest="config_key", help="Configuration key", type=str)
    args = parser.parse_args()
    main(args.api_key, args.config_key)
