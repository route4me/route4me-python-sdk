"""Request-level tests for :class:`route4me.route.Route`.

Each test pins the HTTP method, endpoint, query string and body the SDK sends
for one public method. Known defects are written as the *correct* behaviour
under ``xfail(strict=True)``: when the fix lands the test passes, strict xfail
turns that into a failure, and the marker has to be removed with the fix.
"""

import json
from urllib.parse import parse_qs

import pytest
import responses

from route4me import Route4Me
from route4me.api_endpoints import (
    ADDRESS_HOST,
    DUPLICATE_ROUTE,
    EXPORTER,
    EXPORTER_V5,
    GET_ACTIVITIES_HOST,
    MERGE_ROUTES_HOST,
    RESEQUENCE_ROUTE,
    ROUTE_HOST,
    SHARE_ROUTE_HOST,
)
from route4me.exceptions import ParamValueException

ROUTE_ID = "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"
OTHER_ROUTE_ID = "BADC0DE0BADC0DE0BADC0DE0BADC0DE0"
DESTINATION_ID = 98765
ADDRESSES = [{"address": "754 5th Ave New York, NY 10019", "lat": 40.7636197, "lng": -73.9744388}]


def body_of(request):
    """Decode a JSON request body."""
    return json.loads(request.body)


class TestGetRoute:
    def test_sends_the_route_id_as_a_query_parameter(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.GET, ROUTE_HOST, json={"route_id": ROUTE_ID}, status=200)

        result = client.route.get_route(route_id=ROUTE_ID)

        assert result == {"route_id": ROUTE_ID}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {"api_key": api_key, "route_id": ROUTE_ID}

    def test_requires_a_route_id(self, client):
        with pytest.raises(ParamValueException):
            client.route.get_route()

    def test_a_later_call_does_not_reuse_the_previous_route_id(self, client, mocked):
        mocked.add(responses.GET, ROUTE_HOST, json={}, status=200)
        client.route.get_route(route_id=ROUTE_ID)

        with pytest.raises(ParamValueException):
            client.route.get_route()

    def test_tracking_does_not_leak_into_the_next_get_route(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, ROUTE_HOST, json={}, status=200)
        client.route.get_route_tracking(route_id=ROUTE_ID)

        client.route.get_route(route_id=OTHER_ROUTE_ID)

        assert "device_tracking_history" not in query_of(last_request())

    def test_tracking_asks_for_the_device_history(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, ROUTE_HOST, json={}, status=200)

        client.route.get_route_tracking(route_id=ROUTE_ID)

        assert query_of(last_request())["device_tracking_history"] == "1"


class TestSimpleGets:
    @pytest.mark.parametrize(
        ("method", "endpoint", "kwargs"),
        [
            ("get_routes", ROUTE_HOST, {"limit": 10, "offset": 0}),
            ("get_activities", GET_ACTIVITIES_HOST, {"route_id": ROUTE_ID, "limit": 10, "offset": 0}),
            ("duplicate_route", DUPLICATE_ROUTE, {"route_id": ROUTE_ID}),
            ("get_route_path_points", ROUTE_HOST, {"route_id": ROUTE_ID, "route_path_output": "Points"}),
            ("get_route_directions", ROUTE_HOST, {"route_id": ROUTE_ID, "directions": 1}),
            (
                "resequence_route_all",
                RESEQUENCE_ROUTE,
                {"route_id": ROUTE_ID, "disable_optimization": 0, "optimize": "Distance"},
            ),
        ],
    )
    def test_sends_kwargs_as_query_parameters(
        self, client, mocked, query_of, last_request, api_key, method, endpoint, kwargs
    ):
        mocked.add(responses.GET, endpoint, json={"ok": True}, status=200)

        result = getattr(client.route, method)(**kwargs)

        assert result == {"ok": True}
        assert last_request().method == "GET"
        expected = {k: str(v) for k, v in kwargs.items()}
        expected["api_key"] = api_key
        assert query_of(last_request()) == expected

    @pytest.mark.parametrize(
        ("method", "kwargs"),
        [
            ("get_routes", {"limit": 10}),
            ("get_activities", {"route_id": ROUTE_ID}),
            ("duplicate_route", {}),
            ("get_route_path_points", {"route_id": ROUTE_ID}),
            ("get_route_directions", {"route_id": ROUTE_ID}),
            ("resequence_route_all", {"route_id": ROUTE_ID}),
        ],
    )
    def test_missing_required_parameters_raise(self, client, method, kwargs):
        with pytest.raises(ParamValueException):
            getattr(client.route, method)(**kwargs)

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.GET, ROUTE_HOST, json={"errors": ["Route not found"]}, status=404)

        result = client.route.get_routes(limit=1, offset=0)

        assert result == {"errors": ["Route not found"]}


