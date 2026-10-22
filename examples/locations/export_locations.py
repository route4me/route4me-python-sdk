"""Start a CSV export of the address book locations with API V5.

Calls :meth:`Locations.export_locations <route4me.locations.Locations.export_locations>` with
``format="csv"`` and ``filename="locations"``, which sends
``POST /modules/api/v5.0/address-book/locations/export`` (API V5, on ``wh.route4me.com``) with them as
the JSON body. The API accepts the export with ``202 Accepted`` and prepares the file in the
background; the example prints the reply.

Run it with::

    python examples/locations/export_locations.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Start the export and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    locations = route4me.locations
    response = locations.export_locations(format="csv", filename="locations")
    if isinstance(response, dict) and "errors" in response.keys():
        print(response["errors"])
    else:
        print(f"Export accepted: {response!r}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Locations")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
