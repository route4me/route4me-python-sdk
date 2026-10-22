"""Create a test optimization profile.

Calls :meth:`OptimizationProfiles.create_optimization_profile
<route4me.optimization_profiles.OptimizationProfiles.create_optimization_profile>`, which sends
``POST /modules/api/v5.0/optimization-profiles`` (API V5, on ``wh.route4me.com``), and prints the reply.

Run it with::

    python examples/optimization_profiles/create_optimization_profile.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create the test optimization profile and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.optimization_profiles.create_optimization_profile(
        profile_name="Example optimization profile",
        is_default=False,
        optimization_type="multi",
        route_end_mode="rt",
        avoid_tolls=True,
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an Optimization Profile")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
