import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    activity_feed = route4me.activity_feed
    response = activity_feed.get_activities_feed(limit=10, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        print(f"Total Found: {response['total']}")
        for i, activity in enumerate(response["results"]):
            print(f"Activity #{i + 1}")
            print(f"\tActivity ID: {activity['activity_id']}")
            print(f"\tActivity Message: {activity['activity_message']}")
            print(f"\tActivity Type: {activity['activity_type']}")
            print(f"\tRoute ID: {activity['route_id']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Activities Feed")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
