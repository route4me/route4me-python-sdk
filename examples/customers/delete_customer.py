"""Delete a customer with API V5.

Calls :meth:`Customers.delete_customer <route4me.customers.Customers.delete_customer>`, which sends
``DELETE /modules/api/v5.0/customers/{customer_id}`` (API V5, on ``wh.route4me.com``). The API answers
``204 No Content`` on success, so the example prints a confirmation, or the errors. This deletes the
customer.

Run it with::

    python examples/customers/delete_customer.py --api_key <your key> --customer_id <customer ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, customer_id):
    """Delete the customer and print the outcome.

    :param api_key: Route4Me API key.
    :param customer_id: ID of the customer.
    """
    route4me = Route4Me(api_key)

    customers = route4me.customers
    response = customers.delete_customer(customer_id)
    if isinstance(response, dict) and "errors" in response.keys():
        print(response["errors"])
    else:
        print(f"Customer {customer_id} deleted")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete a Customer")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--customer_id", dest="customer_id", help="Customer ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.customer_id)
