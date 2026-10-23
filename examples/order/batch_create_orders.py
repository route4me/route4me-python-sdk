r"""Create two orders in one request, with API V5.

Calls :meth:`OrdersV5.batch_create_orders <route4me.orders_v5.OrdersV5.batch_create_orders>`, which
sends ``POST /modules/api/v5.0/orders-platform/batch-create`` (API V5, on ``wh.route4me.com``) with
the orders as ``data`` in the JSON body, and prints the reply.

Run it with::

    python examples/order/batch_create_orders.py --api_key <your key>
"""

import argparse

from route4me import Route4Me

ORDERS = [
    {"address_1": "1 Example St, Springfield", "cached_lat": 40.1, "cached_lng": -75.2, "address_alias": "Order 1"},
    {"address_1": "2 Example St, Springfield", "cached_lat": 40.2, "cached_lng": -75.3, "address_alias": "Order 2"},
]


def main(api_key):
    """Create the orders and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.orders_v5.batch_create_orders(ORDERS)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Create Orders (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
