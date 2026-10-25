"""Put several address book contacts in the same group (API V5).

Calls :meth:`AddressBookV5.batch_update_address_book_contact
<route4me.address_book_v5.AddressBookV5.batch_update_address_book_contact>`, which sends
``PUT /modules/api/v5.0/address-book/addresses/batch-update`` (API V5, on ``wh.route4me.com``) with
``address_ids`` and the new ``address_group`` as the JSON body, and prints the updated contacts. This
changes contacts of the account.

Run it with::

    python examples/addressbook/batch_update_address_book_contact.py --api_key <your key> \
        --address_ids <contact ID> [<contact ID> ...]
"""

import argparse

from route4me import Route4Me


def main(api_key, address_ids):
    """Set the group of the contacts and print the reply.

    :param api_key: Route4Me API key.
    :param address_ids: IDs of the contacts.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.batch_update_address_book_contact(address_ids=address_ids, address_group="Example group")
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Update Address Book Contacts V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--address_ids", dest="address_ids", help="Contact IDs", type=int, nargs="+", required=True)
    args = parser.parse_args()
    main(args.api_key, args.address_ids)
