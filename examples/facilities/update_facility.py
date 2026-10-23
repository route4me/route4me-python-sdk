"""Rename a facility with API V5.

Calls :meth:`Facilities.get_facility <route4me.facilities.Facilities.get_facility>`
(``GET /modules/api/v5.0/facilities/{facility_id}``) to read the facility, then
:meth:`Facilities.update_facility <route4me.facilities.Facilities.update_facility>`, which sends
``PUT /modules/api/v5.0/facilities/{facility_id}`` (API V5, on ``wh.route4me.com``) with the new
``facility_alias`` and the current ``address``, ``coordinates`` and ``facility_types`` as the JSON body,
and prints the updated facility.

Run it with::

    python examples/facilities/update_facility.py --api_key <your key> --facility_id <facility ID> --alias <new alias>
"""

import argparse

from route4me import Route4Me


def main(api_key, facility_id, alias):
    """Rename the facility and print it.

    :param api_key: Route4Me API key.
    :param facility_id: ID of the facility.
    :param alias: the new alias of the facility.
    """
    route4me = Route4Me(api_key)

    facilities = route4me.facilities
    facility = facilities.get_facility(facility_id)
    if "errors" in facility.keys():
        print(facility["errors"])
        return
    facility_types = [
        {"facility_type_id": item.get("facility_type_id"), "is_default": item.get("is_default")}
        for item in facility.get("facility_types", [])
    ]
    response = facilities.update_facility(
        facility_id,
        facility_alias=alias,
        address=facility.get("address"),
        coordinates=facility.get("coordinates"),
        facility_types=facility_types,
    )
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a Facility")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--facility_id", dest="facility_id", help="Facility ID", type=str, required=True)
    parser.add_argument("--alias", dest="alias", help="New facility alias", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.facility_id, args.alias)
