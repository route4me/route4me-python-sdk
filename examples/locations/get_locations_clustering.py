"""Group the address book locations into map clusters with API V5.

Calls :meth:`Locations.get_locations_clustering
<route4me.locations.Locations.get_locations_clustering>` with ``clustering={"zoom": 10}`` and
``with_clusters=True``, which sends ``POST /modules/api/v5.0/address-book/locations/clustering``
(API V5, on ``wh.route4me.com``) with them as the JSON body, and prints the clusters.

Run it with::

    python examples/locations/get_locations_clustering.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the location clusters at zoom level 10.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    locations = route4me.locations
    response = locations.get_locations_clustering(clustering={"zoom": 10}, with_clusters=True)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Locations Clustering")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
