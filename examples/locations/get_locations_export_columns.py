"""List the columns a location export can have, with API V5.

Calls :meth:`Locations.get_locations_export_columns
<route4me.locations.Locations.get_locations_export_columns>`, which sends
``POST /modules/api/v5.0/address-book/locations/export/columns`` (API V5, on ``wh.route4me.com``) with
an empty JSON body, and prints the columns.

Run it with::

    python examples/locations/get_locations_export_columns.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the export columns.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    locations = route4me.locations
    response = locations.get_locations_export_columns()
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Locations Export Columns")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
