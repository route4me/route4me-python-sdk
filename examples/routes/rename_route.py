r"""Rename a route.

Calls :meth:`Route.rename_route <route4me.route.Route.rename_route>`, which sends
``POST /actions/route/rename_route.php`` with ``route_id`` and ``route_name`` as form fields, and prints
the reply.

Run it with::

    python examples/routes/rename_route.py --api_key <your key> --route_id <route id> \
        --route_name <route name>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id, route_name):
    """Rename the route and print the reply.

    :param api_key: Route4Me API key.
    :param route_id: route ID.
    :param route_name: new name of the route.
    """
    route4me = Route4Me(api_key)

    response = route4me.route.rename_route(route_id, route_name)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename a Route")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route ID", type=str, required=True)
    parser.add_argument("--route_name", dest="route_name", help="New name of the route", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id, args.route_name)
