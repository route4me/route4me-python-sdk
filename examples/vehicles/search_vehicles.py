r"""Search the given vehicles around a location.

Calls :meth:`VehiclesV5.search_vehicles <route4me.vehicles_v5.VehiclesV5.search_vehicles>`, which sends
``POST /modules/api/v5.0/vehicles/search`` (API V5, on ``wh.route4me.com``), and prints the reply.

Run it with::

    python examples/vehicles/search_vehicles.py --api_key <your key> \
        --vehicle_ids <vehicle ID> <vehicle ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, vehicle_ids):
    """Search the vehicles around a sample location and print them.

    :param api_key: Route4Me API key.
    :param vehicle_ids: IDs of the vehicles.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicles_v5.search_vehicles(vehicle_ids=vehicle_ids, lat=40.7128, lng=-74.006)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Vehicles")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--vehicle_ids", dest="vehicle_ids", help="One or more vehicle IDs", type=str, required=True, nargs="+"
    )
    args = parser.parse_args()
    main(args.api_key, args.vehicle_ids)
