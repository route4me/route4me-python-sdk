r"""Delete one or more destinations from their routes.

Calls :meth:`Address.delete_route_destinations <route4me.address.Address.delete_route_destinations>`, which
sends ``POST /actions/route/delete_route_destination.php`` with the IDs, comma-separated, as a form field,
and prints the reply.

Run it with::

    python examples/addresses/delete_route_destinations.py --api_key <your key> \
        --route_destination_id <route destination id> [--route_destination_id ...]
"""

import argparse

from route4me import Route4Me


def main(api_key, route_destination_id):
    """Delete the destinations and print the reply.

    :param api_key: Route4Me API key.
    :param route_destination_id: route destination ID; repeat for several.
    """
    route4me = Route4Me(api_key)

    response = route4me.address.delete_route_destinations(route_destination_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete Route Destinations")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--route_destination_id",
        dest="route_destination_id",
        help="Route destination ID; repeat for several",
        type=int,
        action="append",
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.route_destination_id)
