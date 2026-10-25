"""Get the destinations inserted into the latest route.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` (``GET /api.v4/route.php``) to find the
latest route, then :meth:`ActivityFeed.get_activity_feed_inserted
<route4me.activity_feed.ActivityFeed.get_activity_feed_inserted>`, which sends
``GET /api.v4/activity_feed.php`` with its ``route_id`` and ``activity_type=insert-destination``. Prints
the total and the ID and type of each activity.

Run it with::

    python examples/activity_feed/get_activity_feed_inserted.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the ``insert-destination`` activities of the latest route.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    activity_feed = route4me.activity_feed
    route = route4me.route
    print("Getting Last Route")
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        route_id = response[0]["route_id"]
        print(f"Route ID: {route_id}")
        response = activity_feed.get_activity_feed_inserted(route_id=route_id)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            print(f"Total affected: {response['total']}")
            for i, activity in enumerate(response["results"]):
                print(f"Activity #{i + 1}")
                print(f"\tActivity ID: {activity['activity_id']}")
                print(f"\tActivity Type: {activity['activity_type']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Inserted Destination Activities")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
