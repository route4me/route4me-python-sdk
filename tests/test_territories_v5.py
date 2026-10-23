"""Request-level tests for :class:`route4me.territories_v5.TerritoriesV5`."""

import json

import pytest
import responses

from route4me.api_endpoints import (
    AUTOMATIC_TERRITORIES_JOB_RESULT_V5,
    AUTOMATIC_TERRITORIES_JOB_STATUS_V5,
    AUTOMATIC_TERRITORIES_V5,
)
from route4me.exceptions import ParamValueException

JOB_ID = "JOB-1"
ADDRESSES = [{"id": 1, "lat": 40.7, "lng": -73.9}, {"id": 2, "lat": 40.8, "lng": -74.0}]


class TestAutomaticTerritories:
    def test_create_job_posts_the_addresses_and_returns_the_job_headers(self, client, mocked, last_request, query_of):
        mocked.add(
            responses.POST,
            AUTOMATIC_TERRITORIES_V5,
            json=[],
            status=202,
            headers={"X-job-id": JOB_ID, "Location": f"{AUTOMATIC_TERRITORIES_JOB_STATUS_V5}/{JOB_ID}"},
        )

        result = client.territories_v5.create_automatic_territories_job(addresses=ADDRESSES, mode=0, params=[])

        assert result == {
            "job_id": JOB_ID,
            "location": f"{AUTOMATIC_TERRITORIES_JOB_STATUS_V5}/{JOB_ID}",
            "data": [],
        }
        assert last_request().method == "POST"
        assert query_of(last_request()) == {}
        assert json.loads(last_request().body) == {"addresses": ADDRESSES, "mode": 0, "params": []}

    def test_create_job_accepts_a_temporary_storage_id(self, client, mocked, last_request):
        mocked.add(responses.POST, AUTOMATIC_TERRITORIES_V5, body=b"", status=202, headers={"X-job-id": JOB_ID})

        result = client.territories_v5.create_automatic_territories_job(temporary_addresses_storage_id="STORAGE-1")

        assert result == {"job_id": JOB_ID, "location": None, "data": b""}
        assert json.loads(last_request().body) == {"temporary_addresses_storage_id": "STORAGE-1"}

    def test_create_job_needs_addresses_or_a_storage_id(self, client, mocked):
        with pytest.raises(ParamValueException) as excinfo:
            client.territories_v5.create_automatic_territories_job(mode=0)

        assert "addresses" in str(excinfo.value)
        assert not mocked.calls

    def test_create_job_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.POST, AUTOMATIC_TERRITORIES_V5, json={"errors": ["Bad addresses"]}, status=406)

        assert client.territories_v5.create_automatic_territories_job(addresses=[]) == {"errors": ["Bad addresses"]}

    def test_get_job_status(self, client, mocked, last_request, query_of):
        mocked.add(
            responses.GET, f"{AUTOMATIC_TERRITORIES_JOB_STATUS_V5}/{JOB_ID}", json={"status": "processing"}, status=200
        )

        assert client.territories_v5.get_automatic_territories_job_status(JOB_ID) == {"status": "processing"}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {}

    def test_get_job_result(self, client, mocked, last_request):
        result = {"job_id": JOB_ID, "clusters": [{"cluster_id": "1", "addresses_count": 2}]}
        mocked.add(responses.GET, f"{AUTOMATIC_TERRITORIES_JOB_RESULT_V5}/{JOB_ID}", json=result, status=200)

        assert client.territories_v5.get_automatic_territories_job_result(JOB_ID) == result
        assert last_request().method == "GET"

    def test_a_job_id_with_a_slash_is_encoded(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{AUTOMATIC_TERRITORIES_JOB_STATUS_V5}/a%2Fb", json={}, status=200)

        client.territories_v5.get_automatic_territories_job_status("a/b")

        assert last_request().path_url == "/modules/api/v5.0/automatic-territories/job-tracker/status/a%2Fb"

    @pytest.mark.parametrize("method", ["get_automatic_territories_job_status", "get_automatic_territories_job_result"])
    def test_an_empty_job_id_is_rejected_before_any_request(self, client, mocked, method):
        with pytest.raises(ParamValueException):
            getattr(client.territories_v5, method)("")

        assert not mocked.calls

    def test_a_job_in_progress_is_returned_as_an_error_dict(self, client, mocked):
        mocked.add(
            responses.GET,
            f"{AUTOMATIC_TERRITORIES_JOB_RESULT_V5}/{JOB_ID}",
            json={"errors": ["Job is in progress"]},
            status=409,
        )

        assert client.territories_v5.get_automatic_territories_job_result(JOB_ID) == {"errors": ["Job is in progress"]}
