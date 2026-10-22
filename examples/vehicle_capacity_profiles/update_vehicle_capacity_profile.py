r"""Change the weight limit of a vehicle capacity profile.

Calls :meth:`VehicleCapacityProfiles.update_vehicle_capacity_profile
<route4me.vehicle_capacity_profiles.VehicleCapacityProfiles.update_vehicle_capacity_profile>`, which
sends ``PATCH /modules/api/v5.0/vehicle-capacity-profiles/{id}`` (API V5, on ``wh.route4me.com``), and
prints the reply.

Run it with::

    python examples/vehicle_capacity_profiles/update_vehicle_capacity_profile.py --api_key <your key> \
        --vehicle_capacity_profile_id <capacity profile ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, vehicle_capacity_profile_id):
    """Set the weight limit of the capacity profile to 1500 kg and print the reply.

    :param api_key: Route4Me API key.
    :param vehicle_capacity_profile_id: ID of the vehicle capacity profile.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicle_capacity_profiles.update_vehicle_capacity_profile(
        vehicle_capacity_profile_id, max_weight=1500, max_weight_unit="kg"
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a Vehicle Capacity Profile")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--vehicle_capacity_profile_id",
        dest="vehicle_capacity_profile_id",
        help="Vehicle capacity profile ID",
        type=int,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.vehicle_capacity_profile_id)
