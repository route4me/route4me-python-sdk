"""Create a test vehicle with API V5.

Calls :meth:`VehiclesV5.create_vehicle <route4me.vehicles_v5.VehiclesV5.create_vehicle>`, which sends
``POST /modules/api/v5.0/vehicles`` (API V5, on ``wh.route4me.com``), and prints the reply.

Run it with::

    python examples/vehicles/create_vehicle.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create the test vehicle and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicles_v5.create_vehicle(
        vehicle_alias="Example van",
        vehicle_license_plate="TEST123",
        vehicle_make="Example",
        vehicle_model="Van",
        vehicle_type_id="van",
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Vehicle (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
