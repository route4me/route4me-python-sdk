"""Get the GPS location history of a member's device on a route.

Calls :meth:`GPS.get_locations <route4me.gps.GPS.get_locations>` with ``format``, ``route_id``,
``member_id`` and ``time_period``, which sends ``GET /api/track/get_device_location.php``. The positions
come back under ``data``; each is printed with its time, coordinates and speed. set_gps_example.py
records a position to read back.

``--time_period`` is optional: ``today`` (the default), ``yesterday``, ``thismonth``, ``7days``,
``14days``, ``30days``, ``60days``, ``90days`` or ``all_time``.

Run it with::

    python examples/tracking/get_device_locations.py --api_key <your key> --route_id <id> --member_id <id>
"""

import argparse

from route4me import Route4Me
from route4me.constants import FORMAT

#: The time_period values that need no start or end date.
TIME_PERIODS = ("today", "yesterday", "thismonth", "7days", "14days", "30days", "60days", "90days", "all_time")


def main(api_key, route_id, member_id, time_period):
    """Print the positions recorded for the route in the time period.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    :param member_id: ID of the member whose device recorded the positions.
    :param time_period: one of :data:`TIME_PERIODS`.
    """
    route4me = Route4Me(api_key)

    gps = route4me.gps
    response = gps.get_locations(
        format=FORMAT.JSON,
        route_id=route_id,
        member_id=member_id,
        time_period=time_period,
    )
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        locations = response.get("data") or []
        print(f"Locations: {len(locations)}")
        for location in locations:
            print(
                f"\t{location.get('ts_friendly')}\tlat: {location.get('lt')}"
                f"\tlng: {location.get('lg')}\tspeed: {location.get('s')}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Device Location History")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="Route ID", type=str, required=True)
    parser.add_argument("--member_id", dest="member_id", help="Member ID", type=int, required=True)
    parser.add_argument(
        "--time_period",
        dest="time_period",
        help="Time period of the history (default: today)",
        choices=TIME_PERIODS,
        default="today",
    )
    args = parser.parse_args()
    main(args.api_key, args.route_id, args.member_id, args.time_period)
