r"""Search the routes created in a date range, with API 5.1.

Calls :meth:`RoutesV5.get_routes_by_filter <route4me.routes_v5.RoutesV5.get_routes_by_filter>`, which sends
``POST /modules/api/v5.1/routes`` (API 5.1, on ``wh.route4me.com``) with a ``created_date`` filter, the
time zone and the page as the JSON body, and prints the ID and name of each route.

Run it with::

    python examples/routes_v5/get_routes_by_filter.py --api_key <your key> --start_date <start date> \
        --end_date <end date> [--timezone <timezone>]
"""

import argparse

from route4me import Route4Me


def main(api_key, start_date, end_date, timezone):
    """Print the routes created from ``start_date`` to ``end_date``.

    :param api_key: Route4Me API key.
    :param start_date: first creation date, YYYY-MM-DD.
    :param end_date: last creation date, YYYY-MM-DD.
    :param timezone: IANA time zone.
    """
    route4me = Route4Me(api_key)

    response = route4me.routes_v5.get_routes_by_filter(
        filters={"created_date": [start_date, end_date]},
        order_by=[["route_created_unix", "desc"]],
        timezone=timezone,
        page=1,
        per_page=20,
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        routes = response.get("data", []) if isinstance(response, dict) else response
        for i, route in enumerate(routes):
            print(f"Route #{i + 1}: {route.get('route_id')} {route.get('route_name', '')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Routes by Filter (API 5.1)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--start_date", dest="start_date", help="First creation date, YYYY-MM-DD", type=str, required=True
    )
    parser.add_argument("--end_date", dest="end_date", help="Last creation date, YYYY-MM-DD", type=str, required=True)
    parser.add_argument("--timezone", dest="timezone", help="IANA time zone", type=str, default="UTC")
    args = parser.parse_args()
    main(args.api_key, args.start_date, args.end_date, args.timezone)
