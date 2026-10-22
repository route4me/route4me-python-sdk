"""Delete an order custom field.

Calls :meth:`OrdersV5.delete_order_custom_field <route4me.orders_v5.OrdersV5.delete_order_custom_field>`,
which sends ``DELETE /modules/api/v5.0/orders/custom-fields/{order_custom_field_id}`` (API V5, on
``wh.route4me.com``). Prints the reply.

Run it with::

    python examples/order/delete_order_custom_field.py --api_key <your key> \\
        --order_custom_field_id <order_custom_field_id>
"""

import argparse

from route4me import Route4Me


def main(api_key, order_custom_field_id):
    """Delete the field and print the reply.

    :param api_key: Route4Me API key.
    :param order_custom_field_id: ID of the order custom field.
    """
    route4me = Route4Me(api_key)

    response = route4me.orders_v5.delete_order_custom_field(order_custom_field_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete Order Custom Field")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--order_custom_field_id",
        dest="order_custom_field_id",
        help="ID of the order custom field",
        type=int,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.order_custom_field_id)
