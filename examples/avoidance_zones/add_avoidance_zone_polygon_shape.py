"""Create a polygon avoidance zone, an area that routes must avoid.

Calls :meth:`AvoidanceZones.add_avoidance_zone
<route4me.avoidance_zones.AvoidanceZones.add_avoidance_zone>`, which sends
``POST /api.v4/avoidance.php`` with the zone as the JSON body: ``territory_name``, ``territory_color``
and ``territory``, of type ``poly``, whose ``data`` is its vertices, each as ``"lat,lng"``. Prints the
new zone. The zone stays in the account; delete_avoidance_zone.py shows how to remove one.

Run it with::

    python examples/avoidance_zones/add_avoidance_zone_polygon_shape.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create a polygon avoidance zone and print it.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    avoidance_zones = route4me.avoidance_zones
    print("Creating Polygon Shape Zone")
    territory = {
        "territory_name": "Polygon Territory",
        "territory_color": "ff0000",
        "territory": {
            "type": "poly",
            "data": [
                "56.127184156131065,56.93115234375",
                "58.41322259056806,59.501953125",
                "61.53840616716746,59.315185546875",
                "61.047650586031104,51.998291015625",
                "59.254649544483726,53.63525390625",
                "56.47462805805596,54.42626953125",
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
    parser = argparse.ArgumentParser(description="Add Polygon Avoidance Zone")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
