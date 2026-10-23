"""Get one location type with API V5.

Calls :meth:`Locations.get_location_type_by_id <route4me.locations.Locations.get_location_type_by_id>`,
which sends ``GET /modules/api/v5.0/address-book/locations/types/{location_type_id}`` (API V5, on
``wh.route4me.com``), and prints the location type.

Run it with::

    python examples/locations/get_location_type_by_id.py --api_key <your key> --location_type_id <type ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, location_type_id):
    """Print one location type.

    :param api_key: Route4Me API key.
    :param location_type_id: ID of the location type.
    """
    route4me = Route4Me(api_key)

    locations = route4me.locations
    response = locations.get_location_type_by_id(location_type_id)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Location Type")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--location_type_id", dest="location_type_id", help="Location type ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.location_type_id)
