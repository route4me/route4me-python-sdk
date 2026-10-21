import argparse

from route4me import Route4Me


def main(api_key):
    r4m = Route4Me(api_key)

    route = r4m.route
    response = route.get_routes(limit=2, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        route_id1 = response[0]["route_id"]
        route_id2 = response[1]["route_id"]
        data = {"route_ids": f"{route_id1},{route_id2}"}
        print(f"Routes to merge: {data['route_ids']}")
        response = route.merge_routes(**data)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            print(f"Optimization Problem ID: {response['optimization_problem_id']} - Status: {response['status']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge Two Routes")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
