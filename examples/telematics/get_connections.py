"""List a member's telematics connections.

Calls :meth:`Telematics.register_member <route4me.telematics.Telematics.register_member>`
(``GET /api.v4/telematics/register.php``) to get the member's telematics API token, then
:meth:`Telematics.get_connections <route4me.telematics.Telematics.get_connections>` with it, which sends
``GET /api.v4/telematics/connections.php``, and prints each connection.

Run it with::

    python examples/telematics/get_connections.py --api_key <your key> --member_id <member ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, member_id):
    """Print the telematics connections of the member.

    :param api_key: Route4Me API key.
    :param member_id: ID of the member.
    """
    route4me = Route4Me(api_key)

    telematics = route4me.telematics
    token = telematics.register_member(member_id)

    if "api_token" not in token.keys():
        print(token)
        return

    api_token = token["api_token"]
    connections = telematics.get_connections(api_token)
    if connections:
        for connection in connections:
            telematics.pp_response(connection)
    else:
        print("You currently have no telematics connections")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telematics Vendors Connections")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--member_id", dest="member_id", help="Route4Me member_id", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.member_id)
