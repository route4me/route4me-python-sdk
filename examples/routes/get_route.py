"""Get the latest route.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` (``GET /api.v4/route.php``) to find the
latest route, then :meth:`Route.get_route <route4me.route.Route.get_route>` with its ``route_id``, which
sends the same request with ``route_id`` in the query. Prints the optimization ID and the ID and address
of each destination.

Run it with::

    python examples/routes/get_route.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the latest route.

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
            print(f"Optimization Problem ID: {response['optimization_problem_id']}")
            for address in response["addresses"]:
                print(f"\t\t\tID: {address['route_destination_id']} - Address: {address['address']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Route")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
