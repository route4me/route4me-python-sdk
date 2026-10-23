"""List the latest ten routes.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` with ``limit=10`` and ``offset=0``,
which sends ``GET /api.v4/route.php``, and prints the optimization ID and route ID of each route.

Run it with::

    python examples/routes/get_routes.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the latest ten routes.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    route = route4me.route
    response = route.get_routes(limit=10, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        for i, route in enumerate(response):
            print(f"Route #{i + 1}")
            print(f"\tOptimization Problem ID: {route['optimization_problem_id']}\tRoute ID: {route['route_id']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Multiple Routes")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
