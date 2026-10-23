"""Get the configuration of the authentication history API, with API V5.

Calls :meth:`AuthHistory.get_api_config <route4me.auth_history.AuthHistory.get_api_config>`, which
sends ``GET /modules/api/v5.0/auth-history/apiconf`` (API V5, on ``wh.route4me.com``), and prints
the sortable and filterable fields and the API preferences.

Run it with::

    python examples/auth_history/get_api_config.py --api_key <your key>
"""

import argparse
import json

from route4me import Route4Me


def main(api_key):
    """Print the configuration.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    auth_history = route4me.auth_history
    response = auth_history.get_api_config()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Auth History API Config (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
