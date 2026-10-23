"""Get the custom data of a route.

Calls :meth:`RoutesV5.get_route_custom_data <route4me.routes_v5.RoutesV5.get_route_custom_data>`, which sends
``GET /modules/api/v5.0/routes/{route_id}/custom-data`` (API V5, on ``wh.route4me.com``), and prints each
key and value.

Run it with::

    python examples/routes_v5/get_route_custom_data.py --api_key <your key> --route_id <route id>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id):
    """Print the custom data of the route.

    :param api_key: Route4Me API key.
    :param route_id: route ID.
    """
    route4me = Route4Me(api_key)

    response = route4me.routes_v5.get_route_custom_data(route_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        for key, value in response.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Route Custom Data (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id)
