r"""List the customers that match a text, with API V5.

Calls :meth:`Customers.get_customers_list <route4me.customers.Customers.get_customers_list>`, which
sends ``POST /modules/api/v5.0/customers/list`` (API V5, on ``wh.route4me.com``) with a
``search_query`` filter, ``page`` and ``per_page`` as the JSON body, and prints the reply.

Run it with::

    python examples/customers/get_customers_list.py --api_key <your key> --query <text>
"""

import argparse

from route4me import Route4Me


def main(api_key, query):
    """Print the customers that match ``query``.

    :param api_key: Route4Me API key.
    :param query: text to search for.
    """
    route4me = Route4Me(api_key)

    response = route4me.customers.get_customers_list(filters={"search_query": query}, page=1, per_page=20)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the Customers List (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--query", dest="query", help="Text to search for", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.query)
