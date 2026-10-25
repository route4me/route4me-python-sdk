"""List the archived orders, a page at a time.

Calls :meth:`OrdersV5.archive_orders <route4me.orders_v5.OrdersV5.archive_orders>`, which sends
``POST /modules/api/v5.0/orders/archive`` (API V5, on ``wh.route4me.com``) with ``per_page=10`` as the JSON
body. Prints the reply.

Run it with::

    python examples/order/archive_orders.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first page of archived orders.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.orders_v5.archive_orders(per_page=10)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Archive Orders")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
