"""Delete address book contacts (API V5).

Calls :meth:`AddressBookV5.remove_address_book_contacts
<route4me.address_book_v5.AddressBookV5.remove_address_book_contacts>`, which sends
``DELETE /modules/api/v5.0/address-book/addresses/delete`` (API V5, on ``wh.route4me.com``) with
``address_ids`` as the JSON body, and prints the reply, or where to follow the job when the API deletes
them in the background. This deletes contacts of the account.

Run it with::

    python examples/addressbook/remove_address_book_contacts.py --api_key <your key> \
        --address_ids <contact ID> [<contact ID> ...]
"""

import argparse

from route4me import Route4Me


def main(api_key, address_ids):
    """Delete the contacts and print the reply.

    :param api_key: Route4Me API key.
    :param address_ids: IDs of the contacts.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.remove_address_book_contacts(address_ids=address_ids)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    elif response == b"":
        reply = address_book.response
        print(f"Job queued (HTTP {reply.status_code}): {reply.headers.get('Location')}")
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove Address Book Contacts V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--address_ids", dest="address_ids", help="Contact IDs", type=int, nargs="+", required=True)
    args = parser.parse_args()
    main(args.api_key, args.address_ids)
