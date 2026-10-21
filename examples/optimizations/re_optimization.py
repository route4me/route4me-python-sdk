"""Re-optimize the latest optimization.

Calls :meth:`Optimization.get_optimizations <route4me.optimization.Optimization.get_optimizations>` with
``limit=1`` (``GET /api.v4/optimization_problem.php``) to find the latest optimization, then
:meth:`Route4Me.re_optimization <route4me.api.Route4Me.re_optimization>` with its ID, which sends
``PUT /api.v4/optimization_problem.php`` with ``reoptimize=1``, and prints the new state (an
``OPTIMIZATION_STATE`` name). This re-optimizes an optimization of the account.

Run it with::

    python examples/optimizations/re_optimization.py --api_key <your key>
"""

import argparse

from route4me import Route4Me
from route4me.constants import OPTIMIZATION_STATE


def main(api_key):
    """Re-optimize the latest optimization and print its state.

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
        print(f"Re-optimization problem id: {optimization_problem_id}")
        response = route4me.re_optimization(optimization_problem_id)
        print(f"Re-optimization status: {OPTIMIZATION_STATE.reverse_mapping.get(response['state'])}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Re-Optimization")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
