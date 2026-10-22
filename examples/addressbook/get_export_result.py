"""Download the file of a finished address book contact export (API V5).

Calls :meth:`AddressBookV5.get_export_result <route4me.address_book_v5.AddressBookV5.get_export_result>`,
which sends ``GET /modules/api/v5.0/address-book/addresses/export/result/{export_id}`` (API V5, on
``wh.route4me.com``) and saves the file. Check the export with ``get_export_status.py`` first.

Run it with::

    python examples/addressbook/get_export_result.py --api_key <your key> --export_id <export ID> \
        [--output contacts.csv]
"""

import argparse
import pathlib

from route4me import Route4Me


def main(api_key, export_id, output):
    """Save the file of an export.

    :param api_key: Route4Me API key.
    :param export_id: the export's ID.
    :param output: the path to save the file to.
    """
    route4me = Route4Me(api_key)

    response = route4me.address_book_v5.get_export_result(export_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        pathlib.Path(output).write_bytes(response)
        print(f"Saved {len(response)} bytes to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Export Result V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--export_id", dest="export_id", help="Export ID", type=str, required=True)
    parser.add_argument("--output", dest="output", help="File to save", type=str, default="contacts.csv")
    args = parser.parse_args()
    main(args.api_key, args.export_id, args.output)
