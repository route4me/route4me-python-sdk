"""Get the path points of the latest route.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` and
:meth:`Route.get_route <route4me.route.Route.get_route>` (``GET /api.v4/route.php``) to read the latest
route, then :meth:`Route.get_route_path_points <route4me.route.Route.get_route_path_points>` with
``route_path_output="Points"``, which sends ``GET /api.v4/route.php``, and prints each destination and
the points of the path to the next one.

Run it with::

    python examples/routes/get_route_path_points.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the destinations and path points of the latest route.

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
            data = {"route_path_output": "Points", "route_id": route_id}
            response = route.get_route_path_points(**data)
            print(f"Optimization Problem ID: {response['optimization_problem_id']}")
            for i, address in enumerate(response["addresses"]):
                print(f"Address #{i + 1}")
                print(f"\tAddress: {address['address']}")
                print(f"\tRoute Destination ID: {address['route_destination_id']}")
                if "path_to_next" in address.keys():
                    for j, path in enumerate(address["path_to_next"]):
                        print(f"\t{j + 1} - \tlat: {path['lat']} \tlng: {path['lng']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Route Path Points")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
