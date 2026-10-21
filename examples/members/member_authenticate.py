"""Authenticate a member with an email address and a password.

Calls :meth:`Members.member_authenticate <route4me.members.Members.member_authenticate>`, which sends
``POST /actions/authenticate.php`` with ``strEmail``, ``strPassword`` and ``format`` as the JSON body,
and prints the reply. The credentials are samples; use those of a member of your account.

Run it with::

    python examples/members/member_authenticate.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Authenticate the sample member and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    members = route4me.members
    data = {"email": "john@route4me.com", "password": "ultrasecretword", "format": "json"}
    response = members.member_authenticate(**data)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Member Authentication")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
