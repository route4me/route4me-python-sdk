"""Log a message on the latest route's activity feed.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` (``GET /api.v4/route.php``) to find the
latest route, then :meth:`ActivityFeed.log_specific_message
<route4me.activity_feed.ActivityFeed.log_specific_message>`, which sends
``POST /api.v4/activity_feed.php`` with the ``route_id``, the ``activity_message`` and
``activity_type=user_message`` as the JSON body. The message stays in the route's feed.

Run it with::

    python examples/activity_feed/log_specific_message.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Log a message on the latest route.

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
        response = activity_feed.log_specific_message(activity_message="Hello from Python SDK", route_id=route_id)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            print(f"Message Logged: {response['status']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log Specific Message")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
