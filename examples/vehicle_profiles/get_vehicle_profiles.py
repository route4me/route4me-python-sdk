"""List the first ten vehicle profiles.

Calls :meth:`VehicleProfiles.get_vehicle_profiles
<route4me.vehicle_profiles.VehicleProfiles.get_vehicle_profiles>`, which sends
``GET /modules/api/v5.0/vehicle-profiles`` (API V5, on ``wh.route4me.com``), and prints the reply.

Run it with::

    python examples/vehicle_profiles/get_vehicle_profiles.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first page of ten vehicle profiles.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicle_profiles.get_vehicle_profiles(with_pagination=True, page=1, per_page=10)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Vehicle Profiles")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
