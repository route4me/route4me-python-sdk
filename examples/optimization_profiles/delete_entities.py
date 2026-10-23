r"""Delete the entities of an optimization profile.

Calls :meth:`OptimizationProfiles.delete_entities
<route4me.optimization_profiles.OptimizationProfiles.delete_entities>`, which sends
``POST /modules/api/v5.0/optimization-profiles/delete-entities`` (API V5, on ``wh.route4me.com``), and
prints the reply.

Run it with::

    python examples/optimization_profiles/delete_entities.py --api_key <your key> \
        --optimization_profile_id <optimization profile ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, optimization_profile_id):
    """Delete the entities of the optimization profile and print the reply.

    :param api_key: Route4Me API key.
    :param optimization_profile_id: ID of the optimization profile.
    """
    route4me = Route4Me(api_key)

    response = route4me.optimization_profiles.delete_entities(items=[{"id": optimization_profile_id}])
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete Optimization Profile Entities")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--optimization_profile_id",
        dest="optimization_profile_id",
        help="Optimization profile ID",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.optimization_profile_id)
