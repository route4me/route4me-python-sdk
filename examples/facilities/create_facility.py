"""Create a facility with API V5.

Calls :meth:`Facilities.create_facility <route4me.facilities.Facilities.create_facility>`, which sends
``POST /modules/api/v5.0/facilities`` (API V5, on ``wh.route4me.com``) with ``facility_alias``,
``address``, ``coordinates``, ``facility_types`` and ``status`` as the JSON body, and prints the new
facility. The facility is a sample: use a facility type of your account, which
``examples/facilities/get_facility_types.py`` lists.

Run it with::

    python examples/facilities/create_facility.py --api_key <your key> --facility_type_id <type ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, facility_type_id):
    """Create a sample facility and print it.

    :param api_key: Route4Me API key.
    :param facility_type_id: ID of the facility type of the new facility.
    """
    route4me = Route4Me(api_key)

    facilities = route4me.facilities
    response = facilities.create_facility(
        facility_alias="Example Depot",
        address="754 5th Ave, New York, NY 10019",
        coordinates={"lat": 40.7636197, "lng": -73.9744388},
        facility_types=[{"facility_type_id": facility_type_id, "is_default": True}],
        status=1,
    )
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Facility")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--facility_type_id", dest="facility_type_id", help="Facility type ID", type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.facility_type_id)
