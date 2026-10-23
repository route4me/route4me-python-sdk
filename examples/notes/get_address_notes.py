"""Get the notes of a route destination.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` and
:meth:`Route.get_route <route4me.route.Route.get_route>` (``GET /api.v4/route.php``) to read the latest
route, then :meth:`Address.get_address_notes <route4me.address.Address.get_address_notes>` for its first
destination, which sends ``GET /api.v4/address.php`` with ``notes=True``, and prints the address and
each note.

Run it with::

    python examples/notes/get_address_notes.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the notes of the first destination of the latest route.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    route = route4me.route
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        route_id = response[0]["route_id"]
        print(f"Route ID: {route_id}")
        response = route.get_route(route_id=route_id)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            address = response["addresses"][0]
            route_destination_id = address["route_destination_id"]
            response = route4me.address.get_address_notes(
                route_id=route_id,
                route_destination_id=route_destination_id,
            )
            if isinstance(response, dict) and "errors" in response.keys():
                print(". ".join(response["errors"]))
            else:
                print(f"Address: {response['address']}")
                print("Notes")
                for i, note in enumerate(response["notes"]):
                    print(f"\t{i + 1} - {note['contents']} - {note['activity_type']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Notes from an Address")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
