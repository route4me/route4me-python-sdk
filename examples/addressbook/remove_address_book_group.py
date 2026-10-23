"""Delete an address book group.

Calls :meth:`AddressBook.remove_address_book_group
<route4me.address_book.AddressBook.remove_address_book_group>`, which sends
``DELETE /api.v4/address_book_group.php`` with ``group_id`` as the JSON body, and prints the status.
This deletes a group of the account.

Run it with::

    python examples/addressbook/remove_address_book_group.py --api_key <your key> --group_id <group ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, group_id):
    """Delete the group and print the status.

    :param api_key: Route4Me API key.
    :param group_id: ID of the address book group.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book
    response = address_book.remove_address_book_group(group_id=group_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove Address Book Group")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--group_id", dest="group_id", help="Address book group ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.group_id)
