"""Request-level tests for :class:`route4me.routes_v5.RoutesV5`."""

import json

import pytest
import responses

from route4me.api_endpoints import (
    ROUTES_CUSTOM_DATA_BULK_V5,
    ROUTES_CUSTOM_DATA_KEYS_V5,
    ROUTES_DATATABLE_CONFIG_V5,
    ROUTES_DELETE_V5,
    ROUTES_LIST_V5,
    ROUTES_LOOKUP_FOR_NEW_DESTINATION_V5,
    ROUTES_V5,
    ROUTES_V5_1,
)
from route4me.exceptions import ParamValueException

ROUTE_ID = "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"
OTHER_ROUTE_ID = "BADC0DE0BADC0DE0BADC0DE0BADC0DE0"
CUSTOM_DATA_URL = f"{ROUTES_V5}/{ROUTE_ID}/custom-data"
PAGE = {"data": [{"route_id": ROUTE_ID}], "links": {}, "meta": {"total": 1}}


def body_of(request):
    """Decode a JSON request body."""
    return json.loads(request.body)


class TestRouteLists:
    @pytest.mark.parametrize(
        ("method", "endpoint"),
        [
            ("get_routes", ROUTES_V5),
            ("get_routes_list", ROUTES_LIST_V5),
            ("get_routes_by_filter", ROUTES_V5_1),
        ],
    )
    def test_posts_the_keywords_as_the_json_body(self, client, mocked, last_request, query_of, method, endpoint):
        mocked.add(responses.POST, endpoint, json=PAGE, status=200)

        result = getattr(client.routes_v5, method)(
            filters={"schedule_date": ["2026-10-01", "2026-10-31"]},
            order_by=[["route_created_unix", "desc"]],
            page=1,
            per_page=20,
            timezone="America/New_York",
        )

        assert result == PAGE
        request = last_request()
        assert request.method == "POST"
        assert request.url.split("?")[0] == endpoint
        assert query_of(request) == {}
        assert body_of(request) == {
            "filters": {"schedule_date": ["2026-10-01", "2026-10-31"]},
            "order_by": [["route_created_unix", "desc"]],
            "page": 1,
            "per_page": 20,
            "timezone": "America/New_York",
        }

    def test_get_routes_by_filter_uses_api_5_1(self, client, mocked, last_request):
        mocked.add(responses.POST, ROUTES_V5_1, json=PAGE, status=200)

        client.routes_v5.get_routes_by_filter(filters={"created_date": ["2026-10-01", "2026-10-02"]})

        assert "/modules/api/v5.1/routes" in last_request().url

    def test_a_list_without_keywords_posts_an_empty_object(self, client, mocked, last_request):
        mocked.add(responses.POST, ROUTES_LIST_V5, json=PAGE, status=200)

        client.routes_v5.get_routes_list()

        assert body_of(last_request()) == {}

    def test_a_later_call_does_not_reuse_the_previous_body(self, client, mocked, last_request):
        mocked.add(responses.POST, ROUTES_V5, json=PAGE, status=200)
        client.routes_v5.get_routes(page=2)

        client.routes_v5.get_routes(per_page=5)

        assert body_of(last_request()) == {"per_page": 5}


class TestDeleteRoutes:
    def test_sends_the_filters_and_signature_as_the_json_body(self, client, mocked, last_request):
        mocked.add(responses.DELETE, ROUTES_DELETE_V5, json={"status": True, "removed": 2, "async": False}, status=200)

        result = client.routes_v5.delete_routes(
            filters={"route_id": [ROUTE_ID, OTHER_ROUTE_ID]}, signature="SIGNATURE-1"
        )

        assert result == {"status": True, "removed": 2, "async": False}
        assert last_request().method == "DELETE"
        assert body_of(last_request()) == {
            "filters": {"route_id": [ROUTE_ID, OTHER_ROUTE_ID]},
            "signature": "SIGNATURE-1",
        }

    @pytest.mark.parametrize(
        ("kwargs", "missing"),
        [({"signature": "SIGNATURE-1"}, "filters"), ({"filters": {}}, "signature"), ({}, "filters, signature")],
    )
    def test_requires_filters_and_a_signature(self, client, mocked, kwargs, missing):
        with pytest.raises(ParamValueException) as raised:
            client.routes_v5.delete_routes(**kwargs)

        assert raised.value.param == missing
        assert not mocked.calls


class TestDataTableConfig:
    def test_gets_the_config(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, ROUTES_DATATABLE_CONFIG_V5, json={"columns": []}, status=200)

        assert client.routes_v5.get_route_data_table_config() == {"columns": []}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {}
        assert last_request().body is None


