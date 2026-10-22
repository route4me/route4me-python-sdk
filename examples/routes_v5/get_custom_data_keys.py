"""List the custom data keys used across routes.

Calls :meth:`RoutesV5.get_custom_data_keys <route4me.routes_v5.RoutesV5.get_custom_data_keys>`, which sends
``GET /modules/api/v5.0/routes/custom-data/keys`` (API V5, on ``wh.route4me.com``), and prints each key.

Run it with::

    python examples/routes_v5/get_custom_data_keys.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the custom data keys.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.routes_v5.get_custom_data_keys()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        for key in response:
            print(key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Route Custom Data Keys (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
