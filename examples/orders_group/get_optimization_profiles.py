"""List the optimization profiles.

Calls :meth:`OptimizationProfiles.get_optimization_profiles
<route4me.optimization_profiles.OptimizationProfiles.get_optimization_profiles>`, which sends
``GET /modules/api/v5.0/optimization-profiles/data-list`` (API V5, on ``wh.route4me.com``), and prints
the ID and name of each profile, and whether it is the default.

Run it with::

    python examples/orders_group/get_optimization_profiles.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print every optimization profile.

    :param api_key: Route4Me API key.
    """
    r4m = Route4Me(api_key)
    optimization_profiles = r4m.optimization_profiles

    print("\nGetting Optimization Profiles:\n")
    profiles = optimization_profiles.get_optimization_profiles()

    for profile in profiles.get("items", []):
        print(
            " - ".join(
                [
                    f"ID: {profile['optimization_profile_id']}",
                    f"ProfileName: {profile['profile_name']}",
                    f"isDefault: {profile['is_default']}",
                ]
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Optimization Profiles")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
