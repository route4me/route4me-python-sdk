"""Delete a note.

Calls :meth:`Notes.delete_note <route4me.notes.Notes.delete_note>`, which sends
``DELETE /modules/api/v5.0/notes/{note_id}`` (API V5, on ``wh.route4me.com``), and prints the reply. The
note is deleted.

Run it with::

    python examples/notes/delete_note.py --api_key <your key> --note_id <note ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, note_id):
    """Delete the note and print the reply.

    :param api_key: Route4Me API key.
    :param note_id: ID of the note.
    """
    route4me = Route4Me(api_key)

    response = route4me.notes.delete_note(note_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete Note")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--note_id", dest="note_id", help="Note ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.note_id)
