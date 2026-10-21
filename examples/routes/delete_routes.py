"""Delete the two latest routes.

Calls :meth:`Route.get_routes <route4me.route.Route.get_routes>` with ``limit=2``
(``GET /api.v4/route.php``), then :meth:`Route.delete_routes <route4me.route.Route.delete_routes>` with
both IDs, which sends ``DELETE /api.v4/route.php`` with ``route_id`` set to the comma-separated IDs, and
prints the deleted IDs. This deletes the two latest routes of the account.

Run it with::

    python examples/routes/delete_routes.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Delete the two latest routes and print their IDs.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    route = route4me.route
    print("Getting Latest 2 Routes")
    response = route.get_routes(limit=2, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        route_ids = [x["route_id"] for x in response]
        print(f"Route IDs: {route_ids}")
        if len(route_ids) > 0:
            response = route.delete_routes(route_id=route_ids)
            if isinstance(response, dict) and "errors" in response.keys():
                print(". ".join(response["errors"]))
            else:
                print("Routes Deleted:")
                for i, deleted_id in enumerate(response["route_ids"]):
                    print(f"\t{i + 1} - {deleted_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deleting Multiple Routes")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
