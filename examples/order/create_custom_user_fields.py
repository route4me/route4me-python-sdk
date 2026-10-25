"""Create an order custom user field (API V5).

Calls :meth:`OrdersV5.create_custom_user_fields <route4me.orders_v5.OrdersV5.create_custom_user_fields>`,
which sends ``POST /modules/api/v5.0/orders-platform/order-custom-user-fields`` (API V5, on
``wh.route4me.com``) with the field as the JSON body. Prints the reply.

Run it with::

    python examples/order/create_custom_user_fields.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create the field and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.orders_v5.create_custom_user_fields(
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
    parser = argparse.ArgumentParser(description="Create Custom User Fields")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
