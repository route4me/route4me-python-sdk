r"""Search the orders created in a date range, with API V5.

Calls :meth:`OrdersV5.search_orders <route4me.orders_v5.OrdersV5.search_orders>`, which sends
``POST /modules/api/v5.0/orders-platform`` (API V5, on ``wh.route4me.com``) with a
``created_timestamp`` filter and ``limit`` as the JSON body, and prints the reply.

Run it with::

    python examples/order/search_orders.py --api_key <your key> --start <Unix time> --end <Unix time>
"""

import argparse

from route4me import Route4Me


def main(api_key, start, end):
    """Print the orders created from ``start`` to ``end``.

    :param api_key: Route4Me API key.
    :param start: first creation time, a Unix timestamp.
    :param end: last creation time, a Unix timestamp.
    """
    route4me = Route4Me(api_key)

    response = route4me.orders_v5.search_orders(filters={"created_timestamp": [start, end]}, limit=20)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Orders (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--start", dest="start", help="First creation time, Unix timestamp", type=int, required=True)
    parser.add_argument("--end", dest="end", help="Last creation time, Unix timestamp", type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.start, args.end)
