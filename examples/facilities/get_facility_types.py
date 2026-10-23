"""List the facility types with API V5.

Calls :meth:`Facilities.get_facility_types <route4me.facilities.Facilities.get_facility_types>`, which
sends ``GET /modules/api/v5.0/facilities/types`` (API V5, on ``wh.route4me.com``), and prints the ID
and name of each type.

Run it with::

    python examples/facilities/get_facility_types.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the facility types.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    facilities = route4me.facilities
    response = facilities.get_facility_types()
    if isinstance(response, dict) and "errors" in response.keys():
        print(response["errors"])
    else:
        for facility_type in response.get("data", []):
            print(f"{facility_type.get('facility_type_id')}\t{facility_type.get('facility_type_alias')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Facility Types")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
