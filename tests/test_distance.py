"""Request-level tests for :class:`route4me.distance.Distance`."""

import responses

from route4me.api_endpoints import DISTANCE


class TestDistance:
    def test_calculate_distance_sends_the_keywords_as_the_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, DISTANCE, json={"distance": 1.5}, status=200)

        # The parameter names are undocumented; any keyword goes through as given.
        result = client.distance.calculate_distance(param_a="1 Example Way", param_b="2 Example Way")

        assert result == {"distance": 1.5}
        assert last_request().method == "GET"
        assert last_request().url.split("?")[0] == DISTANCE
        assert query_of(last_request()) == {
            "api_key": client.key,
            "param_a": "1 Example Way",
            "param_b": "2 Example Way",
        }

    def test_a_plain_text_reply_is_returned_raw(self, client, mocked):
        mocked.add(responses.GET, DISTANCE, body=b"Missing or invalid start and end address.", status=200)

        assert client.distance.calculate_distance() == b"Missing or invalid start and end address."

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked, load_fixture):
        mocked.add(responses.GET, DISTANCE, json=load_fixture("error_v4"), status=401)

        assert client.distance.calculate_distance() == {"errors": ["The API key is invalid."]}
