"""List the account's avoidance zones.

Calls :meth:`AvoidanceZones.get_avoidance_zones
<route4me.avoidance_zones.AvoidanceZones.get_avoidance_zones>`, which sends
``GET /api.v4/avoidance.php``, and prints the name, colour, owner, shape and data of each zone.

Run it with::

    python examples/avoidance_zones/get_avoidance_zones.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print every avoidance zone.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    avoidance_zones = route4me.avoidance_zones
    response = avoidance_zones.get_avoidance_zones()
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        for i, territory in enumerate(response):
            print(f"{i + 1}  - Territory ID: {territory['territory_id']}")
            print(f"\tTerritory Name: {territory['territory_name']}")
            print(f"\tTerritory Color: {territory['territory_color']}")
            print(f"\tMember ID: {territory['member_id']}")
            print(f"\tTerritory Type: {territory['territory']['type']}")
            if territory["territory"]["data"]:
                print("\tData:")
                for data in territory["territory"]["data"]:
                    print(f"\t\t{data}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Avoidance Zones")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
