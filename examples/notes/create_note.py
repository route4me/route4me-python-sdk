"""Add a note to a route.

Calls :meth:`Notes.create_note <route4me.notes.Notes.create_note>`, which sends
``POST /modules/api/v5.0/notes`` (API V5, on ``wh.route4me.com``) with ``route_id``, the note text
(``strNoteContents``), its type (``strUpdateType``) and ``device_type`` as the JSON body, and prints the
reply. Pass ``--address_id`` to attach the note to one destination of the route. The note stays on the
route.

Run it with::

    python examples/notes/create_note.py --api_key <your key> --route_id <route ID>

Optional: ``--address_id <destination ID>``.
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id, address_id):
    """Add a note to the route and print the reply.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    :param address_id: ID of a destination of the route, or ``None``.
    """
    route4me = Route4Me(api_key)

    note = {
        "route_id": route_id,
        "strNoteContents": "Left the parcel at the front door",
        "strUpdateType": "dropoff",
        "device_type": "web",
    }
    if address_id is not None:
        note["address_id"] = address_id
    response = route4me.notes.create_note(**note)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Note")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route4Me Route ID", type=str, required=True)
    parser.add_argument("--address_id", dest="address_id", help="Route destination ID", type=int, required=False)
    args = parser.parse_args()
    main(args.api_key, args.route_id, args.address_id)
