"""Request-level tests for :class:`route4me.route_destinations_v5.RouteDestinationsV5`."""

import json

import pytest
import responses

from route4me.api_endpoints import (
    ROUTE_DESTINATIONS_COLUMNS_V5,
    ROUTE_DESTINATIONS_LIST_FIELDS_V5,
    ROUTE_DESTINATIONS_LIST_V5,
    ROUTE_DESTINATIONS_SEQUENCE_V5,
    ROUTE_DESTINATIONS_SORTING_V5,
    ROUTE_DESTINATIONS_V5,
)
from route4me.exceptions import ParamValueException

ROUTE_ID = "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"
DESTINATION_ID = 98765
COORDINATES = [{"lat": 40.7636197, "lng": -73.9744388}, {"lat": 40.7669692, "lng": -73.9693864}]


def body_of(request):
    """Decode a JSON request body."""
    return json.loads(request.body)


class TestDestinationsList:
    def test_posts_the_filters_as_the_json_body(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, ROUTE_DESTINATIONS_LIST_V5, json={"items": [], "total_items_count": 0}, status=200)

        result = client.route_destinations_v5.get_destinations_list(
            filters={"route_id": [ROUTE_ID]}, page=1, per_page=50
        )

        assert result == {"items": [], "total_items_count": 0}
        assert last_request().method == "POST"
        assert query_of(last_request()) == {}
        assert body_of(last_request()) == {"filters": {"route_id": [ROUTE_ID]}, "page": 1, "per_page": 50}

    def test_requires_filters(self, client, mocked):
        with pytest.raises(ParamValueException) as raised:
            client.route_destinations_v5.get_destinations_list(page=1)

        assert raised.value.param == "filters"
        assert not mocked.calls

    def test_get_destination_fields(self, client, mocked, last_request):
        mocked.add(responses.GET, ROUTE_DESTINATIONS_LIST_FIELDS_V5, json={"fields": []}, status=200)

        assert client.route_destinations_v5.get_destination_fields() == {"fields": []}
        assert last_request().method == "GET"


class TestColumns:
    def test_get_destination_columns_sends_the_key_in_the_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, ROUTE_DESTINATIONS_COLUMNS_V5, json={"order": ["alias"]}, status=200)

        assert client.route_destinations_v5.get_destination_columns("route_columns_config_key") == {"order": ["alias"]}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {"columns_configurator_key": "route_columns_config_key"}

    def test_edit_destination_columns_puts_the_order(self, client, mocked, last_request, query_of):
        mocked.add(responses.PUT, ROUTE_DESTINATIONS_COLUMNS_V5, json={"order": ["alias", "eta"]}, status=200)

        client.route_destinations_v5.edit_destination_columns(
            columns_configurator_key="route_columns_config_key", order=["alias", "eta"]
        )

        assert last_request().method == "PUT"
        assert query_of(last_request()) == {}
        assert body_of(last_request()) == {
            "columns_configurator_key": "route_columns_config_key",
            "order": ["alias", "eta"],
        }

    @pytest.mark.parametrize(
        ("kwargs", "missing"),
        [({"order": []}, "columns_configurator_key"), ({"columns_configurator_key": "key"}, "order")],
    )
    def test_edit_destination_columns_requires_the_key_and_the_order(self, client, mocked, kwargs, missing):
        with pytest.raises(ParamValueException) as raised:
            client.route_destinations_v5.edit_destination_columns(**kwargs)

        assert raised.value.param == missing
        assert not mocked.calls


class TestLookups:
    def test_get_destination_by_label_code(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, ROUTE_DESTINATIONS_SORTING_V5, json={"route_id": ROUTE_ID}, status=200)

        assert client.route_destinations_v5.get_destination_by_label_code("LABEL-5") == {"route_id": ROUTE_ID}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {"label_code": "LABEL-5"}

    @pytest.mark.parametrize(
        ("method", "name"),
        [("get_destination_by_label_code", "label_code"), ("get_destination_columns", "columns_configurator_key")],
    )
    @pytest.mark.parametrize("value", ["", "  ", None])
    def test_an_empty_query_value_is_rejected(self, client, mocked, method, name, value):
        with pytest.raises(ParamValueException) as raised:
            getattr(client.route_destinations_v5, method)(value)

        assert raised.value.param == name
        assert not mocked.calls

    def test_get_destination_sequence_posts_the_coordinates(self, client, mocked, last_request):
        mocked.add(responses.POST, ROUTE_DESTINATIONS_SEQUENCE_V5, json={"items": COORDINATES}, status=200)

        assert client.route_destinations_v5.get_destination_sequence(COORDINATES) == {"items": COORDINATES}
        assert last_request().method == "POST"
        assert body_of(last_request()) == {"coordinates": COORDINATES}

    def test_get_destination_sequence_requires_coordinates(self, client, mocked):
        with pytest.raises(ParamValueException):
            client.route_destinations_v5.get_destination_sequence(None)

        assert not mocked.calls


class TestDeleteRouteDestination:
    def test_deletes_by_id_in_the_path(self, client, mocked, last_request):
        mocked.add(responses.DELETE, f"{ROUTE_DESTINATIONS_V5}/{DESTINATION_ID}", json={"status": True}, status=200)

        assert client.route_destinations_v5.delete_route_destination(DESTINATION_ID) == {"status": True}
        assert last_request().method == "DELETE"
        assert last_request().body is None

    def test_an_empty_reply_is_returned_raw(self, client, mocked):
        mocked.add(responses.DELETE, f"{ROUTE_DESTINATIONS_V5}/{DESTINATION_ID}", body=b"", status=204)

        assert client.route_destinations_v5.delete_route_destination(DESTINATION_ID) == b""

    def test_an_id_cannot_escape_its_path_segment(self, client, mocked, last_request):
        mocked.add(responses.DELETE, f"{ROUTE_DESTINATIONS_V5}/a%2Fb", json={}, status=200)

        client.route_destinations_v5.delete_route_destination("a/b")

        assert last_request().url == f"{ROUTE_DESTINATIONS_V5}/a%2Fb"

    @pytest.mark.parametrize("destination_id", ["", None])
    def test_an_empty_id_is_rejected_before_any_request(self, client, mocked, destination_id):
        with pytest.raises(ParamValueException):
            client.route_destinations_v5.delete_route_destination(destination_id)

        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.DELETE,
            f"{ROUTE_DESTINATIONS_V5}/{DESTINATION_ID}",
            json={"status": False, "code": 404, "messages": ["Destination not found"]},
            status=404,
        )

        assert client.route_destinations_v5.delete_route_destination(DESTINATION_ID) == {
            "errors": ["Destination not found"]
        }


class TestErrors:
    def test_a_v5_error_is_returned_as_a_dict(self, client, mocked, load_fixture):
        mocked.add(responses.POST, ROUTE_DESTINATIONS_LIST_V5, json=load_fixture("error_v5"), status=422)

        result = client.route_destinations_v5.get_destinations_list(filters={})

        assert result == {"errors": ["The route id field is required."]}
