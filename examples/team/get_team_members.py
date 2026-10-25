"""List the sub-users of the account with API V5.

Calls :meth:`TeamV5.get_team_members <route4me.team_v5.TeamV5.get_team_members>`, which sends
``GET /modules/api/v5.0/team/users`` (API V5, on ``wh.route4me.com``), optionally with a ``query``
search phrase, and prints the ID, name and type of each member.

Run it with::

    python examples/team/get_team_members.py --api_key <your key> [--query <search phrase>]
"""

import argparse

from route4me import Route4Me


def main(api_key, query=None):
    """Print the members of the team.

    :param api_key: Route4Me API key.
    :param query: search phrase to filter the members by, or ``None`` for all of them.
    """
    route4me = Route4Me(api_key)

    team = route4me.team_v5
    filters = {} if query is None else {"query": query}
    response = team.get_team_members(**filters)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        for member in response:
            name = f"{member.get('member_first_name')} {member.get('member_last_name')}"
            print(f"{member.get('member_id')}\t{name}\t{member.get('member_type')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Team Members (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--query", dest="query", help="Search phrase", type=str)
    args = parser.parse_args()
    main(args.api_key, args.query)
