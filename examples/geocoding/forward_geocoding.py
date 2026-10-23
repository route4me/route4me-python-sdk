"""Geocode an address with the batch geocoder.

Calls :meth:`Address.geocode <route4me.address.Address.geocode>` with
``addresses="Boston-Cambridge-Quincy, MA-NH, USA"``, which sends ``POST /api/geocoder.php`` with
``addresses`` as a form field, and prints the raw reply, CSV by default. Several addresses can go in one
request, separated by ``||``; get_geocode.py geocodes one address and returns JSON.

Run it with::

    python examples/geocoding/forward_geocoding.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Geocode the sample address and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address = "Boston-Cambridge-Quincy, MA-NH, USA"
    print(f"Geocoding this address: {address}")
    response = route4me.address.geocode(addresses=address)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Forward Geocoding")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
