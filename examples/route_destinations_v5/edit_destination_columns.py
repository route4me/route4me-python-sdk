r"""Save the order of the destination columns of one column set.

Calls :meth:`RouteDestinationsV5.edit_destination_columns
<route4me.route_destinations_v5.RouteDestinationsV5.edit_destination_columns>`, which sends
``PUT /modules/api/v5.0/route-destinations/columns`` (API V5, on ``wh.route4me.com``) with
``columns_configurator_key`` and ``order`` as the JSON body, and prints the saved order.

Run it with::

    python examples/route_destinations_v5/edit_destination_columns.py --api_key <your key> \
        --columns_configurator_key <columns configurator key> --column <column> [--column ...]
"""

import argparse

from route4me import Route4Me


def main(api_key, columns_configurator_key, column):
    """Save the column order and print the reply.

    :param api_key: Route4Me API key.
    :param columns_configurator_key: key of the column set.
    :param column: column name, in display order; repeat for each column.
    """
    route4me = Route4Me(api_key)

    response = route4me.route_destinations_v5.edit_destination_columns(
        columns_configurator_key=columns_configurator_key, order=column
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Edit Destination Columns (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--columns_configurator_key",
        dest="columns_configurator_key",
        help="Key of the column set",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--column",
        dest="column",
        help="Column name, in display order; repeat for each column",
        type=str,
        action="append",
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.columns_configurator_key, args.column)
