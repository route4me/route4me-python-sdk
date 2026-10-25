"""Record a GPS position of a device on the latest route.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` (``GET /api.v4/route.php``) to find the
latest route, sets the position with the :class:`~route4me.gps.GPS` setters (``format``, ``route_id``,
``lat``, ``lng``, ``course``, ``speed``, ``device_type``, ``member_id``, ``device_guid`` and
``device_timestamp``) and sends it with :meth:`GPS.set_gps_track <route4me.gps.GPS.set_gps_track>`,
which sends ``GET /track/set.php`` with them in the query. Prints the reply. ``member_id`` 1 and the
timestamp are samples: use a member of your account.

Run it with::

    python examples/tracking/set_gps_example.py --api_key <your key>
"""

import argparse

from route4me import Route4Me
from route4me.constants import DEVICE_TYPE, FORMAT


def main(api_key):
    """Record a position on the latest route and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)
    route = route4me.route
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        gps = route4me.gps
        gps.format(FORMAT.JSON)
        gps.route_id(response[0]["route_id"])
        gps.lat(33.14384)
        gps.lng(-83.22466)
        gps.course(1)
        gps.speed(120)
        gps.device_type(DEVICE_TYPE.IPHONE, "param")
        gps.member_id(1, "param")
        gps.device_guid("TEST_GPS")
        gps.device_timestamp("2014-06-14 17:43:35")
        print(gps.params.keys())
        print(gps.set_gps_track())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set GPS Tracking Data into a Route")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
