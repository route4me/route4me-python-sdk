"""Create an address book group.

Calls :meth:`AddressBook.add_address_book_group
<route4me.address_book.AddressBook.add_address_book_group>`, which sends
``POST /api.v4/address_book_group.php`` with the group as the JSON body, and prints the new group. The
group stays in the account; remove_address_book_group.py shows how to delete one.

Run it with::

    python examples/addressbook/add_address_book_group.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create a group and print it.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book
    response = address_book.add_address_book_group(
        group_name="Example group",
        group_color="92e1c0",
        filter={
            "condition": "AND",
            "rules": [{"id": "address_1", "field": "address_1", "operator": "contains", "value": "Example"}],
        },
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add Address Book Group")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
