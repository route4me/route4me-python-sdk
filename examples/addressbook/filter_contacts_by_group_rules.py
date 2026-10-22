"""List the address book contacts that match group rules (API V5).

Calls :meth:`AddressBookV5.filter_contacts_by_group_rules
<route4me.address_book_v5.AddressBookV5.filter_contacts_by_group_rules>`, which sends
``POST /modules/api/v5.0/address-book/groups/filter/all`` (API V5, on ``wh.route4me.com``) with the
``rules`` and ``limit`` as the JSON body and ``display=all`` in the query, and prints the first ten
contacts whose address contains "Example".

Run it with::

    python examples/addressbook/filter_contacts_by_group_rules.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first ten contacts that match the rules.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.filter_contacts_by_group_rules(
        {
            "rules": {
                "condition": "AND",
                "rules": [{"id": "address_1", "field": "address_1", "operator": "contains", "value": "Example"}],
            },
            "limit": 10,
        },
        display="all",
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter Contacts By Group Rules V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
