"""List the location types with API V5.

Calls :meth:`Locations.get_location_types <route4me.locations.Locations.get_location_types>` with
``page=1`` and ``per_page=10``, which sends ``GET /modules/api/v5.0/address-book/locations/types``
(API V5, on ``wh.route4me.com``) with them in the query, and prints the ID and name of each type.

Run it with::

    python examples/locations/get_location_types.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first ten location types.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    locations = route4me.locations
    response = locations.get_location_types(page=1, per_page=10)
    if isinstance(response, dict) and "errors" in response.keys():
        print(response["errors"])
    else:
        for location_type in response.get("data", []):
            print(f"{location_type.get('location_type_id')}\t{location_type.get('name')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Location Types")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
