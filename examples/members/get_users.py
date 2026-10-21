"""List the users of the account.

Calls :meth:`Members.get_users <route4me.members.Members.get_users>` with ``limit=5`` and ``offset=0``,
which sends ``GET /api/member/view_users.php``, and prints the name and email of each user.
get_api_key_users.py lists them with ``GET /api.v4/user.php``.

Run it with::

    python examples/members/get_users.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first five users.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    members = route4me.members
    response = members.get_users(limit=5, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        for i, member in enumerate(response):
            print(f"Member #{i + 1}")
            print(f"\tName: {member.get('member_first_name')}, {member.get('member_last_name')}")
            print(f"\tEmail: {member.get('member_email')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get All Users")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
