"""Request-level tests for :class:`route4me.vehicles_v5.VehiclesV5`."""

import json
from urllib.parse import urlsplit

import pytest
import responses

from route4me.api_endpoints import (
    VEHICLES_ASSIGN_V5,
    VEHICLES_BULK_ACTIVATE_V5,
    VEHICLES_BULK_DEACTIVATE_V5,
    VEHICLES_BULK_DELETE_V5,
    VEHICLES_BULK_RESTORE_V5,
    VEHICLES_BULK_UPDATE_V5,
    VEHICLES_EXECUTE_V5,
    VEHICLES_JOB_RESULT_V5,
    VEHICLES_JOB_STATUS_V5,
    VEHICLES_LICENSE_V5,
    VEHICLES_PAGINATE_V5,
    VEHICLES_SEARCH_V5,
    VEHICLES_SYNC_PENDING_V5,
    VEHICLES_V5,
)
from route4me.exceptions import ParamValueException

VEHICLE_ID = "VEHICLE-1"
JOB_ID = "JOB-1"
V5_ERROR = {"status": False, "code": 406, "messages": {"vehicle_alias": ["The vehicle alias is required."]}}


def path_of(url):
    return urlsplit(url).path


class TestQueries:
    @pytest.mark.parametrize(
        ("method", "url", "kwargs", "expected"),
        [
            ("get_vehicles", VEHICLES_V5, {}, {}),
            (
                "get_vehicles",
                VEHICLES_V5,
                {"show": "all", "is_operational": True, "only_with_profile": False},
                {"show": "all", "is_operational": "1", "only_with_profile": "0"},
            ),
            (
                "get_paginated_vehicles_list",
                VEHICLES_PAGINATE_V5,
                {"page": 2, "per_page": 10, "search_query": "van"},
                {"page": "2", "per_page": "10", "search_query": "van"},
            ),
            (
                "get_vehicle_by_license_plate",
                VEHICLES_LICENSE_V5,
                {"vehicle_license_plate": "TEST123"},
                {"vehicle_license_plate": "TEST123"},
            ),
        ],
    )
    def test_sends_the_keywords_as_the_query(
        self, client, mocked, last_request, query_of, method, url, kwargs, expected
    ):
        mocked.add(responses.GET, url, json=[{"vehicle_id": VEHICLE_ID}], status=200)

        result = getattr(client.vehicles_v5, method)(**kwargs)

        assert result == [{"vehicle_id": VEHICLE_ID}]
        request = last_request()
        assert request.method == "GET"
        assert path_of(request.url) == path_of(url)
        assert query_of(request) == expected
        assert request.body is None

    def test_list_values_are_sent_with_bracketed_keys(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, VEHICLES_V5, json=[], status=200)

        client.vehicles_v5.get_vehicles(facility_ids=["FACILITY-1", "FACILITY-2"])

        assert query_of(last_request()) == {"facility_ids[]": ["FACILITY-1", "FACILITY-2"]}

    def test_no_query_value_is_kept_between_calls(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, VEHICLES_V5, json=[], status=200)

        client.vehicles_v5.get_vehicles(show="deleted")
        client.vehicles_v5.get_vehicles()

        assert query_of(last_request()) == {}


