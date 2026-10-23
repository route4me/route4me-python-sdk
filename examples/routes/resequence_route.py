"""Move one stop of a route to a new position.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` and
:meth:`Route.get_route <route4me.route.Route.get_route>` (``GET /api.v4/route.php``) to read the latest
route, then :meth:`Route.resequence_route <route4me.route.Route.resequence_route>`, which sends
``PUT /api.v4/route.php`` with ``route_id`` and the second destination's ``route_destination_id`` in the
query, and the third destination with ``sequence_no=6`` in ``addresses`` as the JSON body. Prints the
route before and after. This changes the latest route of the account.

Run it with::

    python examples/routes/resequence_route.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Move a stop of the latest route and print the route.

    :param api_key: Route4Me API key.
    """
    r4m = Route4Me(api_key)

    route = r4m.route
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        route_id = response[0]["route_id"]
        print(f"Route ID: {route_id}")
        response = route.get_route(route_id=route_id)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            print("Original Route")
            print(f"Route ID: {response['route_id']}")
            for i, address in enumerate(response["addresses"]):
                print(f"Address #{i + 1}")
                print(f"\tAddress: {address['address']}")
                print(f"\tRoute Destination ID: {address['route_destination_id']}")
            route_destination_id = response["addresses"][1]["route_destination_id"]
            route_destination_id2 = response["addresses"][2]["route_destination_id"]
            data = {
                "route_destination_id": route_destination_id,
                "route_id": route_id,
                "addresses": [
                    {
                        "route_destination_id": route_destination_id2,
                        "sequence_no": 6,
                    }
                ],
            }
            print("After Re-sequence Route")
            response = route.resequence_route(**data)
            print(f"Route ID: {response['route_id']}")
            for i, address in enumerate(response["addresses"]):
                print(f"Address #{i + 1}")
                print(f"\tAddress: {address['address']}")
                print(f"\tRoute Destination ID: {address['route_destination_id']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Re-sequence a Route")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
