r"""Find a vehicle by its license plate.

Calls :meth:`VehiclesV5.get_vehicle_by_license_plate
<route4me.vehicles_v5.VehiclesV5.get_vehicle_by_license_plate>`, which sends
``GET /modules/api/v5.0/vehicles/license`` (API V5, on ``wh.route4me.com``), and prints the reply.

Run it with::

    python examples/vehicles/get_vehicle_by_license_plate.py --api_key <your key> \
        --license_plate <license plate>
"""

import argparse

from route4me import Route4Me


def main(api_key, license_plate):
    """Print the vehicle that has the license plate.

    :param api_key: Route4Me API key.
    :param license_plate: license plate of the vehicle.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicles_v5.get_vehicle_by_license_plate(vehicle_license_plate=license_plate)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Vehicle by License Plate")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--license_plate", dest="license_plate", help="License plate of the vehicle", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.license_plate)
