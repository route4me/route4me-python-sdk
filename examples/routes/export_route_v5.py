"""Export a route with API V5.

Calls :meth:`Route.export_route_v5 <route4me.route.Route.export_route_v5>`, which sends
``POST /modules/api/v5.0/route-export/{route_id}/export`` (API V5, on ``wh.route4me.com``) with
``format`` (``csv``) and ``all_custom_fields`` as the JSON body, and prints the export. It replaces
:meth:`Route.export_route <route4me.route.Route.export_route>`, whose V4 endpoint returns 404.

Run it with::

    python examples/routes/export_route_v5.py --api_key <your key> --route_id <route ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id):
    """Export the route and print it.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    """
    route4me = Route4Me(api_key)

    route = route4me.route
    exported_route = route.export_route_v5(route_id)
    if isinstance(exported_route, dict) and "errors" in exported_route.keys():
        print(exported_route["errors"])
    else:
        print(exported_route.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Route Exporter API V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id)
