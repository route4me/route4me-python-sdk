"""Tests for the optimization methods on the ``Route4Me`` client itself.

``run_optimization``, ``re_optimization``, ``get_optimization``,
``parse_response`` and the two JSON exporters are the SDK's headline API --
they are what every ``examples/`` script calls -- and none of them had any
coverage.
"""

import json

import pytest
import responses

from route4me import Route4Me
from route4me.api_endpoints import API_HOST
from route4me.constants import ALGORITHM_TYPE
from route4me.exceptions import APIException

OPTIMIZATION_ID = "07372F2CF3814EC6E2E4C4B0DCF20B9C"

OPTIMIZATION_RESPONSE = {
    "optimization_problem_id": OPTIMIZATION_ID,
    "state": 4,
    "addresses": [
        {"route_destination_id": 501, "alias": "Bergdorf Goodman", "sequence_no": 0},
        {"route_destination_id": 502, "alias": "Giorgio Armani", "sequence_no": 1},
    ],
}


@pytest.fixture
def prepared(client):
    """A client with a minimal but valid optimization staged."""
    client.optimization.add(
        data={
            "algorithm_type": ALGORITHM_TYPE.TSP,
            "route_name": "Single Driver Round Trip",
            "route_time": 0,
        }
    )
    client.address.add_address(
        address="754 5th Ave New York, NY 10019",
        lat=40.7636197,
        lng=-73.9744388,
        alias="Bergdorf Goodman",
        is_depot=1,
        time=0,
    )
    return client


class TestRunOptimization:
    def test_posts_to_the_optimization_host_and_returns_json(self, prepared, mocked, last_request):
        mocked.add(responses.POST, API_HOST, json=OPTIMIZATION_RESPONSE, status=200)

        result = prepared.run_optimization()

        assert result["optimization_problem_id"] == OPTIMIZATION_ID
        assert last_request().method == "POST"

    def test_sends_the_staged_optimization_as_the_body(self, prepared, mocked, last_request):
        mocked.add(responses.POST, API_HOST, json=OPTIMIZATION_RESPONSE, status=200)

        prepared.run_optimization()

        body = json.loads(last_request().body)
        assert body["parameters"]["route_name"] == "Single Driver Round Trip"
        assert len(body["addresses"]) == 1

    def test_the_response_is_retained_on_the_client(self, prepared, mocked):
        mocked.add(responses.POST, API_HOST, json=OPTIMIZATION_RESPONSE, status=200)

        prepared.run_optimization()

        assert prepared.response is not None
        assert prepared.response.status_code == 200

    def test_redirects_disabled_adds_the_redirect_flag(self, mocked, query_of, last_request):
        """``redirects=False`` is surfaced to the API as ``redirect=0``."""
        client = Route4Me("1" * 32, redirects=False)
        mocked.add(responses.POST, API_HOST, json=OPTIMIZATION_RESPONSE, status=200)

        client.run_optimization()

        assert query_of(last_request())["redirect"] == "0"

    def test_an_http_error_propagates(self, prepared, mocked):
        """``run_optimization`` does not catch -- unlike resource methods, it
        raises. Pinning this because it is an inconsistency callers rely on."""
        mocked.add(responses.POST, API_HOST, json={"errors": ["bad"]}, status=400)

        with pytest.raises(APIException):
            prepared.run_optimization()


class TestGetOptimization:
    ADDRESSLESS = {"optimization_problem_id": OPTIMIZATION_ID, "state": 4}

    def test_sends_the_optimization_problem_id(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, API_HOST, json=self.ADDRESSLESS, status=200)

        client.get_optimization(OPTIMIZATION_ID)

        assert query_of(last_request())["optimization_problem_id"] == OPTIMIZATION_ID

    def test_uses_a_get(self, client, mocked, last_request):
        mocked.add(responses.GET, API_HOST, json=self.ADDRESSLESS, status=200)

        client.get_optimization(OPTIMIZATION_ID)

        assert last_request().method == "GET"

    def test_works_with_a_realistic_payload(self, client, mocked):
        """Regression: this raised TypeError for any payload containing
        "addresses" -- i.e. every real optimization response -- because
        `parse_response` subscripted the Response object."""
        mocked.add(responses.GET, API_HOST, json=OPTIMIZATION_RESPONSE, status=200)

        result = client.get_optimization(OPTIMIZATION_ID)

        assert result["optimization_problem_id"] == OPTIMIZATION_ID
        assert len(client.address.addresses) == 2

    def test_it_returns_the_payload(self, client, mocked):
        """Regression: previously returned None unconditionally."""
        mocked.add(responses.GET, API_HOST, json=self.ADDRESSLESS, status=200)

        assert client.get_optimization(OPTIMIZATION_ID) == self.ADDRESSLESS


