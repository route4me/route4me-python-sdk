"""Give every order scheduled on a date the same color, in the background.

Calls :meth:`OrdersV5.batch_update_filter <route4me.orders_v5.OrdersV5.batch_update_filter>`, which sends
``PUT /modules/api/v5.0/orders-platform/batch-update/filter`` (API V5, on ``wh.route4me.com``) with ``data``
and ``filters`` as the JSON body. Prints the reply.

Run it with::

    python examples/order/batch_update_filter.py --api_key <your key> --scheduled_for <scheduled_for>
"""

import argparse

from route4me import Route4Me


def main(api_key, scheduled_for):
    """Start the update and print the reply.

    :param api_key: Route4Me API key.
    :param scheduled_for: The scheduled date, as YYYY-MM-DD.
    """
    route4me = Route4Me(api_key)

    response = route4me.orders_v5.batch_update_filter(
        data={"color": "ff0000"},
        filters={"scheduled_for_range": [scheduled_for, scheduled_for]},
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Update Orders by Filter")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--scheduled_for", dest="scheduled_for", help="The scheduled date, as YYYY-MM-DD", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.scheduled_for)
