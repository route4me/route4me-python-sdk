import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    route = route4me.route
    print("Getting Last Route")
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        route_id = response[0]["route_id"]
        print(f"Route ID: {route_id}")
        response = route.get_activities(route_id=route_id, limit=10, offset=5)
        if "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            print(f"Total: {response['total']}")
            print("Activities:\n")
            for i, activity in enumerate(response["results"]):
                print(f"Activity #{i + 1}")
                print(f"\tActivity ID: {activity['activity_id']}")
                print(f"\tActivity Message: {activity['activity_message']}")
                print(f"\tActivity Type: {activity['activity_type']}")
                print(f"\tRoute ID: {activity['route_id']}")
                print(f"\tRoute Name: {activity['route_name']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Activities")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
