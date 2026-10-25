"""Get the hybrid optimization of a date.

Calls :meth:`Optimization.get_hybrid_optimization
<route4me.optimization.Optimization.get_hybrid_optimization>`, which sends
``GET /api.v4/hybrid_date_optimization.php`` with ``target_date_string`` and ``timezone_offset_minutes`` in
the query. Prints the reply.

Run it with::

    python examples/optimizations/get_hybrid_optimization.py --api_key <your key> \\
        --target_date_string <target_date_string>
"""

import argparse

from route4me import Route4Me


def main(api_key, target_date_string):
    """Print the hybrid optimization of ``target_date_string``.

    :param api_key: Route4Me API key.
    :param target_date_string: The date, as YYYY-MM-DD.
    """
    route4me = Route4Me(api_key)

    response = route4me.optimization.get_hybrid_optimization(
        target_date_string=target_date_string,
        timezone_offset_minutes=0,
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Hybrid Optimization")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--target_date_string", dest="target_date_string", help="The date, as YYYY-MM-DD", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.target_date_string)
