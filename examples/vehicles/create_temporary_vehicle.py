r"""Assign a vehicle to a member for the next two days.

Calls :meth:`VehiclesV5.create_temporary_vehicle
<route4me.vehicles_v5.VehiclesV5.create_temporary_vehicle>`, which sends
``POST /modules/api/v5.0/vehicles/assign`` (API V5, on ``wh.route4me.com``), and prints the reply.

Run it with::

    python examples/vehicles/create_temporary_vehicle.py --api_key <your key> \
        --vehicle_id <vehicle ID> --member_id <member ID>
"""

import argparse
import time

from route4me import Route4Me


def main(api_key, vehicle_id, member_id):
    """Assign the vehicle to the member until two days from now and print the reply.

    :param api_key: Route4Me API key.
    :param vehicle_id: ID of the vehicle.
    :param member_id: ID of the member who gets the vehicle.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicles_v5.create_temporary_vehicle(
        vehicle_id=vehicle_id,
        assigned_member_id=member_id,
        expires_at=int(time.time()) + 2 * 24 * 3600,
        **{"force-assignment": False},
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Temporary Vehicle")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--vehicle_id", dest="vehicle_id", help="Vehicle ID", type=str, required=True)
    parser.add_argument(
        "--member_id", dest="member_id", help="ID of the member who gets the vehicle", type=int, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.vehicle_id, args.member_id)
