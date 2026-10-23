r"""Get one route destination by its ID.

Calls :meth:`RouteDestinationsV5.get_destination
<route4me.route_destinations_v5.RouteDestinationsV5.get_destination>`, which sends
``GET /modules/api/v5.0/route-destinations/{route_destination_id}`` (API V5, on ``wh.route4me.com``),
and prints the destination.

Run it with::

    python examples/route_destinations_v5/get_destination.py --api_key <your key> \
        --route_destination_id <destination ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_destination_id):
    """Print the destination.

    :param api_key: Route4Me API key.
    :param route_destination_id: ID of the destination.
    """
    route4me = Route4Me(api_key)

    response = route4me.route_destinations_v5.get_destination(route_destination_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Route Destination (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--route_destination_id", dest="route_destination_id", help="Route destination ID", type=int, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.route_destination_id)
