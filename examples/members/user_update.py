"""Update a user with API V4.

Calls :meth:`Members.user_update <route4me.members.Members.user_update>`, which sends
``PUT /api.v4/user.php`` with ``member_id`` in the query and ``member_phone`` as the JSON body, and
prints the updated user. API V5 does the same with ``examples/team/update_team_member.py``.

Deprecated: Members.user_update is deprecated, because the C# SDK marks the operation obsolete.
The API V5 replacement is shown in ``examples/team/update_team_member.py``.

Run it with::

    python examples/members/user_update.py --api_key <your key> --member_id <member ID>
"""

import argparse
import json

from route4me import Route4Me


def main(api_key, member_id):
    """Change the user's phone number and print the user.

    :param api_key: Route4Me API key.
    :param member_id: ID of the user.
    """
    route4me = Route4Me(api_key)

    members = route4me.members
    response = members.user_update(member_id, member_phone="555-0100")
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(json.dumps(response, indent=2) if isinstance(response, (dict, list)) else response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a User")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--member_id", dest="member_id", help="Member ID", type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.member_id)
