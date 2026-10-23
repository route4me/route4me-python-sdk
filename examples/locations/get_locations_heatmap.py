"""Get a heat map of the address book locations with API V5.

Calls :meth:`Locations.get_locations_heatmap <route4me.locations.Locations.get_locations_heatmap>`
with ``zoom=10``, which sends ``POST /modules/api/v5.0/address-book/locations/heatmap`` (API V5, on
``wh.route4me.com``) with it as the JSON body, and prints the heat map.

Run it with::

    python examples/locations/get_locations_heatmap.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the location heat map at zoom level 10.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    locations = route4me.locations
    response = locations.get_locations_heatmap(zoom=10)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Locations Heatmap")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
