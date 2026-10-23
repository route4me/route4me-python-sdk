"""Make a route recur on Mondays, Wednesdays and Fridays.

Calls :meth:`RecurringRoutes.create_master_route
<route4me.recurring_routes.RecurringRoutes.create_master_route>`, which sends
``POST /modules/api/v5.0/recurring-routes/master-routes`` (API V5, on ``wh.route4me.com``) with the route ID
and the schedule as the JSON body. Prints the reply.

Run it with::

    python examples/recurring_routes/create_master_route.py --api_key <your key> --route_id <route_id>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id):
    """Create the master route and print the reply.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    """
    route4me = Route4Me(api_key)

    response = route4me.recurring_routes.create_master_route(
        route_id=route_id,
        name="Example master route",
        schedule=[{"mode": "weekly", "enabled": True, "weekly": {"every": 1, "weekdays": [1, 3, 5]}}],
        timezone="UTC",
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Master Route")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="ID of the route", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id)
