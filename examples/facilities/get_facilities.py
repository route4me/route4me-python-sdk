"""List the first page of facilities with API V5.

Calls :meth:`Facilities.get_facilities <route4me.facilities.Facilities.get_facilities>` with ``page=1``
and ``per_page=10``, which sends ``GET /modules/api/v5.0/facilities`` (API V5, on ``wh.route4me.com``)
with them in the query, and prints the ID and alias of each facility.

Run it with::

    python examples/facilities/get_facilities.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first ten facilities.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    facilities = route4me.facilities
    response = facilities.get_facilities(page=1, per_page=10)
    if isinstance(response, dict) and "errors" in response.keys():
        print(response["errors"])
    else:
        for facility in response.get("data", []):
            print(f"{facility.get('facility_id')}\t{facility.get('facility_alias')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Facilities")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
