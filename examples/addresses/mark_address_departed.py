r"""Mark a destination of a route as departed.

Calls :meth:`Address.mark_address_departed <route4me.address.Address.mark_address_departed>`, which sends
``GET /api/route/mark_address_departed.php`` with ``route_id``, ``address_id`` and ``is_departed=1`` in
the query, and prints the reply.

Run it with::

    python examples/addresses/mark_address_departed.py --api_key <your key> --route_id <route id> \
        --address_id <address id>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id, address_id):
    """Mark the destination as departed and print the reply.

    :param api_key: Route4Me API key.
    :param route_id: route ID.
    :param address_id: route destination ID.
    """
    route4me = Route4Me(api_key)

    response = route4me.address.mark_address_departed(route_id, address_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mark an Address as Departed")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route ID", type=str, required=True)
    parser.add_argument("--address_id", dest="address_id", help="Route destination ID", type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id, args.address_id)
