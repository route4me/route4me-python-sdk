"""Create a test vehicle profile.

Calls :meth:`VehicleProfiles.create_vehicle_profile
<route4me.vehicle_profiles.VehicleProfiles.create_vehicle_profile>`, which sends
``POST /modules/api/v5.0/vehicle-profiles`` (API V5, on ``wh.route4me.com``), and prints the reply.

Run it with::

    python examples/vehicle_profiles/create_vehicle_profile.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create the test vehicle profile and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicle_profiles.create_vehicle_profile(
        name="Example truck profile",
        fuel_type="diesel",
        fuel_consumption_city=11,
        fuel_consumption_city_unit="mpg",
        fuel_consumption_highway=8,
        fuel_consumption_highway_unit="mpg",
        vehicle_axle_count=3,
        is_predefined=False,
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Vehicle Profile")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
