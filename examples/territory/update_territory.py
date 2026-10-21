"""Create a territory, then update it.

Calls :meth:`Territory.add_territory <route4me.territory.Territory.add_territory>`
(``POST /api.v4/territory.php``) to create a polygon territory, then :meth:`Territory.update_territory
<route4me.territory.Territory.update_territory>` with its ``territory_id``, a new name and a new colour,
which sends ``PUT /api.v4/territory.php`` with ``territory_id`` in the query and the territory as the
JSON body. Prints the territory before and after. The territory stays in the account.

Run it with::

    python examples/territory/update_territory.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create a territory, rename and recolour it, and print it.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    territories = route4me.territory
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
    response = territories.add_territory(**territory)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        territory_id = response["territory_id"]
        print(f"Territory ID: {territory_id} -> Created")
        print(f"\tTerritory Name: {response['territory_name']}")
        print(f"\tTerritory Color: {response['territory_color']}")
        print(f"\tMember ID: {response['member_id']}")
        print(f"\tTerritory Type: {response['territory']['type']}")
        if response["territory"]["data"]:
            print("\tData:")
            for data in response["territory"]["data"]:
                print(f"\t\t{data}")
        territory = {
            "territory_name": "Polygon Territory Updated",
            "territory_color": "ff00ff",
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
        response = territories.update_territory(territory_id=territory_id, **territory)
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
    parser = argparse.ArgumentParser(description="Update an existing Territory")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
