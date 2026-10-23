"""Delete a configuration key of the member.

Calls :meth:`ConfigurationSettings.remove_configuration_key
<route4me.configuration_settings.ConfigurationSettings.remove_configuration_key>`, which sends
``DELETE /api.v4/configuration-settings.php`` with ``config_key`` as the JSON body, and prints the
reply. Running it deletes the key.

Run it with::

    python examples/configuration_settings/remove_configuration_key.py --api_key <your key> --config_key <key>
"""

import argparse

from route4me import Route4Me


def main(api_key, config_key):
    """Delete the key and print the reply.

    :param api_key: Route4Me API key.
    :param config_key: name of the key.
    """
    route4me = Route4Me(api_key)

    settings = route4me.configuration_settings
    response = settings.remove_configuration_key(config_key)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove a Configuration Key")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--config_key", dest="config_key", help="Configuration key", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.config_key)
