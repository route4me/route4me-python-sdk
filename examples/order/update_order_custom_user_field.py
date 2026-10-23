"""Rename an order custom user field (API V4).

Calls :meth:`Order.update_order_custom_user_field <route4me.orders.Order.update_order_custom_user_field>`,
which sends ``PUT /api.v4/order_custom_user_fields.php`` with the field ID and the new label as the JSON body.
Prints the reply.

Run it with::

    python examples/order/update_order_custom_user_field.py --api_key <your key> \\
        --order_custom_field_id <order_custom_field_id>
"""

import argparse

from route4me import Route4Me


def main(api_key, order_custom_field_id):
    """Change the label of the field and print the reply.

    :param api_key: Route4Me API key.
    :param order_custom_field_id: ID of the order custom user field.
    """
    route4me = Route4Me(api_key)

    response = route4me.order.update_order_custom_user_field(
        order_custom_field_id=order_custom_field_id,
        order_custom_field_label="Example gate code (updated)",
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Order Custom User Field")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--order_custom_field_id",
        dest="order_custom_field_id",
        help="ID of the order custom user field",
        type=int,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.order_custom_field_id)
