"""Create an address book contact.

Calls :meth:`AddressBook.create_contact <route4me.address_book.AddressBook.create_contact>`, which sends
``POST /api.v4/address_book.php`` with the contact as the JSON body (``address_1``, ``cached_lat`` and
``cached_lng`` are required), and prints the new contact. The contact stays in the address book;
delete_addressbook_contact.py shows how to remove one.

Run it with::

    python examples/addressbook/add_addressbook_contact.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create a contact and print it.

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
    print(f"Address ID: {response['address_id']}")
    print(f"First Name: {response['first_name']}")
    print(f"Last Name: {response['last_name']}")
    print(f"Address: {response['address_1']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add AddressBook Contact")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
