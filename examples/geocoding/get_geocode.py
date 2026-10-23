"""Geocode a single address.

Calls :meth:`Address.get_geocode <route4me.address.Address.get_geocode>` with
``{"format": "json", "address": ...}``, which sends ``GET /api/address.php``. The geocoder answers with
a list of matches; each is printed with its name, coordinates, type and confidence. forward_geocoding.py
geocodes several addresses in one request instead.

Run it with::

    python examples/geocoding/get_geocode.py --api_key <your key> [--address "<address>"]
"""

import argparse

from route4me import Route4Me


def main(api_key, address):
    """Geocode one address and print the matches.

    :param api_key: Route4Me API key.
    :param address: the address to geocode.
    """
    route4me = Route4Me(api_key)

    print(f"Geocoding this address: {address}")
    response = route4me.address.get_geocode({"format": "json", "address": address})
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        for i, match in enumerate(response):
            print(f"Match #{i + 1}")
            print(f"\tName: {match.get('name')}")
            print(f"\tLatitude: {match.get('lat')}")
            print(f"\tLongitude: {match.get('lng')}")
            print(f"\tType: {match.get('type')}")
            print(f"\tConfidence: {match.get('confidence')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Geocode a Single Address")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--address",
        dest="address",
        help="Address to geocode",
        type=str,
        default="754 5th Ave New York, NY 10019",
    )
    args = parser.parse_args()
    main(args.api_key, args.address)
