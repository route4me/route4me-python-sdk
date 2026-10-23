r"""Set the status of one or more routes to planned.

Calls :meth:`RouteStatus.update_route_status_as_planned
<route4me.route_status.RouteStatus.update_route_status_as_planned>`, which sends
``POST /modules/api/v5.0/route-status/planned`` (API V5, on ``wh.route4me.com``) with ``route_ids`` as
the JSON body, and prints the reply. This changes the status of the routes.

Run it with::

    python examples/route_status/update_route_status_as_planned.py --api_key <your key> \
        --route_ids <route ID> [<route ID> ...]
"""

import argparse

from route4me import Route4Me


def main(api_key, route_ids):
    """Set the routes to planned and print the reply.

    :param api_key: Route4Me API key.
    :param route_ids: IDs of the routes.
    """
    route4me = Route4Me(api_key)

    response = route4me.route_status.update_route_status_as_planned(route_ids)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Route Status As Planned")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_ids", dest="route_ids", help="Route4Me Route IDs", type=str, required=True, nargs="+")
    args = parser.parse_args()
    main(args.api_key, args.route_ids)
