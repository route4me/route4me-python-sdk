"""Create several sub-users in one request with API V5.

Calls :meth:`TeamV5.bulk_create_team_members <route4me.team_v5.TeamV5.bulk_create_team_members>`,
which sends ``POST /modules/api/v5.0/team/users/bulk-insert`` (API V5, on ``wh.route4me.com``) with
``users`` and ``conflicts`` (``skip``: leave existing members alone) as the JSON body, and prints the
reply. Running it creates two drivers with sample ``example.com`` email addresses; change the values
first.

Run it with::

    python examples/team/bulk_create_team_members.py --api_key <your key> --owner_member_id <member ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, owner_member_id):
    """Create the two sample drivers and print the reply.

    :param api_key: Route4Me API key.
    :param owner_member_id: member ID of the account owner.
    """
    route4me = Route4Me(api_key)

    team = route4me.team_v5
    users = [
        {
            "member_first_name": "Sample",
            "member_last_name": f"Driver {number}",
            "member_email": f"sample.driver{number}@example.com",
            "member_type": "SUB_ACCOUNT_DRIVER",
            "OWNER_MEMBER_ID": owner_member_id,
        }
        for number in (1, 2)
    ]
    response = team.bulk_create_team_members(users=users, conflicts="skip")
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk Create Team Members (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--owner_member_id", dest="owner_member_id", help="Owner member ID", type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.owner_member_id)
