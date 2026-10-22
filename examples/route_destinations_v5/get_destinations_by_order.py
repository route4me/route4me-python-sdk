r"""List the route destinations made from an order.

Calls :meth:`RouteDestinationsV5.get_destinations_by_order
<route4me.route_destinations_v5.RouteDestinationsV5.get_destinations_by_order>`, which sends
``GET /modules/api/v5.0/route-destinations/order/{order_uuid}`` (API V5, on ``wh.route4me.com``),
and prints the destinations of the order.

Run it with::

    python examples/route_destinations_v5/get_destinations_by_order.py --api_key <your key> --order_uuid <order UUID>
"""

import argparse

from route4me import Route4Me


def main(api_key, order_uuid):
    """Print the destinations of the order.

    :param api_key: Route4Me API key.
    :param order_uuid: UUID of the order.
    """
    route4me = Route4Me(api_key)

    response = route4me.route_destinations_v5.get_destinations_by_order(order_uuid)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Route Destinations by Order (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--order_uuid", dest="order_uuid", help="Order UUID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.order_uuid)
