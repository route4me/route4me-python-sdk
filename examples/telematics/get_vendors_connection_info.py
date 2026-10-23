"""Get information on the telematics vendors a member is connected to.

Calls :meth:`Telematics.register_member <route4me.telematics.Telematics.register_member>`
(``GET /api.v4/telematics/register.php``) to get the member's telematics API token, then
:meth:`Telematics.get_vendors_info <route4me.telematics.Telematics.get_vendors_info>` with it, which
sends ``GET /api.v4/telematics/vendors.php``, and prints each vendor connection.

Run it with::

    python examples/telematics/get_vendors_connection_info.py --api_key <your key> --member_id <member ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, member_id):
    """Print the vendor connections of the member.

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
    vendor_connections = telematics.get_vendors_info(api_token)
    for vendor_connection in vendor_connections:
        telematics.pp_response(vendor_connection)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Telematics Vendors Connection Information")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--member_id", dest="member_id", help="Route4Me member_id", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.member_id)
