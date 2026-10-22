"""List routes with API V5.

Calls :meth:`RoutesV5.get_routes <route4me.routes_v5.RoutesV5.get_routes>`, which sends
``POST /modules/api/v5.0/routes`` (API V5, on ``wh.route4me.com``) with ``page`` and ``per_page`` as the
JSON body, and prints the ID and name of each route.

Run it with::

    python examples/routes_v5/get_routes.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first ten routes.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.routes_v5.get_routes(page=1, per_page=10)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        routes = response.get("data", []) if isinstance(response, dict) else response
        for i, route in enumerate(routes):
            print(f"Route #{i + 1}: {route.get('route_id')} {route.get('route_name', '')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Routes (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
