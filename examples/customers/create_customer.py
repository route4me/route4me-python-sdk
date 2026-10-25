"""Create a customer with API V5.

Calls :meth:`Customers.create_customer <route4me.customers.Customers.create_customer>`, which sends
``POST /modules/api/v5.0/customers`` (API V5, on ``wh.route4me.com``) with ``name``,
``accountable_person_id``, ``external_id`` and ``currency`` as the JSON body, and prints the new
customer. The customer data is a sample: change it before you run this.

Run it with::

    python examples/customers/create_customer.py --api_key <your key> --accountable_person_id <member ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, accountable_person_id):
    """Create a sample customer and print it.

    :param api_key: Route4Me API key.
    :param accountable_person_id: ID of the member accountable for the customer.
    """
    route4me = Route4Me(api_key)

    customers = route4me.customers
    response = customers.create_customer(
        name="Example Customer",
        accountable_person_id=accountable_person_id,
        external_id="EXAMPLE-CUSTOMER-1",
        currency="USD",
    )
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Customer")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--accountable_person_id",
        dest="accountable_person_id",
        help="ID of the member accountable for the customer",
        type=int,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.accountable_person_id)
