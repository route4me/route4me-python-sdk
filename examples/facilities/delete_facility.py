"""Delete a facility with API V5.

Calls :meth:`Facilities.delete_facility <route4me.facilities.Facilities.delete_facility>`, which sends
``DELETE /modules/api/v5.0/facilities/{facility_id}`` (API V5, on ``wh.route4me.com``), and prints the
reply. This deletes the facility.

Run it with::

    python examples/facilities/delete_facility.py --api_key <your key> --facility_id <facility ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, facility_id):
    """Delete the facility and print the reply.

    :param api_key: Route4Me API key.
    :param facility_id: ID of the facility.
    """
    route4me = Route4Me(api_key)

    facilities = route4me.facilities
    response = facilities.delete_facility(facility_id)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete a Facility")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--facility_id", dest="facility_id", help="Facility ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.facility_id)
