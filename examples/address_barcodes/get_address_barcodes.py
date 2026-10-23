"""List the barcodes scanned at a stop of a route (API V5).

Calls :meth:`AddressBarcodes.get_address_barcodes
<route4me.address_barcodes.AddressBarcodes.get_address_barcodes>`, which sends
``GET /modules/api/v5.0/address-barcodes`` (API V5, on ``wh.route4me.com``) with ``route_id``,
``route_destination_id`` and ``limit`` in the query, and prints the reply. Pass its ``next_page_cursor``
as ``cursor`` to get the next page.

Run it with::

    python examples/address_barcodes/get_address_barcodes.py --api_key <your key> \
        --route_id <route ID> --route_destination_id <stop ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id, route_destination_id):
    """Print the first ten barcodes of the stop.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    :param route_destination_id: ID of the stop on the route.
    """
    route4me = Route4Me(api_key)

    barcodes = route4me.address_barcodes
    response = barcodes.get_address_barcodes(route_id=route_id, route_destination_id=route_destination_id, limit=10)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Address Barcodes")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route4Me Route ID", type=str, required=True)
    parser.add_argument(
        "--route_destination_id", dest="route_destination_id", help="Route destination ID", type=int, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.route_id, args.route_destination_id)
