r"""Connect a member to a telematics vendor.

Calls :meth:`Telematics.register_member <route4me.telematics.Telematics.register_member>`
(``GET /api.v4/telematics/register.php``) to get the member's telematics API token, reads the vendor
credentials from a JSON file shaped like ``vendor_credentials.json``, and calls
:meth:`Telematics.register_connection <route4me.telematics.Telematics.register_connection>`, which sends
``POST /api.v4/telematics/connections.php`` with the credentials and
``validate_remote_credentials="true"`` as the JSON body. Prints the new connection. The values in
``vendor_credentials.json`` are samples.

Run it with::

    python examples/telematics/register_vendor_connection.py --api_key <your key> --member_id <member ID> \
        --vendor_credentials examples/telematics/vendor_credentials.json
"""

import argparse
import json

from route4me import Route4Me


def _load_credentials(fn):
    """Read the vendor credentials from a JSON file.

    :param fn: path of the file.
    :return: the credentials, as a dict.
    """
    with open(fn, encoding="utf-8") as inputfile:
        return json.load(inputfile)


def main(api_key, member_id, filename):
    """Create the connection and print it.

    :param api_key: Route4Me API key.
    :param member_id: ID of the member.
    :param filename: path of the JSON file with the vendor credentials.
    """
    route4me = Route4Me(api_key)

    telematics = route4me.telematics
    token = telematics.register_member(member_id)

    if "api_token" not in token.keys():
        print(token)
        return

    api_token = token["api_token"]
    vendor_credentials = _load_credentials(filename)
    vendor_connection = telematics.register_connection(api_token, **vendor_credentials)
    telematics.pp_response(vendor_connection)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Register Telematics Member Connection")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--member_id", dest="member_id", help="Route4Me member_id", type=str, required=True)
    parser.add_argument(
        "--vendor_credentials",
        dest="filename",
        help="filename of the JSON with Telematics Vendor Credentials",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.member_id, args.filename)
