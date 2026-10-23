"""Request-level tests for :class:`route4me.vehicle_capacity_profiles.VehicleCapacityProfiles`."""

import json
from urllib.parse import urlsplit

import pytest
import responses

from route4me.api_endpoints import VEHICLE_CAPACITY_PROFILES_V5
from route4me.exceptions import ParamValueException

PROFILE_ID = 7
PROFILE_URL = f"{VEHICLE_CAPACITY_PROFILES_V5}/{PROFILE_ID}"


def path_of(url):
    return urlsplit(url).path


class TestVehicleCapacityProfiles:
    def test_get_vehicle_capacity_profiles_sends_the_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, VEHICLE_CAPACITY_PROFILES_V5, json={"data": [], "total": 0}, status=200)

        result = client.vehicle_capacity_profiles.get_vehicle_capacity_profiles(page=1, per_page=10, merge_pages=False)

        assert result == {"data": [], "total": 0}
        request = last_request()
        assert request.method == "GET"
        assert path_of(request.url) == path_of(VEHICLE_CAPACITY_PROFILES_V5)
        assert query_of(request) == {"page": "1", "per_page": "10", "merge_pages": "0"}
        assert request.body is None

    def test_create_vehicle_capacity_profile_posts_the_keywords(self, client, mocked, last_request, query_of):
        body = {"name": "Test capacity", "max_weight": 1000, "max_weight_unit": "kg", "max_items_number": 40}
        mocked.add(responses.POST, VEHICLE_CAPACITY_PROFILES_V5, json={"data": {"id": PROFILE_ID}}, status=200)

        assert client.vehicle_capacity_profiles.create_vehicle_capacity_profile(**body) == {"data": {"id": PROFILE_ID}}
        request = last_request()
        assert request.method == "POST"
        assert path_of(request.url) == path_of(VEHICLE_CAPACITY_PROFILES_V5)
        assert query_of(request) == {}
        assert json.loads(request.body) == body

    def test_create_vehicle_capacity_profile_requires_a_name(self, client, mocked):
        with pytest.raises(ParamValueException) as excinfo:
            client.vehicle_capacity_profiles.create_vehicle_capacity_profile(max_weight=1000)

        assert excinfo.value.param == "name"
        assert not mocked.calls

    @pytest.mark.parametrize(
        ("method", "http_method"),
        [("get_vehicle_capacity_profile_by_id", "GET"), ("delete_vehicle_capacity_profile", "DELETE")],
    )
    def test_puts_the_profile_id_in_the_path(self, client, mocked, last_request, query_of, method, http_method):
        mocked.add(http_method, PROFILE_URL, json={"data": {"id": PROFILE_ID}}, status=200)

        assert getattr(client.vehicle_capacity_profiles, method)(PROFILE_ID) == {"data": {"id": PROFILE_ID}}
        request = last_request()
        assert request.method == http_method
        assert path_of(request.url) == path_of(PROFILE_URL)
        assert query_of(request) == {}
        assert request.body is None

    def test_update_vehicle_capacity_profile_patches_the_keywords(self, client, mocked, last_request, query_of):
        mocked.add(responses.PATCH, PROFILE_URL, json={"data": {"id": PROFILE_ID}}, status=200)

        client.vehicle_capacity_profiles.update_vehicle_capacity_profile(PROFILE_ID, name="Renamed", max_volume=12.5)

        request = last_request()
        assert request.method == "PATCH"
        assert path_of(request.url) == path_of(PROFILE_URL)
        assert query_of(request) == {}
        assert json.loads(request.body) == {"name": "Renamed", "max_volume": 12.5}

    def test_an_id_cannot_escape_its_path_segment(self, client, monkeypatch):
        urls = []

        def capture(url, params, request_method, **kwargs):
            urls.append(url)
            raise RuntimeError("stop before sending")

        monkeypatch.setattr(client, "_make_request", capture)

        with pytest.raises(RuntimeError):
            client.vehicle_capacity_profiles.delete_vehicle_capacity_profile("a/b")

        assert urls == [f"{VEHICLE_CAPACITY_PROFILES_V5}/a%2Fb"]

    @pytest.mark.parametrize(
        "method",
        [
            "get_vehicle_capacity_profile_by_id",
            "update_vehicle_capacity_profile",
            "delete_vehicle_capacity_profile",
        ],
    )
    def test_an_empty_id_is_rejected_before_any_request(self, client, mocked, method):
        with pytest.raises(ParamValueException):
            getattr(client.vehicle_capacity_profiles, method)(None)

        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.POST,
            VEHICLE_CAPACITY_PROFILES_V5,
            json={"status": False, "code": 406, "messages": {"name": ["The name is required."]}},
            status=406,
        )

        assert client.vehicle_capacity_profiles.create_vehicle_capacity_profile(name="") == {
            "errors": ["The name is required."]
        }
