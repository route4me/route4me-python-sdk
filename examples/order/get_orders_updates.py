"""Get the orders changed since a point in time.

Calls :meth:`Order.get_orders_updates <route4me.orders.Order.get_orders_updates>`, which sends
``GET /api.v4/orders/changes.php`` with ``last_known_ts`` in the query. Prints the reply.

Run it with::

    python examples/order/get_orders_updates.py --api_key <your key> --last_known_ts <last_known_ts>
"""

import argparse

from route4me import Route4Me


def main(api_key, last_known_ts):
    """Print the orders changed since ``last_known_ts``.

    :param api_key: Route4Me API key.
    :param last_known_ts: Unix timestamp of the last update already known.
    """
    route4me = Route4Me(api_key)

    response = route4me.order.get_orders_updates(last_known_ts=last_known_ts)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Orders Updates")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--last_known_ts",
        dest="last_known_ts",
        help="Unix timestamp of the last update already known",
        type=int,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.last_known_ts)
