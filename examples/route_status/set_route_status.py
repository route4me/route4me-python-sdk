r"""Set the status of a route.

Calls :meth:`RouteStatus.set_route_status <route4me.route_status.RouteStatus.set_route_status>`, which
sends ``POST /modules/api/v5.0/route-status/{route_id}`` (API V5, on ``wh.route4me.com``) with
``status``, ``lat``, ``lng`` and ``event_timestamp`` (the current time) as the JSON body, and prints the
reply. ``--status`` is a ``ROUTE_STATUS`` value: planned, started, paused, resumed or completed.

Run it with::

    python examples/route_status/set_route_status.py --api_key <your key> --route_id <route ID> \
        --status started --lat <latitude> --lng <longitude>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id, status, lat, lng):
    """Set the status of the route and print the reply.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    :param status: the new status, e.g. ``"started"``.
    :param lat: latitude where the status changed.
    :param lng: longitude where the status changed.
    """
    r4m = Route4Me(api_key)

    route = r4m.route_status
    print(f"Route ID: {route_id}")
    print(f"Latitude: {lat} - Longitude: {lng}")
    response = route.set_route_status(route_id=route_id, status=status, lat=lat, lng=lng)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set Route Status")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route4Me Route ID", type=str, required=True)
    parser.add_argument(
        "--status",
        dest="status",
        help="Route Status: planned, started, paused, resumed or completed",
        type=str,
        required=True,
    )
    parser.add_argument("--lat", dest="lat", help="Latitude", type=float, required=True)
    parser.add_argument("--lng", dest="lng", help="Longitude", type=float, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id, args.status, args.lat, args.lng)
