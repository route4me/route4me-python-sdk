r"""Delete routes by ID with API V5.

Calls :meth:`RoutesV5.delete_routes <route4me.routes_v5.RoutesV5.delete_routes>`, which sends
``DELETE /modules/api/v5.0/routes/delete`` (API V5, on ``wh.route4me.com``) with a ``route_id`` filter and
the request ``signature`` as the JSON body, and prints the reply. The routes are deleted for good.

Run it with::

    python examples/routes_v5/delete_routes.py --api_key <your key> --route_id <route id> [--route_id ...] \
        --signature <signature>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id, signature):
    """Delete the routes and print the reply.

    :param api_key: Route4Me API key.
    :param route_id: route ID; repeat to delete several.
    :param signature: request signature.
    """
    route4me = Route4Me(api_key)

    response = route4me.routes_v5.delete_routes(filters={"route_id": route_id}, signature=signature)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete Routes (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--route_id",
        dest="route_id",
        help="Route ID; repeat to delete several",
        type=str,
        action="append",
        required=True,
    )
    parser.add_argument("--signature", dest="signature", help="Request signature", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id, args.signature)
