"""Search the orders with a filter.

Calls :meth:`Order.filter_orders <route4me.orders.Order.filter_orders>`, which sends
``POST /api.v4/order.php`` with ``{"filter": {"display": "all"}}`` as the JSON body and ``limit=10`` and
``offset=0`` in the query. Prints the reply.

Run it with::

    python examples/order/filter_orders.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first ten orders the filter matches.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.order.filter_orders({"filter": {"display": "all"}}, limit=10, offset=0)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter Orders")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
