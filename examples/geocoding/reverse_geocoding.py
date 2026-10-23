"""Find the address at a coordinate.

Calls :meth:`Address.geocode <route4me.address.Address.geocode>` with
``addresses="42.35863,-71.05670"``, which sends ``POST /api/geocoder.php``; given coordinates, the
geocoder returns the address there. Prints the raw reply, CSV by default.

Run it with::

    python examples/geocoding/reverse_geocoding.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Reverse-geocode the sample coordinate and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    coordinate = "42.35863,-71.05670"
    print(f"Getting Address from this coordinate: {coordinate}")
    response = route4me.address.geocode(addresses=coordinate)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reverse Geocoding")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
