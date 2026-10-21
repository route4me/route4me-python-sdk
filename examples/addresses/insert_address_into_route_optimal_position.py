import argparse

from route4me import Route4Me


def main(api_key):
    r4m = Route4Me(api_key)

    route = r4m.route
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        route_id = response[0]["route_id"]
        print(f"Route ID: {route_id}")
        response = route.get_route(route_id=route_id)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            data = {
                "addresses": [
                    {
                        "address": "Cabo Rojo, Cabo Rojo 00623, Puerto Rico",
                        "alias": "Cabo Rojo, Cabo Rojo 00623, Puerto Rico",
                        "lat": 18.086627,
                        "lng": -67.145735,
                        "curbside_lat": 18.086627,
                        "curbside_lng": -67.145735,
                        "contact_id": False,
                        "is_departed": False,
                        "is_visited": False,
                    }
                ],
                "optimal_position": True,
                "route_id": route_id,
            }
            response = route.insert_address_into_route_optimal_position(**data)
            print(f"Optimization Problem ID: {response['optimization_problem_id']}")
            print(f"Route ID: {response['route_id']}")
            for i, address in enumerate(response["addresses"]):
                print(f"Address #{i + 1}")
                print(f"\tAddress: {address['address']}")
                print(f"\tRoute Destination ID: {address['route_destination_id']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert an address into a Route at Optimal Position")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
