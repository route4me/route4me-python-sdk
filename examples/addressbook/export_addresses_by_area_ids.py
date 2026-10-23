"""Export the address book contacts inside territories (API V5).

Calls :meth:`AddressBookV5.export_addresses_by_area_ids
<route4me.address_book_v5.AddressBookV5.export_addresses_by_area_ids>`, which sends
``POST /modules/api/v5.0/address-book/addresses/export-by-area-ids`` (API V5, on ``wh.route4me.com``)
with ``territory_ids`` and ``filename`` as the JSON body, and prints where to follow the background job
that builds the file.

Run it with::

    python examples/addressbook/export_addresses_by_area_ids.py --api_key <your key> \
        --territory_ids <territory ID> [<territory ID> ...]
"""

import argparse

from route4me import Route4Me


def main(api_key, territory_ids):
    """Start the export and print the job.

    :param api_key: Route4Me API key.
    :param territory_ids: IDs of the territories.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.export_addresses_by_area_ids(territory_ids=territory_ids, filename="territories")
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    elif response == b"":
        reply = address_book.response
        print(f"Job queued (HTTP {reply.status_code}): {reply.headers.get('Location')}")
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Addresses By Area IDs V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--territory_ids", dest="territory_ids", help="Territory IDs", type=str, nargs="+", required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.territory_ids)
