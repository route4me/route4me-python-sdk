"""Create three territories: a polygon, a circle and a rectangle.

Calls :meth:`Territory.add_territory <route4me.territory.Territory.add_territory>` once per shape, which
sends ``POST /api.v4/territory.php`` with ``territory_name``, ``territory_color`` and ``territory``
(type ``poly``, ``circle`` or ``rect``, and its data) as the JSON body, and prints each new territory.
They stay in the account; delete_territory.py shows how to remove one.

Run it with::

    python examples/territory/add_territory.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create the three territories and print them.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    territories = route4me.territory
    print("Creating Poly Territory")
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
        print(f"Territory ID: {response['territory_id']}")
        print(f"\tTerritory Name: {response['territory_name']}")
        print(f"\tTerritory Color: {response['territory_color']}")
        print(f"\tMember ID: {response['member_id']}")
        print(f"\tTerritory Type: {response['territory']['type']}")
        if response["territory"]["data"]:
            print("\tData:")
            for data in response["territory"]["data"]:
                print(f"\t\t{data}")
    print("Creating Circle Territory")
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
    response = territories.add_territory(**territory)
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
    print("Creating Rect Territory")
    territory = {
        "territory_name": "Rect Territory",
        "territory_color": "ff0000",
        "territory": {
            "type": "rect",
            "data": ["43.51668853502909,-109.3798828125", "46.98025235521883,-101.865234375"],
        },
    }
    response = territories.add_territory(**territory)
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
    parser = argparse.ArgumentParser(description="Add Territory")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
