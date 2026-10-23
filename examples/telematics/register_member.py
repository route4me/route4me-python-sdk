"""Register a member with the telematics service.

Calls :meth:`Telematics.register_member <route4me.telematics.Telematics.register_member>`, which sends
``GET /api.v4/telematics/register.php`` with ``member_id``, and prints the reply, which holds the
member's telematics ``api_token``.

Run it with::

    python examples/telematics/register_member.py --api_key <your key> --member_id <member ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, member_id):
    """Register the member and print the reply.

    :param api_key: Route4Me API key.
    :param member_id: ID of the member.
    """
    route4me = Route4Me(api_key)

    telematics = route4me.telematics
    token = telematics.register_member(member_id)
    telematics.pp_response(token)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Register Telematics Member")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--member_id", dest="member_id", help="Route4Me member_id", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.member_id)
