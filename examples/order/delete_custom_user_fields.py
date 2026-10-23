"""Delete an order custom user field (API V5).

Calls :meth:`OrdersV5.delete_custom_user_fields <route4me.orders_v5.OrdersV5.delete_custom_user_fields>`,
which sends ``DELETE /modules/api/v5.0/orders-platform/order-custom-user-fields/{order_custom_field_uuid}``
(API V5, on ``wh.route4me.com``). Prints the reply.

Run it with::

    python examples/order/delete_custom_user_fields.py --api_key <your key> \\
        --order_custom_field_uuid <order_custom_field_uuid>
"""

import argparse

from route4me import Route4Me


def main(api_key, order_custom_field_uuid):
    """Delete the field and print the reply.

    :param api_key: Route4Me API key.
    :param order_custom_field_uuid: UUID of the order custom user field.
    """
    route4me = Route4Me(api_key)

    response = route4me.orders_v5.delete_custom_user_fields(order_custom_field_uuid)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete Custom User Fields")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--order_custom_field_uuid",
        dest="order_custom_field_uuid",
        help="UUID of the order custom user field",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.order_custom_field_uuid)
