"""Get one facility type with API V5.

Calls :meth:`Facilities.get_facility_type <route4me.facilities.Facilities.get_facility_type>`, which
sends ``GET /modules/api/v5.0/facilities/types/{facility_type_id}`` (API V5, on ``wh.route4me.com``),
and prints the facility type.

Run it with::

    python examples/facilities/get_facility_type.py --api_key <your key> --facility_type_id <type ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, facility_type_id):
    """Print one facility type.

    :param api_key: Route4Me API key.
    :param facility_type_id: ID of the facility type.
    """
    route4me = Route4Me(api_key)

    facilities = route4me.facilities
    response = facilities.get_facility_type(facility_type_id)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Facility Type")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--facility_type_id", dest="facility_type_id", help="Facility type ID", type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.facility_type_id)
