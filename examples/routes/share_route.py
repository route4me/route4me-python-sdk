"""Share the latest route by email.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` and
:meth:`Route.get_route <route4me.route.Route.get_route>` (``GET /api.v4/route.php``) to read the latest
route, then :meth:`Route.share_route <route4me.route.Route.share_route>` with ``recipient_email`` and
``response_format="json"``, which sends ``POST /actions/route/share_route.php`` with ``route_id`` and
``response_format`` in the query and ``recipient_email`` as the JSON body, and prints the reply. Change
the sample recipient before running it.

Run it with::

    python examples/routes/share_route.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Share the latest route and print the reply.

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
            data = {"recipient_email": "recipient@example.com", "route_id": route_id, "response_format": "json"}
            response = route.share_route(**data)
            print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Share a Route")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
