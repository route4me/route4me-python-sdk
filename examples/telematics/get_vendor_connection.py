r"""Get one telematics connection.

Calls :meth:`Telematics.get_connection <route4me.telematics.Telematics.get_connection>` with the
member's API token and the connection token, which sends ``GET /api.v4/telematics/connections.php``, and
prints the connection. The client is created without an API key: the telematics API token authorizes the
call. register_member.py prints the API token, and get_connections.py the connection tokens.

Run it with::

    python examples/telematics/get_vendor_connection.py --api_token <API token> \
        --connection_token <connection token>
"""

import argparse

from route4me import Route4Me


def main(api_token, connection_token):
    """Print the connection.

    :param api_token: the member's telematics API token.
    :param connection_token: token of the connection.
    """
    route4me = Route4Me(None)
    telematics = route4me.telematics
    vendor_connection = telematics.get_connection(api_token, connection_token)
    telematics.pp_response(vendor_connection)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Telematics Member Connection")
    parser.add_argument("--api_token", dest="api_token", help="Telematics API TOKEN", type=str, required=True)
    parser.add_argument(
        "--connection_token", dest="connection_token", help="Telematics Connection Token", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_token, args.connection_token)
