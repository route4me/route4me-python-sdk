r"""Find the routes best suited to take a new stop.

Calls :meth:`RoutesV5.dynamic_insert_route_addresses
<route4me.routes_v5.RoutesV5.dynamic_insert_route_addresses>`, which sends
``POST /modules/api/v5.0/routes/lookup-for-new-destination`` (API V5, on ``wh.route4me.com``) with the
location of the stop, the date and the number of results as the JSON body, and prints the candidate
insertions. Nothing is changed.

Run it with::

    python examples/routes_v5/dynamic_insert_route_addresses.py --api_key <your key> --lat <lat> \
        --lng <lng> --scheduled_for <scheduled for>
"""

import argparse

from route4me import Route4Me


def main(api_key, lat, lng, scheduled_for):
    """Print the routes where the new stop fits best.

    :param api_key: Route4Me API key.
    :param lat: latitude of the new stop.
    :param lng: longitude of the new stop.
    :param scheduled_for: date, YYYY-MM-DD.
    """
    route4me = Route4Me(api_key)

    response = route4me.routes_v5.dynamic_insert_route_addresses(
        lat=lat, lng=lng, scheduled_for=scheduled_for, lookup_results_limit=3
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamic Insert of a Stop (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--lat", dest="lat", help="Latitude of the new stop", type=float, required=True)
    parser.add_argument("--lng", dest="lng", help="Longitude of the new stop", type=float, required=True)
    parser.add_argument("--scheduled_for", dest="scheduled_for", help="Date, YYYY-MM-DD", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.lat, args.lng, args.scheduled_for)
