"""Delete a user with API V4.

Calls :meth:`Members.user_delete <route4me.members.Members.user_delete>`, which sends
``DELETE /api.v4/user.php`` with ``member_id`` in the query, and prints the reply. Running it
deletes the user. API V5 does the same with ``examples/team/remove_team_member.py``.

Deprecated: Members.user_delete is deprecated, because the C# SDK marks the operation obsolete.
The API V5 replacement is shown in ``examples/team/remove_team_member.py``.

Run it with::

    python examples/members/user_delete.py --api_key <your key> --member_id <member ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, member_id):
    """Delete the user and print the reply.

    :param api_key: Route4Me API key.
    :param member_id: ID of the user.
    """
    route4me = Route4Me(api_key)

    members = route4me.members
    response = members.user_delete(member_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete a User")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--member_id", dest="member_id", help="Member ID", type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.member_id)
