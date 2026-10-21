"""Request-level tests for the API V5 resources.

Covers :class:`route4me.route_status.RouteStatus`,
:class:`route4me.orders_group.OrdersGroup` and
:class:`route4me.optimization_profiles.OptimizationProfiles`.
"""

import json

import pytest
import requests
import responses

from route4me.api_endpoints import ASSIGN_PROFILES_V5, OPTIMIZATION_PROFILES_V5, ORDERS_GROUP_V5, ROUTE_STATUS_V5
from route4me.exceptions import ParamValueException

ROUTE_ID = "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"


class TestRouteStatus:
    @pytest.mark.parametrize(
        ("method", "suffix"),
        [
            ("get_route_status", ""),
            ("get_route_status_history", "/history"),
            ("rollback_route_status", "/rollback"),
        ],
    )
    def test_gets_put_the_route_id_in_the_path(self, client, mocked, last_request, method, suffix):
        mocked.add(responses.GET, f"{ROUTE_STATUS_V5}/{ROUTE_ID}{suffix}", json={"status": "started"}, status=200)

        assert getattr(client.route_status, method)(ROUTE_ID) == {"status": "started"}
        assert last_request().method == "GET"

    def test_set_route_status_posts_the_event(self, client, mocked, last_request):
        mocked.add(responses.POST, f"{ROUTE_STATUS_V5}/{ROUTE_ID}", json={"status": True}, status=200)

        client.route_status.set_route_status(ROUTE_ID, "started", 40.7, -73.9, event_timestamp=1792600000)

        assert json.loads(last_request().body) == {
            "status": "started",
            "lat": 40.7,
            "lng": -73.9,
            "event_timestamp": 1792600000,
        }

    def test_set_route_status_defaults_the_timestamp_to_now(self, client, mocked, last_request):
        mocked.add(responses.POST, f"{ROUTE_STATUS_V5}/{ROUTE_ID}", json={"status": True}, status=200)

        client.route_status.set_route_status(ROUTE_ID, "paused", 40.7, -73.9)

        assert isinstance(json.loads(last_request().body)["event_timestamp"], int)

    def test_a_v5_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.GET,
            f"{ROUTE_STATUS_V5}/{ROUTE_ID}",
            json={"status": False, "code": 404, "messages": {"route": ["Not found"]}},
            status=404,
        )

        result = client.route_status.get_route_status(ROUTE_ID)

        assert "errors" in result

    @pytest.mark.xfail(
        strict=True, raises=AssertionError, reason="security: route_id is put in the URL path without encoding"
    )
    def test_a_route_id_cannot_escape_its_path_segment(self, client, monkeypatch):
        urls = []

        def capture(url, params, request_method, **kwargs):
            urls.append(url)
            raise RuntimeError("stop before sending")

        monkeypatch.setattr(client, "_make_request", capture)

        with pytest.raises(RuntimeError):
            client.route_status.get_route_status("../secret")

        assert urls == [f"{ROUTE_STATUS_V5}/..%2Fsecret"]


class TestOrdersGroup:
    def test_posts_the_filters(self, client, mocked, last_request):
        mocked.add(responses.POST, ORDERS_GROUP_V5, json={"data": {"items": [{"group_id": 7}]}}, status=200)

        items = client.orders_group.get_orders_group(["2026-10-01", "2026-10-31"], ["new"])

        assert items == [{"group_id": 7}]
        assert json.loads(last_request().body) == {
            "filters": {"scheduled_for_range": ["2026-10-01", "2026-10-31"], "statuses": ["new"]}
        }

    def test_returns_an_empty_list_without_data(self, client, mocked):
        mocked.add(responses.POST, ORDERS_GROUP_V5, json={"total": 0}, status=200)

        assert client.orders_group.get_orders_group(["2026-10-01"], []) == []

    @pytest.mark.xfail(
        strict=True, raises=TypeError, reason="#35: ParamValueException is raised with a missing argument (TypeError)"
    )
    def test_an_invalid_range_raises_param_value_exception(self, client):
        with pytest.raises(ParamValueException):
            client.orders_group.get_orders_group(["10/01/2026"], [])

    def test_assign_optimization_profile(self, client, mocked, last_request):
        mocked.add(responses.POST, ASSIGN_PROFILES_V5, json={"status": True}, status=200)

        client.orders_group.assign_optimization_profile("profile-1", 42)

        assert json.loads(last_request().body) == {"group_id": 42, "optimization_profile_id": "profile-1"}

    @pytest.mark.xfail(
        strict=True, raises=UnboundLocalError, reason="#38: a ValueError from the transport becomes UnboundLocalError"
    )
    def test_a_transport_value_error_is_not_turned_into_unbound_local_error(self, client, monkeypatch):
        def boom(*args, **kwargs):
            raise requests.exceptions.InvalidHeader("bad header")

        monkeypatch.setattr(client, "_make_request", boom)

        with pytest.raises(requests.exceptions.InvalidHeader):
            client.orders_group.assign_optimization_profile("profile-1", 42)


class TestOptimizationProfiles:
    def test_gets_the_profile_list(self, client, mocked, last_request):
        mocked.add(responses.GET, OPTIMIZATION_PROFILES_V5, json={"items": []}, status=200)

        assert client.optimization_profiles.get_optimization_profiles() == {"items": []}
        assert last_request().method == "GET"

    def test_an_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.GET, OPTIMIZATION_PROFILES_V5, json={"status": False, "code": 401}, status=401)

        assert "errors" in client.optimization_profiles.get_optimization_profiles()

    @pytest.mark.xfail(
        strict=True, raises=UnboundLocalError, reason="#38: a ValueError from the transport becomes UnboundLocalError"
    )
    def test_a_transport_value_error_is_not_turned_into_unbound_local_error(self, client, monkeypatch):
        def boom(*args, **kwargs):
            raise requests.exceptions.InvalidURL("bad url")

        monkeypatch.setattr(client, "_make_request", boom)

        with pytest.raises(requests.exceptions.InvalidURL):
            client.optimization_profiles.get_optimization_profiles()
