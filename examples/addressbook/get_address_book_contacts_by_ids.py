"""Get address book contacts by their IDs (API V5).

Calls :meth:`AddressBookV5.get_address_book_contacts_by_ids
<route4me.address_book_v5.AddressBookV5.get_address_book_contacts_by_ids>`, which sends
``POST /modules/api/v5.0/address-book/addresses/show`` (API V5, on ``wh.route4me.com``) with
``address_ids`` as the JSON body, and prints the reply.

Run it with::

    python examples/addressbook/get_address_book_contacts_by_ids.py --api_key <your key> \
        --address_ids <contact ID> [<contact ID> ...]
"""

import argparse

from route4me import Route4Me


def main(api_key, address_ids):
    """Print the contacts.

    :param api_key: Route4Me API key.
    :param address_ids: IDs of the contacts.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.get_address_book_contacts_by_ids(address_ids=address_ids)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Address Book Contacts By IDs V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--address_ids", dest="address_ids", help="Contact IDs", type=int, nargs="+", required=True)
    args = parser.parse_args()
    main(args.api_key, args.address_ids)
