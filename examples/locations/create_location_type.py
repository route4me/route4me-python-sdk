"""Create a location type with API V5.

Calls :meth:`Locations.create_location_type <route4me.locations.Locations.create_location_type>`,
which sends ``POST /modules/api/v5.0/address-book/locations/types`` (API V5, on ``wh.route4me.com``)
with ``name``, ``description``, ``is_parent_type`` and ``is_child_type`` as the JSON body, and prints
the new location type. The type is a sample: change it before you run this.

Run it with::

    python examples/locations/create_location_type.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create a sample location type and print it.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    locations = route4me.locations
    response = locations.create_location_type(
        name="Example Warehouse",
        description="A sample type for sites that hold other locations",
        is_parent_type=True,
        is_child_type=False,
    )
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Location Type")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
