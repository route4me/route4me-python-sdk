"""Re-optimize the order of every stop of the latest route.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` and
:meth:`Route.get_route <route4me.route.Route.get_route>` (``GET /api.v4/route.php``) to read the latest
route, then :meth:`Route.resequence_route_all <route4me.route.Route.resequence_route_all>` with
``disable_optimization=0`` and ``optimize="Distance"``, which sends
``GET /api.v3/route/reoptimize_2.php``, and prints the reply. This changes the latest route of the
account.

Run it with::

    python examples/routes/resequence_route_all.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Resequence the latest route and print the reply.

    :param api_key: Route4Me API key.
    """
    r4m = Route4Me(api_key)

    route = r4m.route
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        route_id = response[0]["route_id"]
        print(f"Route ID: {route_id}")
        response = route.get_route(route_id=route_id)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            print(f"Route ID: {route_id}")
            data = {
                "disable_optimization": 0,
                "optimize": "Distance",
                "route_id": route_id,
            }
            response = route.resequence_route_all(**data)
            print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Re-sequence all stops from a Route")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
