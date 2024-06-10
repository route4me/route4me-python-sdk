# -*- coding: utf-8 -*-
# codebeat:disable[ABC]

import argparse

from route4me import Route4Me


def main(api_key):
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
    parser = argparse.ArgumentParser(description="Get Optimizations Profile")
    parser.add_argument(
        "--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key)

# codebeat:enable[ABC]
