"""List the order custom fields.

Calls :meth:`OrdersV5.get_order_custom_fields <route4me.orders_v5.OrdersV5.get_order_custom_fields>`, which
sends ``GET /modules/api/v5.0/orders/custom-fields`` (API V5, on ``wh.route4me.com``). Prints the reply.

Run it with::

    python examples/order/get_order_custom_fields.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the order custom fields.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.orders_v5.get_order_custom_fields()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Order Custom Fields")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
