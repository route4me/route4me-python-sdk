"""Create an address book contact (API V5).

Calls :meth:`AddressBookV5.add_address_book_contact
<route4me.address_book_v5.AddressBookV5.add_address_book_contact>`, which sends
``POST /modules/api/v5.0/address-book/addresses`` (API V5, on ``wh.route4me.com``) with the contact as
the JSON body (``address_1``, ``cached_lat`` and ``cached_lng`` are required), and prints the new
contact. The contact stays in the address book; remove_address_book_contacts.py shows how to delete one.

Run it with::

    python examples/addressbook/add_address_book_contact.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create a contact and print it.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.add_address_book_contact(
        address_1="1 Example St, Springfield, IL 62701",
        cached_lat=39.7990,
        cached_lng=-89.6440,
        first_name="Jane",
        last_name="Doe",
        address_email="jane.doe@example.com",
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add Address Book Contact V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
