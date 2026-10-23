"""Replace the depots of a hybrid optimization.

Calls :meth:`Optimization.add_depots_to_hybrid_optimization
<route4me.optimization.Optimization.add_depots_to_hybrid_optimization>`, which sends
``POST /api/change_hybrid_optimization_depot.php`` with the optimization ID, ``delete_old_depots`` and
``new_depots`` as the JSON body. Prints the reply.

Run it with::

    python examples/optimizations/add_depots_to_hybrid_optimization.py --api_key <your key> \\
        --optimization_problem_id <optimization_problem_id>
"""

import argparse

from route4me import Route4Me


def main(api_key, optimization_problem_id):
    """Replace the depots and print the reply.

    :param api_key: Route4Me API key.
    :param optimization_problem_id: ID of the hybrid optimization.
    """
    route4me = Route4Me(api_key)

    depot = {
        "address": "Example Depot, 1604 Parkridge Pkwy, Louisville, KY 40214",
        "lat": 38.141598,
        "lng": -85.793846,
        "is_depot": True,
    }
    response = route4me.optimization.add_depots_to_hybrid_optimization(
        optimization_problem_id=optimization_problem_id,
        delete_old_depots=True,
        new_depots=[depot],
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add Depots to Hybrid Optimization")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--optimization_problem_id",
        dest="optimization_problem_id",
        help="ID of the hybrid optimization",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.optimization_problem_id)
