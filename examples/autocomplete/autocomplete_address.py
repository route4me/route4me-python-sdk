"""Get address suggestions for a partly typed address.

Calls :meth:`Autocomplete.autocomplete_address <route4me.autocomplete.Autocomplete.autocomplete_address>`,
which sends ``GET /autocomplete.php`` with the ``--param`` values as the query, and prints the reply.
The endpoint's parameter names are not documented, so the example passes on whatever you give it.

Run it with::

    python examples/autocomplete/autocomplete_address.py --api_key <your key> --param <name>=<partial address>
"""

import argparse
import json

from route4me import Route4Me


def main(api_key, params):
    """Print the suggestions.

    :param api_key: Route4Me API key.
    :param params: query parameters, as ``name=value`` strings.
    """
    route4me = Route4Me(api_key)

    autocomplete = route4me.autocomplete
    query = dict(param.split("=", 1) for param in params)
    response = autocomplete.autocomplete_address(**query)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    elif isinstance(response, bytes):
        print(response.decode("utf-8", errors="replace"))
    else:
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autocomplete an Address")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--param", dest="params", help="Query parameter, name=value", action="append", default=[])
    args = parser.parse_args()
    main(args.api_key, args.params)
