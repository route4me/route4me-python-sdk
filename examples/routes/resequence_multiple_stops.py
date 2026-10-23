r"""Move several stops of a route to new positions.

Reads the new positions from a JSON file shaped like ``resequence_data.json``:
``{"addresses": [{"route_destination_id": ..., "sequence_no": ...}]}``. Then calls
:meth:`Route.resequence_multiple_stops <route4me.route.Route.resequence_multiple_stops>`, which sends
``PUT /api.v4/route.php`` with ``route_id`` in the query and the file's content as the JSON body, and
prints the route's addresses. The IDs in ``resequence_data.json`` are samples: use destinations of your
route.

Run it with::

    python examples/routes/resequence_multiple_stops.py --api_key <your key> --route_id <route ID> \
        --route_data_filename examples/routes/resequence_data.json
"""

import argparse
import json

from route4me import Route4Me


def load_json(filename):
    """Read a JSON file.

    :param filename: path of the file.
    :return: the decoded content.
    """
    with open(filename, encoding="utf-8") as datafile:
        return json.load(datafile)


def main(api_key, route_id, route_data_filename):
    """Move the stops listed in the file and print the route.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    :param route_data_filename: path of the JSON file with the new positions.
    """
    r4m = Route4Me(api_key)
    route_data = load_json(route_data_filename)
    route = r4m.route
    print(f"Route ID: {route_id}")
    print("Addresses to be Re-sequence")
    for address in route_data["addresses"]:
        print(
            f"Address Sequence: {address['sequence_no']:6} - Route Destination ID: {address['route_destination_id']:9}"
        )
    print(f"After Resequence the Route {route_id}")
    response = route.resequence_multiple_stops(route_id, route_data)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        for address in response["addresses"]:
            print(
                f"Address Sequence: {address['sequence_no']:6} - "
                f"Route Destination ID: {address['route_destination_id']:9} - Address: {address['address']} "
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Re-sequence Multiple Stops from a Route")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route ID", type=str, required=True)
    parser.add_argument(
        "--route_data_filename",
        dest="route_data_filename",
        help="JSON file name with Route Addresses ID and Sequence",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.route_id, args.route_data_filename)
