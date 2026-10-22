r"""List the orders added on a day, with API V4.

Calls :meth:`Order.get_orders <route4me.orders.Order.get_orders>`, which sends
``GET /api.v4/order.php`` (API V4, on ``api.route4me.com``) with ``day_added_YYMMDD``, ``limit`` and
``offset`` in the query, and prints the ID and address of each order.

Run it with::

    python examples/order/get_orders.py --api_key <your key> --day <YYYY-MM-DD>
"""

import argparse

from route4me import Route4Me


def main(api_key, day):
    """Print the orders added on ``day``.

    :param api_key: Route4Me API key.
    :param day: the day the orders were added, YYYY-MM-DD.
    """
    route4me = Route4Me(api_key)

    response = route4me.order.get_orders(day_added_YYMMDD=day, limit=20, offset=0)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    elif isinstance(response, dict):
        for order in response.get("results", []):
            print(f"Order {order.get('order_id')}: {order.get('address_1', '')}")
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Orders (API V4)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--day", dest="day", help="Day the orders were added, YYYY-MM-DD", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.day)
