"""List the account's active vehicles with API V5.

Calls :meth:`VehiclesV5.get_vehicles <route4me.vehicles_v5.VehiclesV5.get_vehicles>`, which sends
``GET /modules/api/v5.0/vehicles`` (API V5, on ``wh.route4me.com``), and prints the reply.

Run it with::

    python examples/vehicles/get_vehicles_v5.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the active vehicles.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicles_v5.get_vehicles(show="active")
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Vehicles (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