class TestPathIds:
    @pytest.mark.parametrize(
        ("method", "http_method", "url"),
        [
            ("get_vehicle_by_id", "GET", f"{VEHICLES_V5}/{VEHICLE_ID}"),
            ("delete_vehicle", "DELETE", f"{VEHICLES_V5}/{VEHICLE_ID}"),
            ("get_vehicle_track", "GET", f"{VEHICLES_V5}/{VEHICLE_ID}/track"),
        ],
    )
    def test_puts_the_vehicle_id_in_the_path(self, client, mocked, last_request, query_of, method, http_method, url):
        mocked.add(http_method, url, json={"vehicle_id": VEHICLE_ID}, status=200)

        assert getattr(client.vehicles_v5, method)(VEHICLE_ID) == {"vehicle_id": VEHICLE_ID}
        request = last_request()
        assert request.method == http_method
        assert path_of(request.url) == path_of(url)
        assert query_of(request) == {}
        assert request.body is None

    def test_update_vehicle_patches_the_given_fields(self, client, mocked, last_request, query_of):
        mocked.add(responses.PATCH, f"{VEHICLES_V5}/{VEHICLE_ID}", json={"vehicle_id": VEHICLE_ID}, status=200)

        result = client.vehicles_v5.update_vehicle(VEHICLE_ID, vehicle_alias="Van 2")

        assert result == {"vehicle_id": VEHICLE_ID}
        request = last_request()
        assert request.method == "PATCH"
        assert path_of(request.url) == path_of(f"{VEHICLES_V5}/{VEHICLE_ID}")
        assert query_of(request) == {}
        assert json.loads(request.body) == {"vehicle_alias": "Van 2"}

    def test_update_vehicle_needs_a_field(self, client, mocked):
        with pytest.raises(ParamValueException):
            client.vehicles_v5.update_vehicle(VEHICLE_ID)

        assert not mocked.calls

    def test_get_vehicle_track_sends_the_period_as_the_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, f"{VEHICLES_V5}/{VEHICLE_ID}/track", json={"data": []}, status=200)

        client.vehicles_v5.get_vehicle_track(VEHICLE_ID, start="2026-10-01", end="2026-10-02")

        assert query_of(last_request()) == {"start": "2026-10-01", "end": "2026-10-02"}

    @pytest.mark.parametrize(
        ("method", "url"),
        [
            ("get_vehicle_job_status", f"{VEHICLES_JOB_STATUS_V5}/{JOB_ID}"),
            ("get_vehicle_job_result", f"{VEHICLES_JOB_RESULT_V5}/{JOB_ID}"),
        ],
    )
    def test_puts_the_job_id_in_the_path(self, client, mocked, last_request, method, url):
        mocked.add(responses.GET, url, json={"status": "processing"}, status=200)

        assert getattr(client.vehicles_v5, method)(JOB_ID) == {"status": "processing"}
        request = last_request()
        assert request.method == "GET"
        assert path_of(request.url) == path_of(url)

    def test_a_finished_job_status_follows_the_redirect_to_the_result(self, client, mocked):
        result_url = f"{VEHICLES_JOB_RESULT_V5}/{JOB_ID}"
        mocked.add(
            responses.GET,
            f"{VEHICLES_JOB_STATUS_V5}/{JOB_ID}",
            json={"status": "processed"},
            status=303,
            headers={"Location": result_url},
        )
        mocked.add(responses.GET, result_url, json={"status": True}, status=200)

        assert client.vehicles_v5.get_vehicle_job_status(JOB_ID) == {"status": True}
        assert [path_of(call.request.url) for call in mocked.calls] == [
            path_of(f"{VEHICLES_JOB_STATUS_V5}/{JOB_ID}"),
            path_of(result_url),
        ]

    def test_an_id_cannot_escape_its_path_segment(self, client, monkeypatch):
        urls = []

        def capture(url, params, request_method, **kwargs):
            urls.append(url)
            raise RuntimeError("stop before sending")

        monkeypatch.setattr(client, "_make_request", capture)

        for method in ("get_vehicle_by_id", "delete_vehicle", "get_vehicle_job_status"):
            with pytest.raises(RuntimeError):
                getattr(client.vehicles_v5, method)("a/b")

        assert urls == [
            f"{VEHICLES_V5}/a%2Fb",
            f"{VEHICLES_V5}/a%2Fb",
            f"{VEHICLES_JOB_STATUS_V5}/a%2Fb",
        ]

    @pytest.mark.parametrize(
        "method",
        [
            "get_vehicle_by_id",
            "delete_vehicle",
            "update_vehicle",
            "get_vehicle_track",
            "get_vehicle_job_status",
            "get_vehicle_job_result",
        ],
    )
    @pytest.mark.parametrize("empty", ["", None])
    def test_an_empty_id_is_rejected_before_any_request(self, client, mocked, method, empty):
        with pytest.raises(ParamValueException):
            getattr(client.vehicles_v5, method)(empty)

        assert not mocked.calls


