r"""List the territories that contain a point, with their address counts (API V5).

Calls :meth:`TerritoriesV5.get_territories <route4me.territories_v5.TerritoriesV5.get_territories>`,
which sends ``GET /modules/api/v5.0/territories`` (API V5, on ``wh.route4me.com``) with ``lat``,
``lng`` and ``addresses_count=1`` in the query, and prints the reply.

Run it with::

    python examples/territory/get_territories_v5.py --api_key <your key> --lat <lat> --lng <lng>
"""

import argparse

from route4me import Route4Me


def main(api_key, lat, lng):
    """Print the territories that contain the point.

    :param api_key: Route4Me API key.
    :param lat: latitude of the point.
    :param lng: longitude of the point.
    """
    route4me = Route4Me(api_key)

    response = route4me.territories_v5.get_territories(lat=lat, lng=lng, addresses_count=True)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Territories (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--lat", dest="lat", help="Latitude of the point", type=float, required=True)
    parser.add_argument("--lng", dest="lng", help="Longitude of the point", type=float, required=True)
    args = parser.parse_args()
    main(args.api_key, args.lat, args.lng)
