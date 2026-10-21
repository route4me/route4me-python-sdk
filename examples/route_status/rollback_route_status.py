"""Roll the status of a route back to the previous one.

Calls :meth:`RouteStatus.rollback_route_status
<route4me.route_status.RouteStatus.rollback_route_status>`, which sends
``GET /modules/api/v5.0/route-status/{route_id}/rollback`` (API V5, on ``wh.route4me.com``), and prints
the reply. This changes the status of the route.

Run it with::

    python examples/route_status/rollback_route_status.py --api_key <your key> --route_id <route ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id):
    """Roll back the status of the route and print the reply.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    """
    r4m = Route4Me(api_key)

    route = r4m.route_status
    print(f"Route ID: {route_id}")
    response = route.rollback_route_status(route_id=route_id)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Roll Back Route Status")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route4Me Route ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id)
