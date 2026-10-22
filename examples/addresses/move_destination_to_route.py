r"""Move a destination to another route.

Calls :meth:`Address.move_destination_to_route <route4me.address.Address.move_destination_to_route>`, which
sends ``POST /actions/route/move_route_destination.php`` with ``to_route_id``, ``route_destination_id``
and ``after_destination_id`` as form fields, and prints the reply. The destination is placed after
``--after_destination_id`` in the target route.

Run it with::

    python examples/addresses/move_destination_to_route.py --api_key <your key> \
        --to_route_id <to route id> --route_destination_id <route destination id> \
        --after_destination_id <after destination id>
"""

import argparse

from route4me import Route4Me


def main(api_key, to_route_id, route_destination_id, after_destination_id):
    """Move the destination and print the reply.

    :param api_key: Route4Me API key.
    :param to_route_id: ID of the route the destination moves to.
    :param route_destination_id: route destination ID to move.
    :param after_destination_id: route destination ID it goes after.
    """
    route4me = Route4Me(api_key)

    response = route4me.address.move_destination_to_route(
        to_route_id, route_destination_id, after_destination_id=after_destination_id
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move a Destination to Another Route")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--to_route_id", dest="to_route_id", help="ID of the route the destination moves to", type=str, required=True
    )
    parser.add_argument(
        "--route_destination_id",
        dest="route_destination_id",
        help="Route destination ID to move",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--after_destination_id",
        dest="after_destination_id",
        help="Route destination ID it goes after",
        type=int,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.to_route_id, args.route_destination_id, args.after_destination_id)
