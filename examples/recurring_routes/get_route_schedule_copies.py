"""List the routes copied from the scheduled route of a route.

Calls :meth:`RecurringRoutes.get_route_schedule_copies
<route4me.recurring_routes.RecurringRoutes.get_route_schedule_copies>`, which sends
``POST /modules/api/v5.0/recurring-routes/scheduled-routes/get-copies`` (API V5, on ``wh.route4me.com``) with
``route_id`` and ``route_date`` as the JSON body. Prints the reply.

Run it with::

    python examples/recurring_routes/get_route_schedule_copies.py --api_key <your key> \\
        --route_id <route_id> \\
        --route_date <route_date>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id, route_date):
    """Print the copies.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    :param route_date: Date of the copies, as YYYY-MM-DD.
    """
    route4me = Route4Me(api_key)

    response = route4me.recurring_routes.get_route_schedule_copies(route_id=route_id, route_date=route_date)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Route Schedule Copies")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="ID of the route", type=str, required=True)
    parser.add_argument(
        "--route_date", dest="route_date", help="Date of the copies, as YYYY-MM-DD", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.route_id, args.route_date)
