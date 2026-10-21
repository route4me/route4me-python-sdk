"""Get one destination of a route.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` and
:meth:`Route.get_route <route4me.route.Route.get_route>` (``GET /api.v4/route.php``) to read the latest
route, then :meth:`Address.get_address <route4me.address.Address.get_address>` with its ``route_id`` and
the first destination's ``route_destination_id``, which sends ``GET /api.v4/address.php``, and prints
the address.

Run it with::

    python examples/addresses/get_address.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first destination of the latest route.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    route = route4me.route
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        response = route.get_route(route_id=response[0]["route_id"])
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            route_id = response["route_id"]
            route_destination_id = response["addresses"][0]["route_destination_id"]
            response = route4me.address.get_address(route_id=route_id, route_destination_id=route_destination_id)
            if isinstance(response, dict) and "errors" in response.keys():
                print(". ".join(response["errors"]))
            else:
                print(f"Address: {response['address']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get an Address from a Route")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
