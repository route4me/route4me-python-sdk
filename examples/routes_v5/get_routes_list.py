r"""List the routes scheduled in a date range, with API V5.

Calls :meth:`RoutesV5.get_routes_list <route4me.routes_v5.RoutesV5.get_routes_list>`, which sends
``POST /modules/api/v5.0/routes/list`` (API V5, on ``wh.route4me.com``) with a ``schedule_date`` filter,
``page`` and ``per_page`` as the JSON body, and prints the ID and name of each route.

Run it with::

    python examples/routes_v5/get_routes_list.py --api_key <your key> --start_date <start date> \
        --end_date <end date>
"""

import argparse

from route4me import Route4Me


def main(api_key, start_date, end_date):
    """Print the routes scheduled from ``start_date`` to ``end_date``.

    :param api_key: Route4Me API key.
    :param start_date: first schedule date, YYYY-MM-DD.
    :param end_date: last schedule date, YYYY-MM-DD.
    """
    route4me = Route4Me(api_key)

    response = route4me.routes_v5.get_routes_list(
        filters={"schedule_date": [start_date, end_date]}, page=1, per_page=20
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        routes = response.get("data", []) if isinstance(response, dict) else response
        for i, route in enumerate(routes):
            print(f"Route #{i + 1}: {route.get('route_id')} {route.get('route_name', '')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the Route List (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--start_date", dest="start_date", help="First schedule date, YYYY-MM-DD", type=str, required=True
    )
    parser.add_argument("--end_date", dest="end_date", help="Last schedule date, YYYY-MM-DD", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.start_date, args.end_date)
