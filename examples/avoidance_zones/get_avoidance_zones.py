import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    avoidance_zones = route4me.avoidance_zones
    response = avoidance_zones.get_avoidance_zones()
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        for i, territory in enumerate(response):
            print("{}  - Territory ID: {}".format(i + 1, territory["territory_id"]))
            print("\tTerritory Name: {}".format(territory["territory_name"]))
            print("\tTerritory Color: {}".format(territory["territory_color"]))
            print("\tMember ID: {}".format(territory["member_id"]))
            print("\tTerritory Type: {}".format(territory["territory"]["type"]))
            if territory["territory"]["data"]:
                print("\tData:")
                for data in territory["territory"]["data"]:
                    print(f"\t\t{data}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Avoidance Zones")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
