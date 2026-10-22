"""Rename a vehicle through the bulk update, an asynchronous job.

Calls :meth:`VehiclesV5.update_vehicles <route4me.vehicles_v5.VehiclesV5.update_vehicles>`, which sends
``POST /modules/api/v5.0/vehicles/bulk/update`` (API V5, on ``wh.route4me.com``), and prints the reply.

The API runs the job in the background; pass the printed ``job_id`` to get_vehicle_job_status.py to
follow it.

Run it with::

    python examples/vehicles/update_vehicles.py --api_key <your key> --vehicle_id <vehicle ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, vehicle_id):
    """Start the update job and print its ID.

    :param api_key: Route4Me API key.
    :param vehicle_id: ID of the vehicle.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicles_v5.update_vehicles(
        vehicles=[{"vehicle_id": vehicle_id, "vehicle_alias": "Renamed example van"}]
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Vehicles")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--vehicle_id", dest="vehicle_id", help="Vehicle ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.vehicle_id)
