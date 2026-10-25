"""List the latest ten optimizations.

Calls :meth:`Optimization.get_optimizations <route4me.optimization.Optimization.get_optimizations>` with
``limit=10`` and ``offset=0``, which sends ``GET /api.v4/optimization_problem.php``, and prints the ID
and route name of each optimization.

Run it with::

    python examples/optimizations/get_optimizations.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the latest ten optimizations.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    optimization = route4me.optimization
    response = optimization.get_optimizations(limit=10, offset=0)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        print("Latest 10 Optimizations")
        for i, optimization in enumerate(response["optimizations"]):
            optimization_problem_id = optimization["optimization_problem_id"]
            print(
                f"{i + 1}.-\tOptimization ID: {optimization_problem_id} - \t{optimization['parameters']['route_name']}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Optimizations")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
