"""Remove a sub-user with API V5.

Calls :meth:`TeamV5.remove_team_member <route4me.team_v5.TeamV5.remove_team_member>`, which sends
``DELETE /modules/api/v5.0/team/users/{user_id}`` (API V5, on ``wh.route4me.com``), and prints the
removed member. Running it deletes the member.

Run it with::

    python examples/team/remove_team_member.py --api_key <your key> --user_id <member ID>
"""

import argparse
import json

from route4me import Route4Me


def main(api_key, user_id):
    """Remove the member and print it.

    :param api_key: Route4Me API key.
    :param user_id: ID of the member.
    """
    route4me = Route4Me(api_key)

    team = route4me.team_v5
    response = team.remove_team_member(user_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove a Team Member (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--user_id", dest="user_id", help="Member ID", type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.user_id)
