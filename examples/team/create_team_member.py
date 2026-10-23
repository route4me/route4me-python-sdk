"""Create a sub-user with API V5.

Calls :meth:`TeamV5.create_team_member <route4me.team_v5.TeamV5.create_team_member>`, which sends
``POST /modules/api/v5.0/team/users`` (API V5, on ``wh.route4me.com``) with the member as the JSON
body, and prints the new member. ``owner_member_id`` is the member ID of the account owner. Running it
creates a driver with a sample ``example.com`` email address; change the values first.

Run it with::

    python examples/team/create_team_member.py --api_key <your key> --owner_member_id <member ID>
"""

import argparse
import json

from route4me import Route4Me


def main(api_key, owner_member_id):
    """Create the sample driver and print it.

    :param api_key: Route4Me API key.
    :param owner_member_id: member ID of the account owner.
    """
    route4me = Route4Me(api_key)

    team = route4me.team_v5
    response = team.create_team_member(
        member_first_name="Sample",
        member_last_name="Driver",
        member_email="sample.driver@example.com",
        member_type="SUB_ACCOUNT_DRIVER",
        OWNER_MEMBER_ID=owner_member_id,
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Team Member (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--owner_member_id", dest="owner_member_id", help="Owner member ID", type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.owner_member_id)
