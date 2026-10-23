r"""Get the destination columns of one column set.

Calls :meth:`RouteDestinationsV5.get_destination_columns
<route4me.route_destinations_v5.RouteDestinationsV5.get_destination_columns>`, which sends
``GET /modules/api/v5.0/route-destinations/columns`` (API V5, on ``wh.route4me.com``) with
``columns_configurator_key`` in the query, and prints the reply.

Run it with::

    python examples/route_destinations_v5/get_destination_columns.py --api_key <your key> \
        --columns_configurator_key <columns configurator key>
"""

import argparse

from route4me import Route4Me


def main(api_key, columns_configurator_key):
    """Print the columns of the column set and their order.

    :param api_key: Route4Me API key.
    :param columns_configurator_key: key of the column set.
    """
    route4me = Route4Me(api_key)

    response = route4me.route_destinations_v5.get_destination_columns(columns_configurator_key)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Destination Columns (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--columns_configurator_key",
        dest="columns_configurator_key",
        help="Key of the column set",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.columns_configurator_key)
