"""List the address book groups.

Calls :meth:`AddressBook.get_address_book_groups
<route4me.address_book.AddressBook.get_address_book_groups>`, which sends
``GET /api.v4/address_book_group.php`` with ``offset`` and ``limit`` in the query, and prints the first
ten groups. Pass ``group_id=...`` instead to get one group.

Run it with::

    python examples/addressbook/get_address_book_groups.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first ten groups.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book
    response = address_book.get_address_book_groups(offset=0, limit=10)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Address Book Groups")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
