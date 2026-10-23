"""Get the best visiting sequence of four New York locations.

Calls :meth:`RouteDestinationsV5.get_destination_sequence
<route4me.route_destinations_v5.RouteDestinationsV5.get_destination_sequence>`, which sends
``POST /modules/api/v5.0/route-destinations/sequence`` (API V5, on ``wh.route4me.com``) with the
``coordinates`` as the JSON body, and prints the sequenced locations.

Run it with::

    python examples/route_destinations_v5/get_destination_sequence.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the sequence of the four locations.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    coordinates = [
        {"lat": 40.7636197, "lng": -73.9744388},
        {"lat": 40.7669692, "lng": -73.9693864},
        {"lat": 40.7715154, "lng": -73.9669241},
        {"lat": 40.7772129, "lng": -73.9669},
    ]
    response = route4me.route_destinations_v5.get_destination_sequence(coordinates)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Destination Sequence (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
