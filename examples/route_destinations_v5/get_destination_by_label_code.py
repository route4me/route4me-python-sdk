r"""Find a destination by its label code.

Calls :meth:`RouteDestinationsV5.get_destination_by_label_code
<route4me.route_destinations_v5.RouteDestinationsV5.get_destination_by_label_code>`, which sends
``GET /modules/api/v5.0/route-destinations/sorting`` (API V5, on ``wh.route4me.com``) with ``label_code``
in the query, and prints the destination with its route and stop number.

Run it with::

    python examples/route_destinations_v5/get_destination_by_label_code.py --api_key <your key> \
        --label_code <label code>
"""

import argparse

from route4me import Route4Me


def main(api_key, label_code):
    """Print the destination that has the label code.

    :param api_key: Route4Me API key.
    :param label_code: label code of the destination.
    """
    route4me = Route4Me(api_key)

    response = route4me.route_destinations_v5.get_destination_by_label_code(label_code)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Destination by Label Code (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--label_code", dest="label_code", help="Label code of the destination", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.label_code)
