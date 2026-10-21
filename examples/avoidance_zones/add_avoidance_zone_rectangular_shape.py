import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    avoidance_zones = route4me.avoidance_zones
    print("Creating Rectangular Shape Zone")
    territory = {
        "territory_name": "Rect Territory",
        "territory_color": "ff0000",
        "territory": {
            "type": "rect",
            "data": ["43.51668853502909,-109.3798828125", "46.98025235521883,-101.865234375"],
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
    parser = argparse.ArgumentParser(description="Add Rectangular Avoidance Zone")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
