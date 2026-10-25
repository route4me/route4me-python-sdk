"""Get the driving directions of the latest route.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` and
:meth:`Route.get_route <route4me.route.Route.get_route>` (``GET /api.v4/route.php``) to read the latest
route, then :meth:`Route.get_route_directions <route4me.route.Route.get_route_directions>` with
``directions=1``, which sends ``GET /api.v4/route.php``, and prints each leg of the directions and its
steps.

Run it with::

    python examples/routes/get_route_directions.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the directions of the latest route.

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
            data = {"directions": 1, "route_id": route_id}
            response = route.get_route_directions(**data)
            print(f"Optimization Problem ID: {response['optimization_problem_id']}")
            for i, direction in enumerate(response["directions"]):
                print(f"Direction #{i + 1}")
                print("\tLocation")
                print(f"\t\tTime: {direction['location']['time']}")
                print(f"\t\tName: {direction['location']['name']}")
                print(f"\t\tStart Location: {direction['location']['start_location']}")
                print(f"\t\tEnd Location: {direction['location']['end_location']}")
                print("\tSteps")
                for step in direction["steps"]:
                    print(f"\t\tDirections: {step['directions']}")
                    print(f"\t\tDirection: {step['direction']}")
                    print(f"\t\tDistance: {step['distance']}")
                    print(f"\t\tDistance unit: {step['distance_unit']}")
                    print(f"\t\tManeuver Type: {step['maneuverType']}")
                    print(f"\t\tCompass Direction: {step['compass_direction']}")
                    print(f"\t\tDuration sec: {step['duration_sec']}")
                    print("\t\tManeuver Point")
                    print(f"\t\t\tLat: {step['maneuverPoint']['lat']}")
                    print(f"\t\t\tLng: {step['maneuverPoint']['lng']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Route Directions")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
