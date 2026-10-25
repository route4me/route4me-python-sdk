"""Tell whether the scheduled route of a route has been copied.

Calls :meth:`RecurringRoutes.is_route_schedule_copied
<route4me.recurring_routes.RecurringRoutes.is_route_schedule_copied>`, which sends
``GET /modules/api/v5.0/recurring-routes/scheduled-routes/is-copy/{route_id}`` (API V5, on
``wh.route4me.com``). Prints the reply.

Run it with::

    python examples/recurring_routes/is_route_schedule_copied.py --api_key <your key> --route_id <route_id>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id):
    """Print whether the scheduled route was copied.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    """
    route4me = Route4Me(api_key)

    response = route4me.recurring_routes.is_route_schedule_copied(route_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Is Route Schedule Copied")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="ID of the route", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id)
