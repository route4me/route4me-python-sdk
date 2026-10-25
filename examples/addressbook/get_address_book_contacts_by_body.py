"""List routed address book contacts, sorted, with a JSON body (API V5).

Calls :meth:`AddressBookV5.get_address_book_contacts_by_body
<route4me.address_book_v5.AddressBookV5.get_address_book_contacts_by_body>`, which sends
``POST /modules/api/v5.0/address-book/addresses/index/all`` (API V5, on ``wh.route4me.com``) with
``fields``, ``filter``, ``order_by`` and ``limit`` as the JSON body, and prints the reply.

Run it with::

    python examples/addressbook/get_address_book_contacts_by_body.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first ten routed contacts, sorted by alias.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.get_address_book_contacts_by_body(
        fields=["address_id", "address_alias", "address_1"],
        filter={"display": "routed"},
        order_by=[["address_alias", "asc"]],
        limit=10,
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Address Book Contacts By Body V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
