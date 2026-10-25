"""Replace the schedule of a route with a new one.

Calls :meth:`RecurringRoutes.replace_route_schedule
<route4me.recurring_routes.RecurringRoutes.replace_route_schedule>`, which sends
``PUT /modules/api/v5.0/recurring-routes/route-schedules/replace/{route_id}`` (API V5, on ``wh.route4me.com``)
with the new schedule as the JSON body. Prints the reply.

Run it with::

    python examples/recurring_routes/replace_route_schedule.py --api_key <your key> --route_id <route_id>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id):
    """Replace the route schedule and print the reply.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    """
    route4me = Route4Me(api_key)

    response = route4me.recurring_routes.replace_route_schedule(
        route_id,
        schedule=[{"mode": "weekly", "enabled": True, "weekly": {"every": 1, "weekdays": [1, 3, 5]}}],
        advance_interval=1,
        advance_schedule_interval_days=7,
        timezone="UTC",
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace Route Schedule")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="ID of the route", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id)
