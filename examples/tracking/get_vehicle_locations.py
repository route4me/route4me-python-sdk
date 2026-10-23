"""Get the latest known location of one or more vehicles, with API V5.

Calls :meth:`GPS.get_vehicle_locations <route4me.gps.GPS.get_vehicle_locations>`, which sends
``GET /modules/api/v5.0/vehicles/location`` (API V5, on ``wh.route4me.com``) with ``ids[]`` in
the query, and prints the reply.

Run it with::

    python examples/tracking/get_vehicle_locations.py --api_key <your key> --vehicle_id <vehicle ID> ...
"""

import argparse

from route4me import Route4Me


def main(api_key, vehicle_ids):
    """Print the latest location of each vehicle.

    :param api_key: Route4Me API key.
    :param vehicle_ids: IDs of the vehicles.
    """
    route4me = Route4Me(api_key)

    gps = route4me.gps
    response = gps.get_vehicle_locations(vehicle_ids)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Vehicle Locations")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--vehicle_id", dest="vehicle_ids", help="Vehicle ID(s)", type=str, nargs="+", required=True)
    args = parser.parse_args()
    main(args.api_key, args.vehicle_ids)
