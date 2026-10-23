"""Delete the schedule items of a route.

Calls :meth:`RecurringRoutes.delete_route_schedule_items
<route4me.recurring_routes.RecurringRoutes.delete_route_schedule_items>`, which sends
``DELETE /modules/api/v5.0/recurring-routes/route-schedules/{route_id}/items`` (API V5, on
``wh.route4me.com``). Prints the reply.

Run it with::

    python examples/recurring_routes/delete_route_schedule_items.py --api_key <your key> --route_id <route_id>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id):
    """Delete the schedule items and print the reply.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    """
    route4me = Route4Me(api_key)

    response = route4me.recurring_routes.delete_route_schedule_items(route_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete Route Schedule Items")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="ID of the route", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id)
