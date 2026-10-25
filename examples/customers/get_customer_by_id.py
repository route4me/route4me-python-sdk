"""Get one customer with API V5.

Calls :meth:`Customers.get_customer_by_id <route4me.customers.Customers.get_customer_by_id>`, which sends
``GET /modules/api/v5.0/customers/{customer_id}`` (API V5, on ``wh.route4me.com``), and prints the
customer.

Run it with::

    python examples/customers/get_customer_by_id.py --api_key <your key> --customer_id <customer ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, customer_id):
    """Print one customer.

    :param api_key: Route4Me API key.
    :param customer_id: ID of the customer.
    """
    route4me = Route4Me(api_key)

    customers = route4me.customers
    response = customers.get_customer_by_id(customer_id)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Customer")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--customer_id", dest="customer_id", help="Customer ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.customer_id)
