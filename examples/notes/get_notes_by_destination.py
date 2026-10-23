r"""List the notes of a route destination.

Calls :meth:`Notes.get_notes_by_destination <route4me.notes.Notes.get_notes_by_destination>`, which
sends ``GET /modules/api/v5.0/notes/destination/{route_destination_id}`` (API V5, on
``wh.route4me.com``) with ``page`` and ``per_page`` in the query, and prints the first page.

Run it with::

    python examples/notes/get_notes_by_destination.py --api_key <your key> \
        --route_destination_id <destination ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_destination_id):
    """Print the first page of the notes of the destination.

    :param api_key: Route4Me API key.
    :param route_destination_id: ID of the route destination: the numeric ID or the UUID.
    """
    route4me = Route4Me(api_key)

    response = route4me.notes.get_notes_by_destination(route_destination_id, page=1, per_page=20)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Notes By Destination")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--route_destination_id",
        dest="route_destination_id",
        help="Route destination ID or UUID",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.route_destination_id)
