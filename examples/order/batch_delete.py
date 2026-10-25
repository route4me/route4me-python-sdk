"""Delete several orders at once.

Calls :meth:`OrdersV5.batch_delete <route4me.orders_v5.OrdersV5.batch_delete>`, which sends
``POST /modules/api/v5.0/orders-platform/batch-delete`` (API V5, on ``wh.route4me.com``) with ``order_ids`` as
the JSON body. Prints the reply.

Run it with::

    python examples/order/batch_delete.py --api_key <your key> --order_uuids <order_uuids> [<order_uuids> ...]
"""

import argparse

from route4me import Route4Me


def main(api_key, order_uuids):
    """Delete the orders and print the reply.

    :param api_key: Route4Me API key.
    :param order_uuids: UUIDs of the orders to delete.
    """
    route4me = Route4Me(api_key)

    response = route4me.orders_v5.batch_delete(order_ids=order_uuids)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Delete Orders")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--order_uuids", dest="order_uuids", help="UUIDs of the orders to delete", nargs="+", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.order_uuids)
