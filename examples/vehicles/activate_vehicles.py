r"""Activate several vehicles, as an asynchronous job.

Calls :meth:`VehiclesV5.activate_vehicles <route4me.vehicles_v5.VehiclesV5.activate_vehicles>`, which
sends ``POST /modules/api/v5.0/vehicles/bulk/activate`` (API V5, on ``wh.route4me.com``), and prints the
reply.

The API runs the job in the background; pass the printed ``job_id`` to get_vehicle_job_status.py to
follow it.

Run it with::

    python examples/vehicles/activate_vehicles.py --api_key <your key> \
        --vehicle_ids <vehicle ID> <vehicle ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, vehicle_ids):
    """Start the activation job and print its ID.

    :param api_key: Route4Me API key.
    :param vehicle_ids: IDs of the vehicles.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicles_v5.activate_vehicles(vehicle_ids=vehicle_ids)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Activate Vehicles")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--vehicle_ids", dest="vehicle_ids", help="One or more vehicle IDs", type=str, required=True, nargs="+"
    )
    args = parser.parse_args()
    main(args.api_key, args.vehicle_ids)