class TestParseResponse:
    def test_a_payload_without_addresses_is_a_no_op(self, client, mocked):
        mocked.add(responses.GET, API_HOST, json={"state": 1}, status=200)
        client.response = client._make_request(API_HOST, {}, client._request_get)

        client.parse_response()  # must not raise

    def test_addresses_are_copied_onto_the_address_resource(self, client, mocked):
        mocked.add(responses.GET, API_HOST, json=OPTIMIZATION_RESPONSE, status=200)
        client.response = client._make_request(API_HOST, {}, client._request_get)

        client.parse_response()

        assert client.address.addresses == OPTIMIZATION_RESPONSE["addresses"]


class TestReOptimization:
    def test_sets_the_reoptimize_flag_and_problem_id(self, client, mocked, query_of, last_request):
        mocked.add(responses.PUT, API_HOST, json=OPTIMIZATION_RESPONSE, status=200)

        client.re_optimization(OPTIMIZATION_ID)

        query = query_of(last_request())
        assert query["optimization_problem_id"] == OPTIMIZATION_ID
        assert query["reoptimize"] == "1"

    def test_wraps_the_supplied_data_under_parameters(self, client, mocked, last_request):
        mocked.add(responses.PUT, API_HOST, json=OPTIMIZATION_RESPONSE, status=200)

        client.re_optimization(OPTIMIZATION_ID, data={"route_name": "Renamed"})

        assert json.loads(last_request().body) == {"parameters": {"route_name": "Renamed"}}

    def test_an_http_error_propagates(self, client, mocked):
        mocked.add(responses.PUT, API_HOST, json={"errors": ["bad"]}, status=400)

        with pytest.raises(APIException):
            client.re_optimization(OPTIMIZATION_ID)


class TestExporters:
    def test_export_request_writes_the_staged_optimization(self, prepared, tmp_path):
        target = tmp_path / "request.json"

        prepared.export_request_to_json(str(target))

        written = json.loads(target.read_text())
        assert written["parameters"]["route_name"] == "Single Driver Round Trip"
        assert len(written["addresses"]) == 1

    def test_export_result_writes_nothing_when_there_is_no_response(self, client, tmp_path):
        target = tmp_path / "result.json"

        client.export_result_to_json(str(target))

        assert not target.exists()

    @pytest.mark.parametrize("exporter", ["export_result_to_json", "export_request_to_json"])
    def test_exports_are_written_as_utf8(self, prepared, mocked, tmp_path, monkeypatch, exporter):
        """#37: without an explicit encoding, non-ASCII addresses fail on Windows."""
        mocked.add(responses.POST, API_HOST, json=OPTIMIZATION_RESPONSE, status=200)
        prepared.run_optimization()
        encodings = []
        real_open = open

        def spy(file, *args, **kwargs):
            encodings.append(kwargs.get("encoding"))
            return real_open(file, *args, **kwargs)

        monkeypatch.setattr("route4me.api.open", spy, raising=False)

        getattr(prepared, exporter)(str(tmp_path / "out.json"))

        assert encodings == ["utf-8"]

    def test_export_result_writes_after_a_call(self, prepared, mocked, tmp_path):
        mocked.add(responses.POST, API_HOST, json=OPTIMIZATION_RESPONSE, status=200)
        prepared.run_optimization()
        target = tmp_path / "result.json"

        prepared.export_result_to_json(str(target))

        assert target.exists()
        assert json.loads(target.read_text())["optimization_problem_id"] == OPTIMIZATION_ID
