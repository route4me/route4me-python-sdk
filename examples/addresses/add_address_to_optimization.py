"""Add addresses to an existing optimization and re-optimize it.

Calls :meth:`Optimization.get_optimizations <route4me.optimization.Optimization.get_optimizations>` and
:meth:`Optimization.get_optimization <route4me.optimization.Optimization.get_optimization>`
(``GET /api.v4/optimization_problem.php``) to read the latest optimization, then
:meth:`Optimization.update_optimization <route4me.optimization.Optimization.update_optimization>` with
two new addresses and ``reoptimize=1``, which sends ``PUT /api.v4/optimization_problem.php`` with the
problem ID and ``reoptimize`` in the query and the addresses as the JSON body. Prints the addresses
before and after. This changes the latest optimization of the account.

Run it with::

    python examples/addresses/add_address_to_optimization.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Add two addresses to the latest optimization.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    optimization = route4me.optimization
    response = optimization.get_optimizations(limit=1, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        optimizations = response["optimizations"]
        optimization_problem_id = optimizations[0]["optimization_problem_id"]
        response = optimization.get_optimization(optimization_problem_id=optimization_problem_id)
        if isinstance(response, dict) and "errors" in response.keys():
            print(". ".join(response["errors"]))
        else:
            print("Addresses to include")
            for i, address in enumerate(response["addresses"]):
                print(f"Address #{i + 1}")
                print(f"\tAddress: {address['address']}")
                print(f"\tLatitude: {address['lat']}")
                print(f"\tLongitude: {address['lng']}")
                print(f"\tAlias: {address['alias']}")
            addresses = [
                {
                    "address": "555 W 57th St New York, NY 10019",
                    "lat": 40.7718005,
                    "lng": -73.9897716,
                    "alias": "BMW of Manhattan",
                    "time": 300,
                },
                {
                    "address": "57 W 57th St New York, NY 10019",
                    "lat": 40.7558695,
                    "lng": -73.9862019,
                    "alias": "Verizon Wireless",
                    "time": 300,
                },
            ]
            print("Addresses to include")
            for i, address in enumerate(addresses):
                print(f"Address #{i + 1}")
                print(f"\tAddress: {address['address']}")
                print(f"\tLatitude: {address['lat']}")
                print(f"\tLongitude: {address['lng']}")
                print(f"\tAlias: {address['alias']}")
            response = optimization.update_optimization(
                optimization_problem_id=optimization_problem_id, addresses=addresses, reoptimize=1
            )
            if isinstance(response, dict) and "errors" in response.keys():
                print(". ".join(response["errors"]))
            else:
                print("Current Addresses")
                for i, address in enumerate(response["addresses"]):
                    print(f"Address #{i + 1}")
                    print(f"\tAddress: {address['address']}")
                    print(f"\tLatitude: {address['lat']}")
                    print(f"\tLongitude: {address['lng']}")
                    print(f"\tAlias: {address['alias']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add address to Optimization")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
