"""Update a sub-user, and give a driver skills, with API V5.

Calls :meth:`TeamV5.update_team_member <route4me.team_v5.TeamV5.update_team_member>`, which sends
``PATCH /modules/api/v5.0/team/users/{user_id}`` (API V5, on ``wh.route4me.com``) with
``member_email`` and ``custom_data`` as the JSON body, and prints the updated member. The driver
skills go in ``custom_data["driver_skills"]``, comma-separated.

Run it with::

    python examples/team/update_team_member.py --api_key <your key> --user_id <member ID> \\
        --member_email <the member's email>
"""

import argparse
import json

from route4me import Route4Me


def main(api_key, user_id, member_email):
    """Give the member two sample skills and print it.

    :param api_key: Route4Me API key.
    :param user_id: ID of the member.
    :param member_email: email address of the member, which the API requires.
    """
    route4me = Route4Me(api_key)

    team = route4me.team_v5
    response = team.update_team_member(
        user_id,
        member_email=member_email,
        custom_data={"driver_skills": "Forklift,Refrigerated"},
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a Team Member (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--user_id", dest="user_id", help="Member ID", type=int, required=True)
    parser.add_argument("--member_email", dest="member_email", help="Member email", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.user_id, args.member_email)
