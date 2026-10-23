"""Record a batch of GPS pings of a device on a route.

Calls :meth:`GPS.set_tracking_pings <route4me.gps.GPS.set_tracking_pings>`, which sends
``POST /track/set.php`` with ``member_id``, ``device_guid``, ``device_type`` and ``speed_unit`` and the
pings in ``items`` as the JSON body, and prints the reply. The pings are samples, one minute apart and
ending now: the API rejects pings older than 7 days. ``EXAMPLE-DEVICE`` is a sample device GUID.

Run it with::

    python examples/tracking/set_tracking_pings.py --api_key <your key> --member_id <member ID> \\
        --route_id <route ID>
"""

import argparse
import time

from route4me import Route4Me

POSITIONS = [(40.7636197, -73.9744388), (40.7615691, -73.9764938), (40.7590403, -73.9799270)]


def main(api_key, member_id, route_id):
    """Record three pings on the route and print the reply.

    :param api_key: Route4Me API key.
    :param member_id: ID of the member who drives the route.
    :param route_id: ID of the route.
    """
    route4me = Route4Me(api_key)

    now = int(time.time())
    items = [
        {
            "lat": lat,
            "lng": lng,
            "route_id": route_id,
            "speed": 12.5,
            "course": 225,
            "device_timestamp": now - 60 * (len(POSITIONS) - 1 - i),
        }
        for i, (lat, lng) in enumerate(POSITIONS)
    ]
    gps = route4me.gps
    response = gps.set_tracking_pings(
        member_id=member_id,
        device_guid="EXAMPLE-DEVICE",
        device_type="iphone",
        speed_unit="m/s",
        items=items,
    )
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set GPS Tracking Pings")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--member_id", dest="member_id", help="Member ID", type=int, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.member_id, args.route_id)
