"""List the account's vehicles.

Calls :meth:`Vehicle.get_vehicles <route4me.vehicles.Vehicle.get_vehicles>`, which sends
``GET /api/vehicles/view_vehicles.php``, and prints the ID and alias of each vehicle.

Run it with::

    python examples/vehicles/get_vehicles.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print every vehicle.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    vehicles = route4me.vehicles
    response = vehicles.get_vehicles()
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response.get("errors")))
    else:
        for vehicle in response:
            print(f"Vehicle ID: {vehicle.get('vehicle_id')}\tVehicle Alias: {vehicle.get('vehicle_alias')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Vehicles")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
