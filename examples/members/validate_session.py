"""Check whether a member's session is valid.

Calls :meth:`Members.validate_session <route4me.members.Members.validate_session>` with
``session_guid``, ``member_id`` and ``format``, which sends
``GET /datafeed/session/validate_session.php``, and prints the reply. The session values are samples.

Run it with::

    python examples/members/validate_session.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Validate the sample session and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    members = route4me.members
    data = {"session_guid": "4552222222", "member_id": "1", "format": "json"}
    response = members.validate_session(**data)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Session")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
