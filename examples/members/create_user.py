"""Create a user (a sub-user of the account) with API V4.

Calls :meth:`Members.create_user <route4me.members.Members.create_user>`, which sends
``POST /api.v4/user.php`` with the user as the JSON body, and prints the new user.
``owner_member_id`` is the member ID of the account owner. Running it creates a dispatcher with a
sample ``example.com`` email address; change the values first. API V5 does the same with
``examples/team/create_team_member.py``.

Deprecated: Members.create_user is deprecated, because the C# SDK marks the operation obsolete.
The API V5 replacement is shown in ``examples/team/create_team_member.py``.

Run it with::

    python examples/members/create_user.py --api_key <your key> --owner_member_id <member ID>
"""

import argparse
import json

from route4me import Route4Me


def main(api_key, owner_member_id):
    """Create the sample user and print it.

    :param api_key: Route4Me API key.
    :param owner_member_id: member ID of the account owner.
    """
    route4me = Route4Me(api_key)

    members = route4me.members
    response = members.create_user(
        member_first_name="Sample",
        member_last_name="Dispatcher",
        member_email="sample.dispatcher@example.com",
        member_type="SUB_ACCOUNT_DISPATCHER",
        OWNER_MEMBER_ID=owner_member_id,
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(json.dumps(response, indent=2) if isinstance(response, (dict, list)) else response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a User")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--owner_member_id", dest="owner_member_id", help="Owner member ID", type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.owner_member_id)
