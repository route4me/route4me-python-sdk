"""List the custom fields of the address book contacts (API V5).

Calls :meth:`AddressBookV5.get_custom_fields
<route4me.address_book_v5.AddressBookV5.get_custom_fields>`, which sends
``GET /modules/api/v5.0/address-book/addresses/custom-fields`` (API V5, on ``wh.route4me.com``), and
prints the reply.

Run it with::

    python examples/addressbook/get_custom_fields.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the custom fields.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.get_custom_fields()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Address Book Custom Fields V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
