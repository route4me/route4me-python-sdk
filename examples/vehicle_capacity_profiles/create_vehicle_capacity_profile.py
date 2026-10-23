"""Create a test vehicle capacity profile.

Calls :meth:`VehicleCapacityProfiles.create_vehicle_capacity_profile
<route4me.vehicle_capacity_profiles.VehicleCapacityProfiles.create_vehicle_capacity_profile>`, which
sends ``POST /modules/api/v5.0/vehicle-capacity-profiles`` (API V5, on ``wh.route4me.com``), and prints
the reply.

Run it with::

    python examples/vehicle_capacity_profiles/create_vehicle_capacity_profile.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create the test capacity profile and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicle_capacity_profiles.create_vehicle_capacity_profile(
        name="Example capacity profile",
        max_weight=1200,
        max_weight_unit="kg",
        max_volume=12,
        max_volume_unit="m3",
        max_items_number=150,
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Vehicle Capacity Profile")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
