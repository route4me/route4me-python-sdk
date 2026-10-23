"""Rename a customer with API V5.

Calls :meth:`Customers.update_customer <route4me.customers.Customers.update_customer>`, which sends
``PUT /modules/api/v5.0/customers/{customer_id}`` (API V5, on ``wh.route4me.com``) with the new
``name`` as the JSON body, and prints the updated customer.

Run it with::

    python examples/customers/update_customer.py --api_key <your key> --customer_id <customer ID> --name <new name>
"""

import argparse

from route4me import Route4Me


def main(api_key, customer_id, name):
    """Rename the customer and print it.

    :param api_key: Route4Me API key.
    :param customer_id: ID of the customer.
    :param name: the new name of the customer.
    """
    route4me = Route4Me(api_key)

    customers = route4me.customers
    response = customers.update_customer(customer_id, name=name)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a Customer")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--customer_id", dest="customer_id", help="Customer ID", type=str, required=True)
    parser.add_argument("--name", dest="name", help="New customer name", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.customer_id, args.name)
