"""List address book locations with their column configuration, with API V5.

Calls :meth:`Locations.get_locations_combined <route4me.locations.Locations.get_locations_combined>`
with ``page=1`` and ``per_page=10``, which sends
``POST /modules/api/v5.0/address-book/locations/list/combined`` (API V5, on ``wh.route4me.com``) with
them as the JSON body, and prints the reply.

Run it with::

    python examples/locations/get_locations_combined.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first ten locations and the column configuration.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    locations = route4me.locations
    response = locations.get_locations_combined(page=1, per_page=10)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Locations Combined")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
