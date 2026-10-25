"""Preview the dates on which the schedule of a route repeats.

Calls :meth:`RecurringRoutes.get_route_schedule_preview
<route4me.recurring_routes.RecurringRoutes.get_route_schedule_preview>`, which sends
``GET /modules/api/v5.0/recurring-routes/route-schedules/{route_id}/preview`` (API V5, on ``wh.route4me.com``)
with ``start`` and ``end`` in the query. Prints the reply.

Run it with::

    python examples/recurring_routes/get_route_schedule_preview.py --api_key <your key> \\
        --route_id <route_id> \\
        --start <start> \\
        --end <end>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id, start, end):
    """Print the dates of the preview.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    :param start: First date, as YYYY-MM-DD.
    :param end: Last date, as YYYY-MM-DD.
    """
    route4me = Route4Me(api_key)

    response = route4me.recurring_routes.get_route_schedule_preview(route_id, start=start, end=end)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Route Schedule Preview")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="ID of the route", type=str, required=True)
    parser.add_argument("--start", dest="start", help="First date, as YYYY-MM-DD", type=str, required=True)
    parser.add_argument("--end", dest="end", help="Last date, as YYYY-MM-DD", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id, args.start, args.end)
