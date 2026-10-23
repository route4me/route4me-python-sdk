"""Rename a location type with API V5.

Calls :meth:`Locations.get_location_type_by_id <route4me.locations.Locations.get_location_type_by_id>`
(``GET /modules/api/v5.0/address-book/locations/types/{location_type_id}``) to read the type, then
:meth:`Locations.update_location_type <route4me.locations.Locations.update_location_type>`, which sends
``PUT /modules/api/v5.0/address-book/locations/types/{location_type_id}`` (API V5, on
``wh.route4me.com``) with the new ``name`` and the current ``is_parent_type`` and ``is_child_type`` as
the JSON body, and prints the updated type.

Run it with::

    python examples/locations/update_location_type.py --api_key <your key> --location_type_id <type ID> \\
        --name <new name>
"""

import argparse

from route4me import Route4Me


def main(api_key, location_type_id, name):
    """Rename the location type and print it.

    :param api_key: Route4Me API key.
    :param location_type_id: ID of the location type.
    :param name: the new name of the location type.
    """
    route4me = Route4Me(api_key)

    locations = route4me.locations
    location_type = locations.get_location_type_by_id(location_type_id)
    if "errors" in location_type.keys():
        print(location_type["errors"])
        return
    response = locations.update_location_type(
        location_type_id,
        name=name,
        is_parent_type=location_type.get("is_parent_type", False),
        is_child_type=location_type.get("is_child_type", False),
    )
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a Location Type")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--location_type_id", dest="location_type_id", help="Location type ID", type=str, required=True)
    parser.add_argument("--name", dest="name", help="New location type name", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.location_type_id, args.name)
