"""Get one facility with API V5.

Calls :meth:`Facilities.get_facility <route4me.facilities.Facilities.get_facility>`, which sends
``GET /modules/api/v5.0/facilities/{facility_id}`` (API V5, on ``wh.route4me.com``), and prints the
facility.

Run it with::

    python examples/facilities/get_facility.py --api_key <your key> --facility_id <facility ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, facility_id):
    """Print one facility.

    :param api_key: Route4Me API key.
    :param facility_id: ID of the facility.
    """
    route4me = Route4Me(api_key)

    facilities = route4me.facilities
    response = facilities.get_facility(facility_id)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Facility")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--facility_id", dest="facility_id", help="Facility ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.facility_id)
