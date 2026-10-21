"""Create a circular avoidance zone, an area that routes must avoid.

Calls :meth:`AvoidanceZones.add_avoidance_zone
<route4me.avoidance_zones.AvoidanceZones.add_avoidance_zone>`, which sends
``POST /api.v4/avoidance.php`` with the zone as the JSON body: ``territory_name``, ``territory_color``
and ``territory``, of type ``circle``, whose ``data`` is the centre, as ``"lat,lng"``, and the radius.
Prints the new zone. The zone stays in the account; delete_avoidance_zone.py shows how to remove one.

Run it with::

    python examples/avoidance_zones/add_avoidance_zone_circular_shape.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create a circular avoidance zone and print it.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    avoidance_zones = route4me.avoidance_zones
    print("Creating Circle Shape Zone")
    territory = {
        "territory_name": "Circle Territory",
        "territory_color": "ff0000",
        "territory": {
            "type": "circle",
            "data": [
                "37.569752822786455,-77.47833251953125",
                "5000",
            ],
        },
    }
    response = avoidance_zones.add_avoidance_zone(**territory)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        print(f"Territory ID: {response['territory_id']}")
        print(f"\tTerritory Name: {response['territory_name']}")
        print(f"\tTerritory Color: {response['territory_color']}")
        print(f"\tMember ID: {response['member_id']}")
        print(f"\tTerritory Type: {response['territory']['type']}")
        if response["territory"]["data"]:
            print("\tData:")
            for data in response["territory"]["data"]:
                print(f"\t\t{data}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add Circular Avoidance Zone")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
