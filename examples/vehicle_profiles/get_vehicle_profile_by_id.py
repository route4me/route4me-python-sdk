r"""Get one vehicle profile by its ID.

Calls :meth:`VehicleProfiles.get_vehicle_profile_by_id
<route4me.vehicle_profiles.VehicleProfiles.get_vehicle_profile_by_id>`, which sends
``GET /modules/api/v5.0/vehicle-profiles/{vehicle_profile_id}`` (API V5, on ``wh.route4me.com``), and
prints the reply.

Run it with::

    python examples/vehicle_profiles/get_vehicle_profile_by_id.py --api_key <your key> \
        --vehicle_profile_id <vehicle profile ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, vehicle_profile_id):
    """Print the vehicle profile.

    :param api_key: Route4Me API key.
    :param vehicle_profile_id: ID of the vehicle profile.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicle_profiles.get_vehicle_profile_by_id(vehicle_profile_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Vehicle Profile")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--vehicle_profile_id", dest="vehicle_profile_id", help="Vehicle profile ID", type=int, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.vehicle_profile_id)