class TestDeleteRoutes:
    def test_joins_a_list_of_route_ids(self, client, mocked, query_of, last_request):
        mocked.add(responses.DELETE, ROUTE_HOST, json={"deleted": True}, status=200)

        client.route.delete_routes(route_id=[ROUTE_ID, OTHER_ROUTE_ID])

        assert last_request().method == "DELETE"
        assert query_of(last_request())["route_id"] == f"{ROUTE_ID},{OTHER_ROUTE_ID}"

    @pytest.mark.xfail(
        strict=True, raises=AssertionError, reason="a single route_id string is split into one id per character"
    )
    def test_a_single_route_id_string_is_sent_as_is(self, client, mocked, query_of, last_request):
        mocked.add(responses.DELETE, ROUTE_HOST, json={"deleted": True}, status=200)

        client.route.delete_routes(route_id=ROUTE_ID)

        assert query_of(last_request())["route_id"] == ROUTE_ID

    def test_requires_route_ids(self, client):
        with pytest.raises(ParamValueException):
            client.route.delete_routes()


class TestDeleteRoute:
    def test_returns_the_deleted_flag(self, client, mocked, query_of, last_request):
        mocked.add(responses.DELETE, ROUTE_HOST, json={"deleted": True}, status=200)

        assert client.route.delete_route(route_id=ROUTE_ID) is True
        assert query_of(last_request())["route_id"] == ROUTE_ID

    def test_requires_a_route_id(self, client):
        with pytest.raises(ParamValueException):
            client.route.delete_route()


class TestRouteUpdates:
    """``insert_address_into_route`` and friends all funnel through ``_update_route``."""

    @pytest.mark.parametrize(
        ("method", "payload"),
        [
            ("insert_address_into_route", {"addresses": ADDRESSES}),
            ("move_addresses_from_route", {"addresses": ADDRESSES}),
            ("update_route_parameters", {"parameters": {"route_name": "Renamed"}}),
            ("update_route", {"parameters": {"route_name": "Renamed"}}),
        ],
    )
    def test_puts_to_the_route_endpoint(self, client, mocked, query_of, last_request, method, payload):
        mocked.add(responses.PUT, ROUTE_HOST, json={"route_id": ROUTE_ID}, status=200)

        getattr(client.route, method)(payload, ROUTE_ID)

        assert last_request().method == "PUT"
        assert query_of(last_request())["route_id"] == ROUTE_ID

    @pytest.mark.parametrize(
        ("method", "payload"),
        [
            ("insert_address_into_route", {"addresses": ADDRESSES}),
            ("move_addresses_from_route", {"addresses": [{"route_destination_id": DESTINATION_ID}]}),
            ("update_route_parameters", {"parameters": {"route_name": "Renamed"}}),
            ("update_route", {"parameters": {"route_name": "Renamed"}}),
        ],
    )
    def test_sends_the_payload_as_json(self, client, mocked, last_request, method, payload):
        mocked.add(responses.PUT, ROUTE_HOST, json={"route_id": ROUTE_ID}, status=200)

        getattr(client.route, method)(payload, ROUTE_ID)

        assert body_of(last_request()) == payload

    def test_a_per_call_timeout_reaches_the_transport(self, client, monkeypatch):
        seen = {}

        def capture(url, params, request_method, **kwargs):
            seen.update(kwargs)
            raise RuntimeError("stop before sending")

        monkeypatch.setattr(client, "_make_request", capture)

        with pytest.raises(RuntimeError):
            client.route.insert_address_into_route({"addresses": ADDRESSES}, ROUTE_ID, timeout=(5, 120))

        assert seen["timeout"] == (5, 120)

    def test_a_put_is_never_retried_even_with_retries_on(self, mocked):
        client = Route4Me("1" * 32, retry_count=3, retry_initial_delay=0)
        mocked.add(responses.PUT, ROUTE_HOST, json={"errors": ["timeout"]}, status=524)

        client.route.insert_address_into_route({"addresses": ADDRESSES}, ROUTE_ID)

        assert len(mocked.calls) == 1

    def test_a_cloudflare_timeout_on_a_get_is_retried(self, mocked):
        client = Route4Me("1" * 32, retry_count=2, retry_initial_delay=0)
        mocked.add(responses.GET, ROUTE_HOST, json={"errors": ["timeout"]}, status=524)

        client.route.get_routes(limit=1, offset=0)

        assert len(mocked.calls) == 3

    def test_optimal_position_insert_sends_json(self, client, mocked, query_of, last_request):
        mocked.add(responses.PUT, ROUTE_HOST, json={}, status=200)

        client.route.insert_address_into_route_optimal_position(
            route_id=ROUTE_ID, addresses=ADDRESSES, optimal_position=True
        )

        assert query_of(last_request())["route_id"] == ROUTE_ID
        assert body_of(last_request()) == {"addresses": ADDRESSES, "optimal_position": True}

    def test_resequence_route_sends_ids_in_the_query(self, client, mocked, query_of, last_request):
        mocked.add(responses.PUT, ROUTE_HOST, json={}, status=200)

        client.route.resequence_route(
            route_id=ROUTE_ID, route_destination_id=DESTINATION_ID, addresses=[{"sequence_no": 2}]
        )

        query = query_of(last_request())
        assert query["route_id"] == ROUTE_ID
        assert query["route_destination_id"] == str(DESTINATION_ID)
        assert body_of(last_request()) == {"addresses": [{"sequence_no": 2}]}

    def test_resequence_multiple_stops_sends_the_addresses_as_json(self, client, mocked, last_request):
        mocked.add(responses.PUT, ROUTE_HOST, json={}, status=200)
        data = {"addresses": [{"route_destination_id": DESTINATION_ID, "sequence_no": 3}]}

        client.route.resequence_multiple_stops(ROUTE_ID, data)

        assert body_of(last_request()) == data

    def test_update_destination_custom_data_targets_the_address_endpoint(self, client, mocked, query_of, last_request):
        mocked.add(responses.PUT, ADDRESS_HOST, json={}, status=200)

        client.route.update_route_destination_custom_data(
            route_id=ROUTE_ID, route_destination_id=DESTINATION_ID, custom_fields={"color": "red"}
        )

        assert query_of(last_request())["route_destination_id"] == str(DESTINATION_ID)
        assert body_of(last_request()) == {"custom_fields": {"color": "red"}}

    @pytest.mark.parametrize(
        ("method", "kwargs"),
        [
            ("insert_address_into_route_optimal_position", {"route_id": ROUTE_ID}),
            ("resequence_route", {"route_id": ROUTE_ID}),
            ("update_route_destination_custom_data", {"route_id": ROUTE_ID}),
            ("share_route", {"route_id": ROUTE_ID}),
            ("merge_routes", {}),
        ],
    )
    def test_missing_required_parameters_raise(self, client, method, kwargs):
        with pytest.raises(ParamValueException):
            getattr(client.route, method)(**kwargs)


