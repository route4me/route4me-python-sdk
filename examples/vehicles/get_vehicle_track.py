"""Get the track of one vehicle for one day.

Calls :meth:`VehiclesV5.get_vehicle_track <route4me.vehicles_v5.VehiclesV5.get_vehicle_track>`, which
sends ``GET /modules/api/v5.0/vehicles/{vehicle_id}/track`` (API V5, on ``wh.route4me.com``), and prints
the reply.

Run it with::

    python examples/vehicles/get_vehicle_track.py --api_key <your key> --vehicle_id <vehicle ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, vehicle_id):
    """Print the track of the vehicle on 2026-10-01.

    :param api_key: Route4Me API key.
    :param vehicle_id: ID of the vehicle.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicles_v5.get_vehicle_track(vehicle_id, start="2026-10-01", end="2026-10-02")
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Vehicle Track")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--vehicle_id", dest="vehicle_id", help="Vehicle ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.vehicle_id)
