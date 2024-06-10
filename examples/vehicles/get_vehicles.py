# -*- coding: utf-8 -*-

import argparse
from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    vehicles = route4me.vehicles
    response = vehicles.get_vehicles()
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response.get("errors")))
    else:
        for vehicle in response:
            print(
                "Vehicle ID: {0}\tVehicle Alias: {1}".format(
                    vehicle.get("vehicle_id"), vehicle.get("vehicle_alias")
                )
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Vehicles")
    parser.add_argument(
        "--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key)
