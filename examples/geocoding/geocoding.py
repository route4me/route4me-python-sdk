"""Geocode addresses one at a time, retrying failures.

Calls :meth:`Address.fix_geocode <route4me.address.Address.fix_geocode>` for each of five Louisville,
Kentucky addresses. It sends ``GET /api/address.php``, copies the ``lat`` and ``lng`` of the first match
into the address dict, and retries connection errors with backoff. Prints each address before and after.

Run it with::

    python examples/geocoding/geocoding.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Geocode the sample addresses and print them.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    addresses = [
        {"address": "455 S 4th St, Louisville, KY 40202"},
        {"address": "1604 PARKRIDGE PKWY, Louisville, KY, 40214"},
        {"address": "1407 MCCOY, Louisville, KY, 40215"},
        {"address": "4805 BELLEVUE AVE, Louisville, KY, 40215"},
        {"address": "730 CECIL AVENUE, Louisville, KY, 40211"},
    ]
    for address in addresses:
        print(f"Original Address: {address}")
        geocode_error, address = route4me.address.fix_geocode(address)
        if geocode_error:
            print(f"Geocoding Error: {geocode_error}")
        print(f"Geocoded Address: {address}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Geocoding")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
