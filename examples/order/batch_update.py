"""Give several orders the same color.

Calls :meth:`OrdersV5.batch_update <route4me.orders_v5.OrdersV5.batch_update>`, which sends
``POST /modules/api/v5.0/orders-platform/batch-update`` (API V5, on ``wh.route4me.com``) with ``order_ids``
and ``data`` as the JSON body. Prints the updated orders.

Run it with::

    python examples/order/batch_update.py --api_key <your key> --order_uuids <order_uuids> [<order_uuids> ...]
"""

import argparse

from route4me import Route4Me


def main(api_key, order_uuids):
    """Update the orders and print the reply.

    :param api_key: Route4Me API key.
    :param order_uuids: UUIDs of the orders to update.
    """
    route4me = Route4Me(api_key)

    response = route4me.orders_v5.batch_update(order_ids=order_uuids, data={"color": "ff0000"})
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Update Orders")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--order_uuids", dest="order_uuids", help="UUIDs of the orders to update", nargs="+", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.order_uuids)
