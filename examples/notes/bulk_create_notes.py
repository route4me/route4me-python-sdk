"""Add two notes to a route in one request.

Calls :meth:`Notes.bulk_create_notes <route4me.notes.Notes.bulk_create_notes>`, which sends
``POST /modules/api/v5.0/notes/bulk-create`` (API V5, on ``wh.route4me.com``) with the list of notes and
``device_type`` as the JSON body, and prints the reply. The API stores the notes asynchronously; they
stay on the route.

Run it with::

    python examples/notes/bulk_create_notes.py --api_key <your key> --route_id <route ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id):
    """Add two notes to the route and print the reply.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    """
    route4me = Route4Me(api_key)

    notes = [
        {"route_id": route_id, "strNoteContents": "Customer asked for a call before delivery"},
        {"route_id": route_id, "strNoteContents": "Gate code changed", "strUpdateType": "other"},
    ]
    response = route4me.notes.bulk_create_notes(notes=notes, device_type="web")
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk Create Notes")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route4Me Route ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id)
