"""Create an order custom user field (API V4).

Calls :meth:`Order.create_order_custom_user_field <route4me.orders.Order.create_order_custom_user_field>`,
which sends ``POST /api.v4/order_custom_user_fields.php`` with the field as the JSON body. Prints the reply.

Run it with::

    python examples/order/create_order_custom_user_field.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create the field and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.order.create_order_custom_user_field(
        order_custom_field_name="ExampleGateCode",
        order_custom_field_label="Example gate code",
        order_custom_field_type="text",
        order_custom_field_type_info={"short_label": "Gate"},
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Order Custom User Field")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
