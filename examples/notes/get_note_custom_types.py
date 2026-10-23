"""List the custom note types of the account.

Calls :meth:`Notes.get_note_custom_types <route4me.notes.Notes.get_note_custom_types>`, which sends
``GET /modules/api/v5.0/notes/custom-types`` (API V5, on ``wh.route4me.com``), and prints the reply.

Run it with::

    python examples/notes/get_note_custom_types.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the custom note types.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.notes.get_note_custom_types()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Note Custom Types")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
