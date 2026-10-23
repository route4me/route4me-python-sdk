"""Get the GPS tracking history of the latest route.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` (``GET /api.v4/route.php``) to find the
latest route, then :meth:`Route.get_route_tracking <route4me.route.Route.get_route_tracking>`, which
sends ``GET /api.v4/route.php`` with ``device_tracking_history=1``, and prints the destinations and each
tracked point.

Run it with::

    python examples/routes/get_route_tracking.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the destinations and tracking history of the latest route.

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
        response = route.get_route_tracking(route_id=route_id)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            print(f"Optimization Problem ID: {response['optimization_problem_id']}")
            for i, address in enumerate(response["addresses"]):
                print(f"Address #{i + 1}")
                print(f"\tAddress: {address['address']}")
                print(f"\tRoute Destination ID: {address['route_destination_id']}")
            print("Tracking History:")
            for point in response.get("tracking_history", []):
                print(f"\tlat: {point['lt']} lng: {point['lg']} time: {point['ts_friendly']} speed: {point['s']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Route Tracking Data")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
