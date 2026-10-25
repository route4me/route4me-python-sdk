"""List the users of the account that the API key belongs to.

Calls :meth:`Members.get_api_key_users <route4me.members.Members.get_api_key_users>`, which sends
``GET /api.v4/user.php``. The users come back under ``results``; each is printed with its member ID,
name, email and type.

Deprecated: Members.get_api_key_users is deprecated, because the C# SDK marks the operation obsolete.
The API V5 replacement is shown in ``examples/team/get_team_members.py``.

Run it with::

    python examples/members/get_api_key_users.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the users of the account.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    members = route4me.members
    response = members.get_api_key_users()
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        for i, member in enumerate(response.get("results", [])):
            print(f"Member #{i + 1}")
            print(f"\tMember ID: {member.get('member_id')}")
            print(f"\tName: {member.get('member_first_name')} {member.get('member_last_name')}")
            print(f"\tEmail: {member.get('member_email')}")
            print(f"\tType: {member.get('member_type')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the Users of the API Key")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
