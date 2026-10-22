"""Add a custom note type with API V4.

Calls :meth:`Notes.add_custom_note_type <route4me.notes.Notes.add_custom_note_type>`, which sends
``POST /api.v4/note_custom_types.php`` with ``note_custom_type`` and ``note_custom_type_values`` as the
JSON body, and prints the reply. The type stays on the account.

Run it with::

    python examples/notes/add_custom_note_type.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Add a custom note type and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.notes.add_custom_note_type(
        note_custom_type="Customer language",
        note_custom_type_values=["English", "French"],
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add Custom Note Type")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
