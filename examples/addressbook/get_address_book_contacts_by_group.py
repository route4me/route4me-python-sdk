"""List the contacts of an address book group.

Calls :meth:`AddressBook.get_address_book_contacts_by_group
<route4me.address_book.AddressBook.get_address_book_contacts_by_group>`, which sends
``POST /api/address_book/get_search_group_addresses.php`` with ``group_id`` in the query and the
``fields`` to return as the JSON body, and prints the reply.

Run it with::

    python examples/addressbook/get_address_book_contacts_by_group.py --api_key <your key> --group_id <group ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, group_id):
    """Print the contacts of the group.

    :param api_key: Route4Me API key.
    :param group_id: ID of the address book group.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book
    response = address_book.get_address_book_contacts_by_group(
        {"fields": ["address_id", "address_1"]}, group_id=group_id
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Address Book Contacts By Group")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--group_id", dest="group_id", help="Address book group ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.group_id)
