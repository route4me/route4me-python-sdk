"""List address book contacts, a page at a time.

Calls :meth:`AddressBook.get_addressbook_contacts
<route4me.address_book.AddressBook.get_addressbook_contacts>` with ``limit=10`` and ``offset=5``, which
sends ``GET /api.v4/address_book.php``, and prints the ID, name and address of each contact.

Run it with::

    python examples/addressbook/get_addressbook_contacts.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print ten contacts, after the first five.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book
    response = address_book.get_addressbook_contacts(limit=10, offset=5)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        contacts = response["results"]
        for i, contact in enumerate(contacts):
            print(f"Address: {i + 1} -  ID: {contact['address_id']}")
            print(f"\tFirst Name: {contact['first_name']}")
            print(f"\tLast Name: {contact['last_name']}")
            print(f"\tAddress: {contact['address_1']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Address Book Contacts")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
