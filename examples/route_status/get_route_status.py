"""Get the status of a route.

Calls :meth:`RouteStatus.get_route_status <route4me.route_status.RouteStatus.get_route_status>`, which
sends ``GET /modules/api/v5.0/route-status/{route_id}`` (API V5, on ``wh.route4me.com``), and prints the
reply.

Run it with::

    python examples/route_status/get_route_status.py --api_key <your key> --route_id <route ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id):
    """Print the status of the route.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    """
    r4m = Route4Me(api_key)

    route = r4m.route_status
    print(f"Route ID: {route_id}")
    response = route.get_route_status(route_id=route_id)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Route Status")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route4Me Route ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id)
