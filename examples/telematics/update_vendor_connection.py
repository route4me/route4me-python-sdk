r"""Update a telematics connection.

Reads the vendor credentials from a JSON file shaped like ``vendor_credentials.json`` and calls
:meth:`Telematics.update_connection <route4me.telematics.Telematics.update_connection>` with the
member's API token and the connection token, which sends ``PUT /api.v4/telematics/connections.php`` with
the credentials and ``validate_remote_credentials="true"`` as the JSON body. Prints the connection. The
client is created without an API key: the telematics API token authorizes the call. register_member.py
prints the API token, and get_connections.py the connection tokens.

Run it with::

    python examples/telematics/update_vendor_connection.py --api_token <API token> \
        --connection_token <connection token> \
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


def main(api_token, connection_token, filename):
    """Update the connection and print it.

    :param api_token: the member's telematics API token.
    :param connection_token: token of the connection.
    :param filename: path of the JSON file with the vendor credentials.
    """
    route4me = Route4Me(None)
    telematics = route4me.telematics
    vendor_credentials = _load_credentials(filename)
    vendor_connection = telematics.update_connection(api_token, connection_token, **vendor_credentials)
    telematics.pp_response(vendor_connection)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Telematics Member Connection")
    parser.add_argument("--api_token", dest="api_token", help="Telematics API TOKEN", type=str, required=True)
    parser.add_argument(
        "--connection_token", dest="connection_token", help="Telematics Connection Token", type=str, required=True
    )
    parser.add_argument(
        "--vendor_credentials",
        dest="filename",
        help="filename of the JSON with Telematics Vendor Credentials",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_token, args.connection_token, args.filename)
