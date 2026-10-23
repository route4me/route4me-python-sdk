"""Add a driver break to one or more routes with API V5.

Calls :meth:`RouteBreaks.insert_route_breaks <route4me.route_breaks.RouteBreaks.insert_route_breaks>`,
which sends ``POST /modules/api/v5.0/route-breaks`` (API V5, on ``wh.route4me.com``) with ``route_id``,
``breaks`` and ``replace_existing_breaks`` as the JSON body, and prints the reply. ``--break_type``
picks the kind of break, a :data:`~route4me.route_breaks.ROUTE_BREAK_TYPE` value: after a total
elapsed time (the default), a travel time, a service time or a number of locations. The default
``--duration`` and ``--after`` are the values of the C# SDK example. This replaces the breaks the
routes already have.

Run it with::

    python examples/route_breaks/insert_route_breaks.py --api_key <your key> --route_id <route ID> \\
        --break_type certain_number_of_locations --duration 900 --after 3
"""

import argparse

from route4me import Route4Me
from route4me.route_breaks import ROUTE_BREAK_TYPE


def main(api_key, route_ids, break_type, duration, after):
    """Insert one break into each route and print the reply.

    :param api_key: Route4Me API key.
    :param route_ids: IDs of the routes.
    :param break_type: the kind of break, a ``ROUTE_BREAK_TYPE`` value.
    :param duration: the length of the break.
    :param after: the amount of ``break_type`` after which the break starts.
    """
    route4me = Route4Me(api_key)

    route_breaks = route4me.route_breaks
    breaks = [{"type": break_type, "duration": duration, "params": [after] * len(route_ids)}]
    response = route_breaks.insert_route_breaks(route_ids, breaks, replace_existing_breaks=True)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert Route Breaks")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_ids", help="Route ID(s)", type=str, nargs="+", required=True)
    parser.add_argument(
        "--break_type",
        dest="break_type",
        help="Kind of break",
        choices=sorted(ROUTE_BREAK_TYPE.reverse_mapping),
        default=ROUTE_BREAK_TYPE.CERTAIN_NUMBER_OF_TOTAL_ELAPSED_TIME,
    )
    parser.add_argument("--duration", dest="duration", help="Length of the break", type=int, default=900)
    parser.add_argument("--after", dest="after", help="Amount after which the break starts", type=int, default=3600)
    args = parser.parse_args()
    main(args.api_key, args.route_ids, args.break_type, args.duration, args.after)
