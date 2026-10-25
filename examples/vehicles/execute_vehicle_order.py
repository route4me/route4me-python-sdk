"""Execute the order of a vehicle at a location.

Calls :meth:`VehiclesV5.execute_vehicle_order <route4me.vehicles_v5.VehiclesV5.execute_vehicle_order>`,
which sends ``POST /modules/api/v5.0/vehicles/execute`` (API V5, on ``wh.route4me.com``), and prints the
reply.

Run it with::

    python examples/vehicles/execute_vehicle_order.py --api_key <your key> --vehicle_id <vehicle ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, vehicle_id):
    """Execute the order of the vehicle at a sample location and print the reply.

    :param api_key: Route4Me API key.
    :param vehicle_id: ID of the vehicle.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicles_v5.execute_vehicle_order(vehicle_id=vehicle_id, lat=40.7128, lng=-74.006)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute a Vehicle Order")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--vehicle_id", dest="vehicle_id", help="Vehicle ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.vehicle_id)