class TestBodies:
    @pytest.mark.parametrize(
        ("method", "url", "body"),
        [
            (
                "create_vehicle",
                VEHICLES_V5,
                {"vehicle_alias": "Test van", "vehicle_license_plate": "TEST123", "vehicle_type_id": "van"},
            ),
            (
                "create_temporary_vehicle",
                VEHICLES_ASSIGN_V5,
                {"vehicle_id": VEHICLE_ID, "assigned_member_id": 1, "expires_at": 1792600000, "force-assignment": True},
            ),
            ("execute_vehicle_order", VEHICLES_EXECUTE_V5, {"vehicle_id": VEHICLE_ID, "lat": 40.7, "lng": -73.9}),
            ("search_vehicles", VEHICLES_SEARCH_V5, {"vehicle_ids": [VEHICLE_ID], "lat": 40.7, "lng": -73.9}),
            (
                "sync_pending_telematics_data",
                VEHICLES_SYNC_PENDING_V5,
                {
                    "vehicle_alias": "Test van",
                    "r4m_telematics_gateway_connection_id": 1,
                    "r4m_telematics_gateway_vehicle_id": 2,
                },
            ),
        ],
    )
    def test_sends_the_keywords_as_the_json_body(self, client, mocked, last_request, query_of, method, url, body):
        mocked.add(responses.POST, url, json={"vehicle_id": VEHICLE_ID}, status=200)

        assert getattr(client.vehicles_v5, method)(**body) == {"vehicle_id": VEHICLE_ID}
        request = last_request()
        assert request.method == "POST"
        assert path_of(request.url) == path_of(url)
        assert query_of(request) == {}
        assert request.headers["Content-Type"] == "application/json"
        assert json.loads(request.body) == body

    @pytest.mark.parametrize(
        ("method", "kwargs", "missing"),
        [
            ("create_vehicle", {"vehicle_make": "Ford"}, "vehicle_alias"),
            ("create_temporary_vehicle", {"vehicle_id": VEHICLE_ID}, "assigned_member_id, expires_at"),
            ("execute_vehicle_order", {"lat": 40.7}, "vehicle_id, lng"),
            ("search_vehicles", {}, "vehicle_ids, lat, lng"),
            ("get_vehicle_by_license_plate", {}, "vehicle_license_plate"),
            ("activate_vehicles", {}, "vehicle_ids"),
            ("deactivate_vehicles", {}, "vehicle_ids"),
            ("delete_vehicles", {}, "vehicle_ids"),
            ("restore_vehicles", {}, "vehicle_ids"),
            ("update_vehicles", {}, "vehicles"),
        ],
    )
    def test_a_missing_required_field_is_named_before_any_request(self, client, mocked, method, kwargs, missing):
        with pytest.raises(ParamValueException) as excinfo:
            getattr(client.vehicles_v5, method)(**kwargs)

        assert excinfo.value.param == missing
        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.POST, VEHICLES_V5, json=V5_ERROR, status=406)

        assert client.vehicles_v5.create_vehicle(vehicle_alias="") == {"errors": ["The vehicle alias is required."]}


BULK = [
    ("activate_vehicles", VEHICLES_BULK_ACTIVATE_V5, {"vehicle_ids": [VEHICLE_ID, "VEHICLE-2"]}),
    ("deactivate_vehicles", VEHICLES_BULK_DEACTIVATE_V5, {"vehicle_ids": [VEHICLE_ID]}),
    ("delete_vehicles", VEHICLES_BULK_DELETE_V5, {"vehicle_ids": [VEHICLE_ID]}),
    ("restore_vehicles", VEHICLES_BULK_RESTORE_V5, {"vehicle_ids": [VEHICLE_ID]}),
    ("update_vehicles", VEHICLES_BULK_UPDATE_V5, {"vehicles": [{"vehicle_id": VEHICLE_ID, "vehicle_alias": "Van"}]}),
]


class TestBulkJobs:
    @pytest.mark.parametrize(("method", "url", "body"), BULK)
    def test_starts_a_job_and_returns_its_id(self, client, mocked, last_request, query_of, method, url, body):
        location = f"{VEHICLES_JOB_STATUS_V5}/{JOB_ID}"
        mocked.add(responses.POST, url, body=b"", status=202, headers={"X-Job-Id": JOB_ID, "Location": location})

        assert getattr(client.vehicles_v5, method)(**body) == {"job_id": JOB_ID, "location": location}
        request = last_request()
        assert request.method == "POST"
        assert path_of(request.url) == path_of(url)
        assert query_of(request) == {}
        assert json.loads(request.body) == body

    def test_the_job_id_falls_back_to_the_location_header(self, client, mocked):
        location = f"{VEHICLES_JOB_STATUS_V5}/{JOB_ID}"
        mocked.add(responses.POST, VEHICLES_BULK_DELETE_V5, body=b"", status=202, headers={"Location": location})

        assert client.vehicles_v5.delete_vehicles(vehicle_ids=[VEHICLE_ID]) == {"job_id": JOB_ID, "location": location}

    def test_a_reply_without_job_headers_gives_none(self, client, mocked):
        mocked.add(responses.POST, VEHICLES_BULK_RESTORE_V5, body=b"", status=202)

        assert client.vehicles_v5.restore_vehicles(vehicle_ids=[VEHICLE_ID]) == {"job_id": None, "location": None}

    def test_a_json_reply_is_returned_as_is(self, client, mocked):
        mocked.add(responses.POST, VEHICLES_BULK_ACTIVATE_V5, json={"status": True}, status=200)

        assert client.vehicles_v5.activate_vehicles(vehicle_ids=[VEHICLE_ID]) == {"status": True}

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.POST, VEHICLES_BULK_UPDATE_V5, json=V5_ERROR, status=406)

        result = client.vehicles_v5.update_vehicles(vehicles=[{"vehicle_id": VEHICLE_ID}])

        assert result == {"errors": ["The vehicle alias is required."]}
