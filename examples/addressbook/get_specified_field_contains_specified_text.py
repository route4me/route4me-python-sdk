"""Search the address book, returning only some fields.

Calls :meth:`AddressBook.get_addressbook_contacts
<route4me.address_book.AddressBook.get_addressbook_contacts>` with ``query="juan"`` and
``fields="first_name,address_email"``, which sends ``GET /api.v4/address_book.php``. With ``fields``,
each result is a list of those values rather than a contact; the example prints the first name and the
email of each match.

Deprecated: AddressBook.get_addressbook_contacts is deprecated, because the C# SDK marks the operation obsolete.
The API V5 replacement is shown in ``examples/addressbook/get_address_book_contacts.py``.

Run it with::

    python examples/addressbook/get_specified_field_contains_specified_text.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first name and email of the contacts that match "juan".

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book
    print('Searching "Juan" in Addressbook')
    response = address_book.get_addressbook_contacts(
        limit=10, offset=0, query="juan", fields="first_name,address_email"
    )
    for row in response.get("results", []):
        print(f"First Name: {row[0]} - Email: {row[1]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Contact by Field and Value")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
