"""List the order custom user fields (API V4).

Calls :meth:`Order.get_order_custom_user_fields <route4me.orders.Order.get_order_custom_user_fields>`, which
sends ``GET /api.v4/order_custom_user_fields.php``. Prints the reply.

Run it with::

    python examples/order/get_order_custom_user_fields.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the order custom user fields.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.order.get_order_custom_user_fields()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Order Custom User Fields")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
