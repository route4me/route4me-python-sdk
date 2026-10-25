"""Change the text of a note.

Calls :meth:`Notes.update_note <route4me.notes.Notes.update_note>`, which sends
``POST /modules/api/v5.0/notes/{note_id}`` (API V5, on ``wh.route4me.com``) with the new
``strNoteContents`` as the JSON body, and prints the reply.

Run it with::

    python examples/notes/update_note.py --api_key <your key> --note_id <note ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, note_id):
    """Change the text of the note and print the reply.

    :param api_key: Route4Me API key.
    :param note_id: ID of the note.
    """
    route4me = Route4Me(api_key)

    response = route4me.notes.update_note(note_id, strNoteContents="Left the parcel with the neighbour")
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Note")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--note_id", dest="note_id", help="Note ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.note_id)
