"""Predict how long an optimization will take.

Calls :meth:`Optimization.get_optimization_prediction
<route4me.optimization.Optimization.get_optimization_prediction>`, which sends
``POST /api.v4/predict-optimization-time.php`` with the route parameters and three addresses as the JSON body.
Prints the reply.

Run it with::

    python examples/optimizations/get_optimization_prediction.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the time prediction.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    addresses = [
        {"address": "1604 Parkridge Pkwy, Louisville, KY 40214", "lat": 38.141598, "lng": -85.793846, "is_depot": True},
        {"address": "1407 McCoy, Louisville, KY 40215", "lat": 38.202496, "lng": -85.786514, "time": 300},
        {"address": "730 Cecil Avenue, Louisville, KY 40211", "lat": 38.248684, "lng": -85.821121, "time": 300},
    ]
    parameters = {"algorithm_type": 3, "route_name": "Example prediction", "rt": True, "parts": 2}
    response = route4me.optimization.get_optimization_prediction(parameters=parameters, addresses=addresses)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Optimization Prediction")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
