r"""Set the status of stops of a route.

Calls :meth:`RouteStatus.set_route_stop_status <route4me.route_status.RouteStatus.set_route_stop_status>`,
which sends ``POST /modules/api/v5.0/route-stop-status`` (API V5, on ``wh.route4me.com``) with
``status`` and ``destination_ids`` as the JSON body, and prints the reply. ``--status`` is Skipped,
Completed, Failed or Empty.

Run it with::

    python examples/route_status/set_route_stop_status.py --api_key <your key> \
        --route_destination_id <route destination id> [--route_destination_id ...] --status <status>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_destination_id, status):
    """Set the status of the stops and print the reply.

    :param api_key: Route4Me API key.
    :param route_destination_id: route destination ID; repeat for several.
    :param status: stop status: Skipped, Completed, Failed or Empty.
    """
    route4me = Route4Me(api_key)

    response = route4me.route_status.set_route_stop_status(status, destination_ids=route_destination_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set Route Stop Status")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--route_destination_id",
        dest="route_destination_id",
        help="Route destination ID; repeat for several",
        type=int,
        action="append",
        required=True,
    )
    parser.add_argument(
        "--status", dest="status", help="Stop status: Skipped, Completed, Failed or Empty", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.route_destination_id, args.status)
