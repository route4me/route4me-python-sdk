"""Create an order, then read it back.

Calls :meth:`Order.create_order <route4me.orders.Order.create_order>` (``POST /api.v4/order.php``), then
:meth:`Order.get_order <route4me.orders.Order.get_order>` with its ``order_id``, which sends
``GET /api.v4/order.php``, and prints the order. The order stays in the account; delete_order.py shows
how to remove one.

Run it with::

    python examples/order/get_order.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create an order and print it as read back.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    order = route4me.order
    url = "http://www.bk.com/restaurants/ny/new-york/106-fulton-st-17871.html"
    data = {
        "address_1": "106 Fulton St, Farmingdale, NY 11735, USA",
        "cached_lat": 40.730730,
        "cached_lng": -73.459283,
        "address_alias": "BK Restaurant #: 17871",
        "EXT_FIELD_phone": "(212) 566-5132",
        "day_scheduled_for_YYMMDD": "2016-07-01",
        "EXT_FIELD_custom_data": {
            "url": url,
        },
    }
    response = order.create_order(**data)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        order_id = response.get("order_id")
        if order_id:
            response = order.get_order(order_id=order_id)
            print(f"Member ID:\t{response.get('member_id')}")
            print(f"Order ID:\t{response.get('order_id')}")
            print(f"Order Status ID:\t{response.get('order_status_id')}")
            print(f"In Route Count:\t{response.get('in_route_count')}")
            print(f"Day Added:\t{response.get('day_added_YYMMDD')}")
            print(f"Is Pending:\t{response.get('is_pending')}")
            print(f"Is Accepted:\t{response.get('is_accepted')}")
            print(f"Is Started:\t{response.get('is_started')}")
            print(f"Is Validated:\t{response.get('is_validated')}")
            print(f"Is Completed:\t{response.get('is_completed')}")
        else:
            print("Error Getting Order")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get an Order")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
