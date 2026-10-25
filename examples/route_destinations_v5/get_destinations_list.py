"""List the destinations of a route with API V5.

Calls :meth:`RouteDestinationsV5.get_destinations_list
<route4me.route_destinations_v5.RouteDestinationsV5.get_destinations_list>`, which sends
``POST /modules/api/v5.0/route-destinations/list`` (API V5, on ``wh.route4me.com``) with a ``route_id``
filter, ``page`` and ``per_page`` as the JSON body, and prints the reply.

Run it with::

    python examples/route_destinations_v5/get_destinations_list.py --api_key <your key> --route_id <route id>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id):
    """Print the first page of the destinations of the route.

    :param api_key: Route4Me API key.
    :param route_id: route ID.
    """
    route4me = Route4Me(api_key)

    response = route4me.route_destinations_v5.get_destinations_list(
        filters={"route_id": [route_id]}, page=1, per_page=20
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the Destination List (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id)
