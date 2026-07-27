import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    territories = route4me.territory
    response = territories.get_territories()
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        territory_id = response[0]["territory_id"]
        print(f"Getting Territory ID: {territory_id}")
        response = territories.get_territory(territory_id=territory_id)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            territory = response
            print("Territory ID: {}".format(territory["territory_id"]))
            print("\tTerritory Name: {}".format(territory["territory_name"]))
            print("\tTerritory Color: {}".format(territory["territory_color"]))
            print("\tMember ID: {}".format(territory["member_id"]))
            print("\tTerritory Type: {}".format(territory["territory"]["type"]))
            if territory["territory"]["data"]:
                print("\tData:")
                for data in territory["territory"]["data"]:
                    print(f"\t\t{data}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Territory")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
