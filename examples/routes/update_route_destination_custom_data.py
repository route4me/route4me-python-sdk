"""Set custom data on a route destination.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` and
:meth:`Route.get_route <route4me.route.Route.get_route>` (``GET /api.v4/route.php``) to read the latest
route, then :meth:`Route.update_route_destination_custom_data
<route4me.route.Route.update_route_destination_custom_data>` for its second destination with
``custom_fields={"SDK": "Python"}``, which sends ``PUT /api.v4/address.php`` with ``route_id`` and
``route_destination_id`` in the query and ``custom_fields`` as the JSON body. This changes a destination
of the latest route.

Run it with::

    python examples/routes/update_route_destination_custom_data.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Set custom data on a destination of the latest route and print it.

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
            route_destination_id = response["addresses"][1]["route_destination_id"]
            print(f"Route Destination ID: {route_destination_id}")
            data = {
                "route_destination_id": route_destination_id,
                "route_id": route_id,
                "custom_fields": {"SDK": "Python"},
            }
            response = route.update_route_destination_custom_data(**data)
            print(f"Route ID: {route_id}")
            print(f"\tAddress: {response['address']}")
            print(f"\tRoute Destination ID: {response['route_destination_id']}")
            print(f"\tCustom Fields: {response['custom_fields']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Route Destination Custom Data")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
