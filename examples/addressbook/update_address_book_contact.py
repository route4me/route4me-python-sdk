"""Set the alias of an address book contact (API V5).

Calls :meth:`AddressBookV5.update_address_book_contact
<route4me.address_book_v5.AddressBookV5.update_address_book_contact>`, which sends
``PUT /modules/api/v5.0/address-book/addresses/{address_id}`` (API V5, on ``wh.route4me.com``) with the
contact as the JSON body, and prints the updated contact. It reads the contact first with
:meth:`AddressBookV5.get_address_book_contacts_by_ids
<route4me.address_book_v5.AddressBookV5.get_address_book_contacts_by_ids>`, because the update needs
``address_1``, ``cached_lat`` and ``cached_lng``. This changes a contact of the account.

Run it with::

    python examples/addressbook/update_address_book_contact.py --api_key <your key> --address_id <contact ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, address_id):
    """Set the alias of the contact and print it.

    :param api_key: Route4Me API key.
    :param address_id: ID of the contact.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.get_address_book_contacts_by_ids(address_ids=[address_id])
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
        return
    contact = response["results"][0]
    response = address_book.update_address_book_contact(
        address_id,
        address_1=contact["address_1"],
        cached_lat=contact["cached_lat"],
        cached_lng=contact["cached_lng"],
        address_alias="Example alias",
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Address Book Contact V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--address_id", dest="address_id", help="Contact ID", type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.address_id)