class TestShareAndMerge:
    def test_share_route_posts_the_recipient(self, client, mocked, query_of, last_request):
        mocked.add(responses.POST, SHARE_ROUTE_HOST, json={"status": True}, status=200)

        client.route.share_route(route_id=ROUTE_ID, response_format="json", recipient_email="ops@example.com")

        assert last_request().method == "POST"
        assert query_of(last_request())["response_format"] == "json"
        assert body_of(last_request()) == {"recipient_email": "ops@example.com"}

    def test_merge_routes_posts_form_data(self, client, mocked, last_request):
        mocked.add(responses.POST, MERGE_ROUTES_HOST, json={"status": True}, status=200)

        client.route.merge_routes(route_ids=f"{ROUTE_ID},{OTHER_ROUTE_ID}")

        assert parse_qs(last_request().body) == {"route_ids": [f"{ROUTE_ID},{OTHER_ROUTE_ID}"]}


class TestExport:
    def test_v5_export_posts_to_the_route_export_endpoint(self, client, mocked, last_request):
        url = EXPORTER_V5.format(route_id=ROUTE_ID)
        mocked.add(responses.POST, url, body=b"csv,data", status=200)

        assert client.route.export_route_v5(ROUTE_ID) == b"csv,data"
        assert last_request().method == "POST"

    def test_v5_export_encodes_the_route_id(self, client, monkeypatch):
        urls = []

        def capture(url, params, request_method, **kwargs):
            urls.append(url)
            raise RuntimeError("stop before sending")

        monkeypatch.setattr(client, "_make_request", capture)

        with pytest.raises(RuntimeError):
            client.route.export_route_v5("../../secret")

        assert urls == [EXPORTER_V5.format(route_id="..%2F..%2Fsecret")]

    def test_the_legacy_export_is_deprecated(self, client, mocked):
        mocked.add(responses.POST, EXPORTER, body=b"csv", status=200)

        with pytest.warns(DeprecationWarning):
            client.route.export_route(ROUTE_ID)
