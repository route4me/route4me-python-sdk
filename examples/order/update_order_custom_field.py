"""Relabel an order custom field.

Calls :meth:`OrdersV5.update_order_custom_field <route4me.orders_v5.OrdersV5.update_order_custom_field>`,
which sends ``PUT /modules/api/v5.0/orders/custom-fields/{order_custom_field_id}`` (API V5, on
``wh.route4me.com``) with the new label as the JSON body. Prints the reply.

Run it with::

    python examples/order/update_order_custom_field.py --api_key <your key> \\
        --order_custom_field_id <order_custom_field_id>
"""

import argparse

from route4me import Route4Me


def main(api_key, order_custom_field_id):
    """Update the field and print the reply.

    :param api_key: Route4Me API key.
    :param order_custom_field_id: ID of the order custom field.
    """
    route4me = Route4Me(api_key)

    response = route4me.orders_v5.update_order_custom_field(
        order_custom_field_id,
        order_custom_field_label="Example gate code (updated)",
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Order Custom Field")
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
