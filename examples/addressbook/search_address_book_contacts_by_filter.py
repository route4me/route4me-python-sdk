"""Search the address book contacts with a text filter.

Calls :meth:`AddressBook.search_address_book_contacts_by_filter
<route4me.address_book.AddressBook.search_address_book_contacts_by_filter>`, which sends
``POST /api.v4/address_book.php`` with the ``fields`` and ``filter`` as the JSON body and ``offset`` and
``limit`` in the query, and prints the first ten contacts whose fields contain "Example".

Run it with::

    python examples/addressbook/search_address_book_contacts_by_filter.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first ten contacts that match the filter.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book
    response = address_book.search_address_book_contacts_by_filter(
        {"fields": ["address_id", "address_1", "address_group"], "filter": {"query": "Example", "display": "all"}},
        offset=0,
        limit=10,
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Address Book Contacts By Filter")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
