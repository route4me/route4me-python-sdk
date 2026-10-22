"""List the route schedules.

Calls :meth:`RecurringRoutes.get_route_schedules_list
<route4me.recurring_routes.RecurringRoutes.get_route_schedules_list>`, which sends
``GET /modules/api/v5.0/recurring-routes/route-schedules`` (API V5, on ``wh.route4me.com``). Prints the reply.

Run it with::

    python examples/recurring_routes/get_route_schedules_list.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the route schedules.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.recurring_routes.get_route_schedules_list()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Route Schedules")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
