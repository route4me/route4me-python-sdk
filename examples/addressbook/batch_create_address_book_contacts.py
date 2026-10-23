"""Create two address book contacts in one request (API V5).

Calls :meth:`AddressBookV5.batch_create_address_book_contacts
<route4me.address_book_v5.AddressBookV5.batch_create_address_book_contacts>`, which sends
``POST /modules/api/v5.0/address-book/addresses/batch-create`` (API V5, on ``wh.route4me.com``) with the
contacts in ``data`` as the JSON body, and prints the reply. The contacts stay in the address book.

Run it with::

    python examples/addressbook/batch_create_address_book_contacts.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create two contacts and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.batch_create_address_book_contacts(
        data=[
            {
                "address_1": "1 Example St, Springfield, IL 62701",
                "cached_lat": 39.7990,
                "cached_lng": -89.6440,
                "address_email": "jane.doe@example.com",
            },
            {
                "address_1": "2 Example St, Springfield, IL 62701",
                "cached_lat": 39.7995,
                "cached_lng": -89.6445,
                "address_email": "john.doe@example.com",
            },
        ]
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Create Address Book Contacts V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
