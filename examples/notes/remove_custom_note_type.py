r"""Delete a custom note type with API V4.

Calls :meth:`Notes.remove_custom_note_type <route4me.notes.Notes.remove_custom_note_type>`, which sends
``DELETE /api.v4/note_custom_types.php`` with ``{"id": <note_custom_type_id>}`` as the JSON body, and
prints the reply. The type is deleted.

Run it with::

    python examples/notes/remove_custom_note_type.py --api_key <your key> \
        --note_custom_type_id <custom note type ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, note_custom_type_id):
    """Delete the custom note type and print the reply.

    :param api_key: Route4Me API key.
    :param note_custom_type_id: ID of the custom note type, as ``get_all_custom_note_types`` returns it.
    """
    route4me = Route4Me(api_key)

    response = route4me.notes.remove_custom_note_type(note_custom_type_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove Custom Note Type")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--note_custom_type_id", dest="note_custom_type_id", help="Custom note type ID", type=int, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.note_custom_type_id)
