"""Export address book contacts to a CSV file (API V5).

Calls :meth:`AddressBookV5.export_addresses <route4me.address_book_v5.AddressBookV5.export_addresses>`,
which sends ``POST /modules/api/v5.0/address-book/addresses/export`` (API V5, on ``wh.route4me.com``)
with the contact ``ids``, ``filename`` and ``extension`` as the JSON body, and prints where to follow
the background job that builds the file.

Run it with::

    python examples/addressbook/export_addresses.py --api_key <your key> \
        --address_ids <contact ID> [<contact ID> ...]
"""

import argparse

from route4me import Route4Me


def main(api_key, address_ids):
    """Start the export and print the job.

    :param api_key: Route4Me API key.
    :param address_ids: IDs of the contacts.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.export_addresses(ids=address_ids, filename="contacts", extension="csv")
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    elif response == b"":
        reply = address_book.response
        print(f"Job queued (HTTP {reply.status_code}): {reply.headers.get('Location')}")
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Addresses V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--address_ids", dest="address_ids", help="Contact IDs", type=int, nargs="+", required=True)
    args = parser.parse_args()
    main(args.api_key, args.address_ids)
