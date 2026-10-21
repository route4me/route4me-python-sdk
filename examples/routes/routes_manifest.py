import argparse

from route4me import Route4Me
from route4me.constants import (
    ROUTE_PATH_OUTPUT,
)


def main(api_key):
    route4me = Route4Me(api_key)

    route = route4me.route
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        route_id = response[0]["route_id"]
        print(f"Route ID: {route_id}")
        params = {
            "route_id": route_id,
            "directions": 1,
            "route_path_output": ROUTE_PATH_OUTPUT.POINTS,
            "device_tracking_history": 1,
            "limit": 10,
            "offset": 5,
        }
        response = route.get_route(**params)
        print(f"Optimization Problem id: {response['optimization_problem_id']}")
        print(f"Trip distance: {response['trip_distance']}")
        print(f"Miles per Gallon: {response['mpg']}")
        for i, direction in enumerate(response["directions"]):
            print(f"Address #{i + 1}")
            print(f"Start Location: {direction['location']['start_location']}")
            print(f"End Location: {direction['location']['end_location']}")
            print(f"Distance: {direction['location']['segment_distance']}")
            print(f"Time: {direction['location']['time']}")
            print("===>Steps")
            for j, step in enumerate(direction["steps"]):
                print(f"\tstep #{j + 1}")
                print(f"\tDirections: {step['directions']}")
                print(f"\tDuration: {step['duration_sec']} sec")
                print(f"\tCompass Direction: {step['compass_direction']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Route Manifest")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
