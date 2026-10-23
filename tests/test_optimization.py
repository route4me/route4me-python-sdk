"""Request-level tests for the :class:`route4me.optimization.Optimization` methods added in 1.0.0.

Covers the hybrid optimization, its depots and the optimization time
prediction. Each test pins the HTTP method, URL, query and JSON body.
"""

import json

import responses

from route4me.api_endpoints import HYBRID_OPTIMIZATION, HYBRID_OPTIMIZATION_DEPOTS, OPTIMIZATION_TIME_PREDICTION

OPTIMIZATION_ID = "OPTIMIZATION-1"
DEPOT = {"address": "1604 Parkridge Pkwy, Louisville, KY 40214", "lat": 38.141598, "lng": -85.793846, "is_depot": True}


def body_of(request):
    """Decode a JSON request body."""
    return json.loads(request.body)


class TestHybridOptimization:
    def test_get_hybrid_optimization_sends_the_date_in_the_query(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.GET, HYBRID_OPTIMIZATION, json={"optimization_problem_id": OPTIMIZATION_ID}, status=200)

        result = client.optimization.get_hybrid_optimization(
            target_date_string="2026-11-02", timezone_offset_minutes=-300
        )

        assert result == {"optimization_problem_id": OPTIMIZATION_ID}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {
            "api_key": api_key,
            "target_date_string": "2026-11-02",
            "timezone_offset_minutes": "-300",
        }

    def test_add_depots_to_hybrid_optimization_posts_the_depots(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.POST, HYBRID_OPTIMIZATION_DEPOTS, json={"status": True}, status=200)
        body = {"optimization_problem_id": OPTIMIZATION_ID, "delete_old_depots": True, "new_depots": [DEPOT]}

        assert client.optimization.add_depots_to_hybrid_optimization(**body) == {"status": True}
        assert last_request().method == "POST"
        assert query_of(last_request()) == {"api_key": api_key}
        assert body_of(last_request()) == body

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.GET, HYBRID_OPTIMIZATION, json={"errors": ["No optimization"]}, status=404)

        assert client.optimization.get_hybrid_optimization(target_date_string="2026-11-02") == {
            "errors": ["No optimization"]
        }


class TestOptimizationPrediction:
    def test_posts_the_parameters_and_addresses(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.POST, OPTIMIZATION_TIME_PREDICTION, json={"time-prediction": []}, status=200)
        body = {"parameters": {"algorithm_type": 3, "rt": True}, "addresses": [DEPOT]}

        assert client.optimization.get_optimization_prediction(**body) == {"time-prediction": []}
        assert last_request().method == "POST"
        assert query_of(last_request()) == {"api_key": api_key}
        assert body_of(last_request()) == body
        assert api_key not in last_request().body.decode()
