"""Change the alias of one vehicle.

Calls :meth:`VehiclesV5.update_vehicle <route4me.vehicles_v5.VehiclesV5.update_vehicle>`, which sends
``PATCH /modules/api/v5.0/vehicles/{vehicle_id}`` (API V5, on ``wh.route4me.com``) with the changed
fields as the JSON body, and prints the reply.

Run it with::

    python examples/vehicles/update_vehicle.py --api_key <your key> --vehicle_id <vehicle ID> --alias <new alias>
"""

import argparse

from route4me import Route4Me


def main(api_key, vehicle_id, alias):
    """Rename the vehicle and print the reply.

    :param api_key: Route4Me API key.
    :param vehicle_id: ID of the vehicle.
    :param alias: the new vehicle alias.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicles_v5.update_vehicle(vehicle_id, vehicle_alias=alias)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a Vehicle (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--vehicle_id", dest="vehicle_id", help="Vehicle ID", type=str, required=True)
    parser.add_argument("--alias", dest="alias", help="New vehicle alias", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.vehicle_id, args.alias)
