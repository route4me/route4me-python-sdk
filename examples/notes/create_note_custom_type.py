"""Add a custom note type.

Calls :meth:`Notes.create_note_custom_type <route4me.notes.Notes.create_note_custom_type>`, which sends
``POST /modules/api/v5.0/notes/custom-types`` (API V5, on ``wh.route4me.com``) with
``note_custom_type``, ``note_custom_type_values`` and ``note_custom_field_type`` (1, a select list) as
the JSON body, and prints the reply. The type stays on the account.

Run it with::

    python examples/notes/create_note_custom_type.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Add a custom note type and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.notes.create_note_custom_type(
        note_custom_type="Delivery place",
        note_custom_type_values=["Front door", "Back door", "Reception"],
        note_custom_field_type=1,
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Note Custom Type")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
