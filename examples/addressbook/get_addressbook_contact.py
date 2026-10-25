"""Get an address book contact by ID.

Calls :meth:`AddressBook.get_addressbook_contacts
<route4me.address_book.AddressBook.get_addressbook_contacts>` (``GET /api.v4/address_book.php``) to pick
the first contact, then :meth:`AddressBook.get_addressbook_contact
<route4me.address_book.AddressBook.get_addressbook_contact>` with its ``address_id``, which sends the
same request with ``address_id`` in the query, and prints the contacts of the reply.

Deprecated: AddressBook.get_addressbook_contacts is deprecated, because the C# SDK marks the operation obsolete.
The API V5 replacement is shown in ``examples/addressbook/get_address_book_contacts.py``.

Run it with::

    python examples/addressbook/get_addressbook_contact.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first contact of the address book.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book
    response = address_book.get_addressbook_contacts(limit=1, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        address_id = response["results"][0]["address_id"]
        response = address_book.get_addressbook_contact(address_id=address_id)
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
    parser = argparse.ArgumentParser(description="Get Address Book Contact")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
