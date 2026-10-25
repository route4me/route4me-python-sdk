"""Save geocoded addresses from temporary storage to the address book.

Calls :meth:`AddressBook.save_geocoded_addresses_to_database
<route4me.address_book.AddressBook.save_geocoded_addresses_to_database>`, which sends
``POST /api/address_book/save_geocoded.php`` with ``optimization_problem_id`` as the JSON body, and
prints the reply. The addresses are added to the address book of the account.

Run it with::

    python examples/addressbook/save_geocoded_addresses_to_database.py --api_key <your key> \
        --optimization_problem_id <optimization ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, optimization_problem_id):
    """Save the geocoded addresses and print the reply.

    :param api_key: Route4Me API key.
    :param optimization_problem_id: ID of the temporary optimization that holds the geocoded addresses.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book
    response = address_book.save_geocoded_addresses_to_database(optimization_problem_id=optimization_problem_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save Geocoded Addresses")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--optimization_problem_id",
        dest="optimization_problem_id",
        help="Temporary optimization problem ID",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.optimization_problem_id)
