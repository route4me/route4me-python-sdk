"""Get the history of an order.

Calls :meth:`OrdersV5.get_order_history <route4me.orders_v5.OrdersV5.get_order_history>`, which sends
``GET /modules/api/v5.0/orders/history`` (API V5, on ``wh.route4me.com``) with ``order_uuid`` in the query.
Prints the reply.

Run it with::

    python examples/order/get_order_history.py --api_key <your key> --order_uuid <order_uuid>
"""

import argparse

from route4me import Route4Me


def main(api_key, order_uuid):
    """Print the history of the order.

    :param api_key: Route4Me API key.
    :param order_uuid: UUID of the order.
    """
    route4me = Route4Me(api_key)

    response = route4me.orders_v5.get_order_history(order_uuid=order_uuid)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Order History")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--order_uuid", dest="order_uuid", help="UUID of the order", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.order_uuid)
