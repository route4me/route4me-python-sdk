"""Get a territory by ID.

Calls :meth:`Territory.get_territories <route4me.territory.Territory.get_territories>`
(``GET /api.v4/territory.php``) to pick the first territory, then :meth:`Territory.get_territory
<route4me.territory.Territory.get_territory>` with its ``territory_id``, which sends the same request
with ``territory_id`` in the query, and prints the territory.

Run it with::

    python examples/territory/get_territory.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first territory of the account.

    :param api_key: Route4Me API key.
    """
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
            print(f"Territory ID: {territory['territory_id']}")
            print(f"\tTerritory Name: {territory['territory_name']}")
            print(f"\tTerritory Color: {territory['territory_color']}")
            print(f"\tMember ID: {territory['member_id']}")
            print(f"\tTerritory Type: {territory['territory']['type']}")
            if territory["territory"]["data"]:
                print("\tData:")
                for data in territory["territory"]["data"]:
                    print(f"\t\t{data}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Territory")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