class TestDynamicInsert:
    def test_posts_the_location_and_options(self, client, mocked, last_request):
        mocked.add(responses.POST, ROUTES_LOOKUP_FOR_NEW_DESTINATION_V5, json=[{"route_id": ROUTE_ID}], status=200)

        result = client.routes_v5.dynamic_insert_route_addresses(
            lat=40.7636197, lng=-73.9744388, scheduled_for="2026-10-22", lookup_results_limit=3
        )

        assert result == [{"route_id": ROUTE_ID}]
        assert last_request().method == "POST"
        assert body_of(last_request()) == {
            "lat": 40.7636197,
            "lng": -73.9744388,
            "scheduled_for": "2026-10-22",
            "lookup_results_limit": 3,
        }

    @pytest.mark.parametrize(("kwargs", "missing"), [({"lat": 40.7}, "lng"), ({"lng": -73.9}, "lat")])
    def test_requires_the_coordinates(self, client, mocked, kwargs, missing):
        with pytest.raises(ParamValueException) as raised:
            client.routes_v5.dynamic_insert_route_addresses(**kwargs)

        assert raised.value.param == missing
        assert not mocked.calls


class TestCustomData:
    def test_get_route_custom_data(self, client, mocked, last_request):
        mocked.add(responses.GET, CUSTOM_DATA_URL, json={"priority": "high"}, status=200)

        assert client.routes_v5.get_route_custom_data(ROUTE_ID) == {"priority": "high"}
        assert last_request().method == "GET"
        assert last_request().body is None

    def test_update_route_custom_data_puts_the_whole_map(self, client, mocked, last_request):
        mocked.add(responses.PUT, CUSTOM_DATA_URL, json={"priority": "high", "dock": "4"}, status=200)

        result = client.routes_v5.update_route_custom_data(ROUTE_ID, {"priority": "high", "dock": "4"})

        assert result == {"priority": "high", "dock": "4"}
        assert last_request().method == "PUT"
        assert body_of(last_request()) == {"priority": "high", "dock": "4"}

    def test_update_route_custom_data_with_an_empty_map_clears_it(self, client, mocked, last_request):
        mocked.add(responses.PUT, CUSTOM_DATA_URL, json={}, status=200)

        client.routes_v5.update_route_custom_data(ROUTE_ID, {})

        assert body_of(last_request()) == {}

    def test_get_bulk_route_custom_data(self, client, mocked, last_request):
        mocked.add(responses.POST, ROUTES_CUSTOM_DATA_BULK_V5, json={"data": []}, status=200)

        client.routes_v5.get_bulk_route_custom_data([ROUTE_ID, OTHER_ROUTE_ID])

        assert last_request().method == "POST"
        assert body_of(last_request()) == {"route_ids": [ROUTE_ID, OTHER_ROUTE_ID]}

    def test_get_bulk_route_custom_data_takes_one_id_as_a_string(self, client, mocked, last_request):
        mocked.add(responses.POST, ROUTES_CUSTOM_DATA_BULK_V5, json={"data": []}, status=200)

        client.routes_v5.get_bulk_route_custom_data(ROUTE_ID)

        assert body_of(last_request()) == {"route_ids": [ROUTE_ID]}

    def test_get_custom_data_keys(self, client, mocked, last_request):
        mocked.add(responses.GET, ROUTES_CUSTOM_DATA_KEYS_V5, json=["dock", "priority"], status=200)

        assert client.routes_v5.get_custom_data_keys() == ["dock", "priority"]
        assert last_request().method == "GET"

    @pytest.mark.parametrize(
        ("method", "args", "http_method"),
        [
            ("get_route_custom_data", (), responses.GET),
            ("update_route_custom_data", ({"dock": "4"},), responses.PUT),
        ],
    )
    def test_a_route_id_cannot_escape_its_path_segment(self, client, mocked, last_request, method, args, http_method):
        mocked.add(http_method, f"{ROUTES_V5}/a%2Fb/custom-data", json={}, status=200)

        getattr(client.routes_v5, method)("a/b", *args)

        assert last_request().url == f"{ROUTES_V5}/a%2Fb/custom-data"

    @pytest.mark.parametrize(
        ("method", "args"), [("get_route_custom_data", ()), ("update_route_custom_data", ({"dock": "4"},))]
    )
    @pytest.mark.parametrize("route_id", ["", None])
    def test_an_empty_route_id_is_rejected_before_any_request(self, client, mocked, method, args, route_id):
        with pytest.raises(ParamValueException):
            getattr(client.routes_v5, method)(route_id, *args)

        assert not mocked.calls


class TestErrors:
    def test_a_v5_error_is_returned_as_a_dict(self, client, mocked, load_fixture):
        mocked.add(responses.POST, ROUTES_LIST_V5, json=load_fixture("error_v5"), status=422)

        assert client.routes_v5.get_routes_list(page=1) == {"errors": ["The route id field is required."]}

    def test_a_custom_data_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.GET,
            CUSTOM_DATA_URL,
            json={"status": False, "code": 404, "messages": ["Route not found"]},
            status=404,
        )

        assert client.routes_v5.get_route_custom_data(ROUTE_ID) == {"errors": ["Route not found"]}
