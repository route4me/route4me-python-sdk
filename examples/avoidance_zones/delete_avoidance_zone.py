"""Create an avoidance zone, then delete it.

Calls :meth:`AvoidanceZones.add_avoidance_zone
<route4me.avoidance_zones.AvoidanceZones.add_avoidance_zone>` (``POST /api.v4/avoidance.php``) to create
a polygon zone, then :meth:`AvoidanceZones.delete_avoidance_zone
<route4me.avoidance_zones.AvoidanceZones.delete_avoidance_zone>` with its ``territory_id``, which sends
``DELETE /api.v4/avoidance.php``, and prints the status.

Run it with::

    python examples/avoidance_zones/delete_avoidance_zone.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create a polygon avoidance zone, delete it and print the status.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    avoidance_zones = route4me.avoidance_zones
    print("Creating Poly Zone")
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
        territory_id = response["territory_id"]
        print(f"Territory ID: {territory_id} -> Created")
        response = avoidance_zones.delete_avoidance_zone(territory_id=territory_id)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            print(f"Territory ID: {territory_id} -> Deleted: {response['status']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete Avoidance Zone")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
