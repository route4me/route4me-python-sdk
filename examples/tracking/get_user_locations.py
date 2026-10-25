"""Get the last known location of each user of the account.

Calls :meth:`GPS.get_user_locations <route4me.gps.GPS.get_user_locations>`, which sends
``GET /api/track/view_user_locations.php``, with ``query`` when ``--query`` is given to search the
users by email, name or member ID, and prints the reply.

Run it with::

    python examples/tracking/get_user_locations.py --api_key <your key> [--query <text>]
"""

import argparse

from route4me import Route4Me


def main(api_key, query=None):
    """Print the user locations.

    :param api_key: Route4Me API key.
    :param query: text to search the users by, or ``None`` for every user.
    """
    route4me = Route4Me(api_key)

    gps = route4me.gps
    response = gps.get_user_locations() if query is None else gps.get_user_locations(query=query)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get User Locations")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--query", dest="query", help="Search text", type=str, default=None)
    args = parser.parse_args()
    main(args.api_key, args.query)
