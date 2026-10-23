"""List the address book contacts marked as depots (API V5).

Calls :meth:`AddressBookV5.get_depots_from_address_book
<route4me.address_book_v5.AddressBookV5.get_depots_from_address_book>`, which sends
``GET /modules/api/v5.0/address-book/addresses/depots`` (API V5, on ``wh.route4me.com``), and prints the
reply.

Run it with::

    python examples/addressbook/get_depots_from_address_book.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the depot contacts.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.get_depots_from_address_book()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Depots From Address Book V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
