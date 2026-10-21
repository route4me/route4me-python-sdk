"""Record GPS positions on the latest route, then read its tracking history.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` (``GET /api.v4/route.php``) to find the
latest route, sets the values shared by every position once with
:meth:`GPS.add <route4me.base.Base.add>`, and sends four positions with
:meth:`GPS.set_gps_track <route4me.gps.GPS.set_gps_track>` (``GET /track/set.php``). It then reads the
route with :meth:`Route.get_route <route4me.route.Route.get_route>` and ``device_tracking_history=1``
(``GET /api.v4/route.php``) and prints each tracked point. ``member_id`` 1 is a sample: use a member of
your account.

Run it with::

    python examples/tracking/track_device_last_location_history.py --api_key <your key>
"""

import argparse
import datetime as dt

from route4me import Route4Me
from route4me.constants import DEVICE_TYPE, FORMAT


def main(api_key):
    """Record four positions on the latest route and print its tracking history.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    gps = route4me.gps
    route = route4me.route
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        route_id = response[0]["route_id"]
        print(f"Route ID: {route_id}")
        gps.add(
            params={
                "format": FORMAT.JSON,
                "route_id": route_id,
                "lng": -109.0803888,
                "course": 1,
                "device_type": DEVICE_TYPE.IPHONE,
                "member_id": 1,
                "device_guid": "qweqweqwe",
            }
        )
        # SET GPS
        for i in range(4):
            gps.add(
                params={
                    "speed": 120 + i,
                    "device_timestamp": dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S"),
                    "lat": 41.8927521 + i,
                }
            )
            print(f"GPS Params SET {gps.set_gps_track()}")
        route.add(
            params={
                "route_id": route_id,
                "device_tracking_history": 1,
            }
        )
        response = route.get_route()
        for history in response["tracking_history"]:
            print(f"lng: {history['lg']} lat: {history['lt']} time: {history['ts_friendly']} speed: {history['s']} ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Tracking History")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
