"""Get the status of an address book contact export (API V5).

Calls :meth:`AddressBookV5.get_export_status <route4me.address_book_v5.AddressBookV5.get_export_status>`,
which sends ``GET /modules/api/v5.0/address-book/addresses/export/status/{export_id}`` (API V5, on
``wh.route4me.com``) and prints the status. The export ID is the last segment of the ``Location``
header that ``export_addresses.py`` prints.

Run it with::

    python examples/addressbook/get_export_status.py --api_key <your key> --export_id <export ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, export_id):
    """Print the status of an export.

    :param api_key: Route4Me API key.
    :param export_id: the export's ID.
    """
    route4me = Route4Me(api_key)

    response = route4me.address_book_v5.get_export_status(export_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(f"Export status: {response}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Export Status V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--export_id", dest="export_id", help="Export ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.export_id)
