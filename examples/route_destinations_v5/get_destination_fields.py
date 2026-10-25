"""List the destination fields that can be filtered and sorted on.

Calls :meth:`RouteDestinationsV5.get_destination_fields
<route4me.route_destinations_v5.RouteDestinationsV5.get_destination_fields>`, which sends
``GET /modules/api/v5.0/route-destinations/list/fields`` (API V5, on ``wh.route4me.com``), and prints the
reply.

Run it with::

    python examples/route_destinations_v5/get_destination_fields.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the destination fields.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.route_destinations_v5.get_destination_fields()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Destination Fields (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
