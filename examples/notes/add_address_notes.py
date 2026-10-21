"""Add a note to a route destination.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` and
:meth:`Route.get_route <route4me.route.Route.get_route>` (``GET /api.v4/route.php``) to read the latest
route, then :meth:`Address.add_address_notes <route4me.address.Address.add_address_notes>` for its first
destination, which sends ``POST /actions/addRouteNotes.php`` with ``route_id``, ``address_id``,
``device_type`` and the destination's coordinates (``dev_lat``, ``dev_lng``) in the query, and the note
(``strNoteContents``) and its type (``strUpdateType``, here ``wrongdelivery``) as form fields. Prints
the new note, which stays on the route.

Run it with::

    python examples/notes/add_address_notes.py --api_key <your key>
"""

import argparse

from route4me import Route4Me
from route4me.constants import DEVICE_TYPE


def main(api_key):
    """Add a note to the first destination of the latest route.

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
            route_id = response["route_id"]
            address = response["addresses"][0]
            route_destination_id = address["route_destination_id"]
            lat = address["lat"]
            lng = address["lng"]
            note = "Test Note Contents"
            response = route4me.address.add_address_notes(
                note,
                route_id=route_id,
                device_type=DEVICE_TYPE.WEB,
                activity_type="wrongdelivery",
                dev_lat=lat,
                dev_lng=lng,
                address_id=route_destination_id,
            )
            if isinstance(response, dict) and "errors" in response.keys():
                print(". ".join(response["errors"]))
            else:
                note = response["note"]
                print(f"Note ID: {response['note_id']}")
                print(f"Note contents: {note['contents']}")
                print(f"Route ID: {note['route_id']}")
                print(f"Route Destination ID: {note['route_destination_id']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add Address Notes")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
