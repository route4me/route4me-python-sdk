r"""Save one setting of an optimization profile as an entity part.

Calls :meth:`OptimizationProfiles.save_entities
<route4me.optimization_profiles.OptimizationProfiles.save_entities>`, which sends
``POST /modules/api/v5.0/optimization-profiles/save-entities`` (API V5, on ``wh.route4me.com``), and
prints the reply.

Run it with::

    python examples/optimization_profiles/save_entities.py --api_key <your key> \
        --optimization_profile_id <optimization profile ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, optimization_profile_id):
    """Turn on ``append_date_to_route_name`` in the profile and print the reply.

    :param api_key: Route4Me API key.
    :param optimization_profile_id: ID of the optimization profile.
    """
    route4me = Route4Me(api_key)

    response = route4me.optimization_profiles.save_entities(
        items=[
            {
                "id": optimization_profile_id,
                "guid": "example-entity",
                "parts": [{"guid": "example-part", "data": {"append_date_to_route_name": True}}],
            }
        ]
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save Optimization Profile Entities")
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
