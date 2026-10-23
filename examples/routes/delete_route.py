"""Delete the latest route.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` (``GET /api.v4/route.php``) to find the
latest route, then :meth:`Route.delete_route <route4me.route.Route.delete_route>` with its ``route_id``,
which sends ``DELETE /api.v4/route.php``, and prints the reply. This deletes the latest route of the
account.

Run it with::

    python examples/routes/delete_route.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Delete the latest route and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    route = route4me.route
    print("Getting Last Route")
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        route_id = response[0]["route_id"]
        print(f"Route ID: {route_id}")
        response = route.delete_route(route_id=route_id)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            print("Route Deleted:")
            print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete a Route")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
