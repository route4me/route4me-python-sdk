"""Get an avoidance zone by ID.

Calls :meth:`AvoidanceZones.get_avoidance_zones
<route4me.avoidance_zones.AvoidanceZones.get_avoidance_zones>` (``GET /api.v4/avoidance.php``) to pick
the first zone, then :meth:`AvoidanceZones.get_avoidance_zone
<route4me.avoidance_zones.AvoidanceZones.get_avoidance_zone>` with its ``territory_id``, which sends the
same request with ``territory_id`` in the query, and prints the zone.

Run it with::

    python examples/avoidance_zones/get_avoidance_zone.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first avoidance zone of the account.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    avoidance_zones = route4me.avoidance_zones
    response = avoidance_zones.get_avoidance_zones()
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        territory_id = response[0]["territory_id"]
        print(f"Getting Territory ID: {territory_id}")
        response = avoidance_zones.get_avoidance_zone(territory_id=territory_id)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            print(f"Territory ID: {response['territory_id']}")
            print(f"\tTerritory Name: {response['territory_name']}")
            print(f"\tTerritory Color: {response['territory_color']}")
            print(f"\tMember ID: {response['member_id']}")
            print(f"\tTerritory Type: {response['territory']['type']}")
            if response["territory"]["data"]:
                print("\tData: ")
                for data in response["territory"]["data"]:
                    print(f"\t\t{data}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Avoidance Zone")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
