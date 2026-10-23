"""Create an address book contact, then delete it.

Calls :meth:`AddressBook.create_contact <route4me.address_book.AddressBook.create_contact>`
(``POST /api.v4/address_book.php``), then :meth:`AddressBook.delete_addressbook_contact
<route4me.address_book.AddressBook.delete_addressbook_contact>` with the new contact's ID in
``address_ids``, which sends ``DELETE /api.v4/address_book.php`` with them as the JSON body, and prints
the status.

Deprecated: AddressBook.create_contact and AddressBook.delete_addressbook_contact are deprecated,
because the C# SDK marks the operations obsolete.
The API V5 replacement is shown in ``examples/addressbook/remove_address_book_contacts.py``.

Run it with::

    python examples/addressbook/delete_addressbook_contact.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create a contact, delete it and print the status.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book
    response = address_book.create_contact(
        first_name="Juan",
        last_name="Pimentel",
        address_1="17205 RICHMOND TNPK, MILFORD, VA, 22514",
        cached_lat=38.024654,
        cached_lng=-77.338814,
    )
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        print(f"Address ID: {response['address_id']}")
        print(f"First Name: {response['first_name']}")
        print(f"Last Name: {response['last_name']}")
        print(f"Address: {response['address_1']}")
        print("Deleting this Contact")
        address_ids = [
            response["address_id"],
        ]
        response = address_book.delete_addressbook_contact(address_ids=address_ids)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            print(f"Deleted: {response['status']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete Address Book Contact")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
