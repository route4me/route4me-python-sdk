"""Get an optimization by ID.

Calls :meth:`Optimization.get_optimizations <route4me.optimization.Optimization.get_optimizations>` with
``limit=1`` (``GET /api.v4/optimization_problem.php``) to find the latest optimization, then
:meth:`Optimization.get_optimization <route4me.optimization.Optimization.get_optimization>` with its
``optimization_problem_id``, which sends the same request with the ID in the query. Prints the
optimization link and the addresses of each route.

Run it with::

    python examples/optimizations/get_optimization.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the latest optimization.

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
            optimization_problem_id = response["optimization_problem_id"]
            print(f"\tOptimization ID: {optimization_problem_id}")
            print(f"Optimization Link: {response['links']['view']}")
            for i, route in enumerate(response["routes"]):
                print(f"\t{i + 1}\tRoute Link: {route['links']['route']}")
                for address in route["addresses"]:
                    print(f"\t\t\tAddress: {address['address']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Optimization")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
