"""Request-level tests for :class:`route4me.locations.Locations`."""

import json

import pytest
import responses

from route4me.api_endpoints import (
    LOCATION_TYPES_V5,
    LOCATIONS_CLUSTERING_V5,
    LOCATIONS_EXPORT_COLUMNS_V5,
    LOCATIONS_EXPORT_V5,
    LOCATIONS_HEATMAP_V5,
    LOCATIONS_LIST_COMBINED_V5,
    LOCATIONS_LIST_V5,
    LOCATIONS_TERRITORIES_V5,
)
from route4me.exceptions import ParamValueException

LOCATION_TYPE_ID = "LOCATION-TYPE-1"
LOCATION_TYPE = {"name": "Warehouse", "is_parent_type": True, "is_child_type": False}
QUERY = {"filters": {"search_query": "Main St"}, "page": 1, "per_page": 20, "order_by": [["address_alias", "asc"]]}


class TestLocationQueries:
    @pytest.mark.parametrize(
        ("method", "endpoint", "extra"),
        [
            ("get_locations_list", LOCATIONS_LIST_V5, {}),
            ("get_locations_combined", LOCATIONS_LIST_COMBINED_V5, {}),
            ("get_locations_clustering", LOCATIONS_CLUSTERING_V5, {"clustering": {"zoom": 10}, "with_clusters": True}),
            ("get_locations_heatmap", LOCATIONS_HEATMAP_V5, {"zoom": 8}),
            ("get_locations_territories", LOCATIONS_TERRITORIES_V5, {"territories_page": 1}),
            ("get_locations_export_columns", LOCATIONS_EXPORT_COLUMNS_V5, {"address_ids": [1, 2]}),
        ],
    )
    def test_posts_the_query_as_the_json_body(self, client, mocked, last_request, query_of, method, endpoint, extra):
        mocked.add(responses.POST, endpoint, json={"items": []}, status=200)

        result = getattr(client.locations, method)(**QUERY, **extra)

        assert result == {"items": []}
        assert last_request().method == "POST"
        assert query_of(last_request()) == {}
        assert json.loads(last_request().body) == dict(QUERY, **extra)

    def test_a_query_without_fields_sends_an_empty_object(self, client, mocked, last_request):
        mocked.add(responses.POST, LOCATIONS_LIST_V5, json={"items": []}, status=200)

        client.locations.get_locations_list()

        assert json.loads(last_request().body) == {}

    def test_export_locations_returns_the_empty_body_of_a_202(self, client, mocked, last_request):
        mocked.add(responses.POST, LOCATIONS_EXPORT_V5, body=b"", status=202)

        result = client.locations.export_locations(columns=["address_alias"], format="csv", filename="locations")

        assert result == b""
        assert last_request().method == "POST"
        assert json.loads(last_request().body) == {
            "columns": ["address_alias"],
            "format": "csv",
            "filename": "locations",
        }

    def test_export_locations_decodes_a_json_reply(self, client, mocked):
        mocked.add(responses.POST, LOCATIONS_EXPORT_V5, json={"status": True}, status=202)

        assert client.locations.export_locations() == {"status": True}

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.POST, LOCATIONS_LIST_V5, json={"errors": ["The page must be an integer."]}, status=406)

        assert client.locations.get_locations_list(page="x") == {"errors": ["The page must be an integer."]}

    def test_an_export_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.POST, LOCATIONS_EXPORT_V5, json={"errors": ["Bad format"]}, status=406)

        assert client.locations.export_locations(format="pdf") == {"errors": ["Bad format"]}


class TestLocationTypes:
    def test_get_location_types_sends_the_filters_as_bracketed_query_keys(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, LOCATION_TYPES_V5, json={"data": []}, status=200)

        result = client.locations.get_location_types(page=1, per_page=10, filters={"search_query": "ware"})

        assert result == {"data": []}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {"page": "1", "per_page": "10", "filters[search_query]": "ware"}
        assert last_request().body is None

    def test_get_location_type_by_id(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{LOCATION_TYPES_V5}/{LOCATION_TYPE_ID}", json=LOCATION_TYPE, status=200)

        assert client.locations.get_location_type_by_id(LOCATION_TYPE_ID) == LOCATION_TYPE
        assert last_request().method == "GET"

    def test_create_location_type_posts_the_fields(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, LOCATION_TYPES_V5, json=LOCATION_TYPE, status=200)

        client.locations.create_location_type(description="Storage sites", **LOCATION_TYPE)

        assert last_request().method == "POST"
        assert query_of(last_request()) == {}
        assert json.loads(last_request().body) == dict(LOCATION_TYPE, description="Storage sites")

    @pytest.mark.parametrize("field", ["name", "is_parent_type", "is_child_type"])
    def test_create_location_type_names_a_missing_required_field(self, client, mocked, field):
        fields = {k: v for k, v in LOCATION_TYPE.items() if k != field}

        with pytest.raises(ParamValueException) as excinfo:
            client.locations.create_location_type(**fields)

        assert field in str(excinfo.value)
        assert not mocked.calls

    def test_update_location_type_puts_the_fields(self, client, mocked, last_request):
        mocked.add(responses.PUT, f"{LOCATION_TYPES_V5}/{LOCATION_TYPE_ID}", json=LOCATION_TYPE, status=200)

        client.locations.update_location_type(LOCATION_TYPE_ID, **LOCATION_TYPE)

        assert last_request().method == "PUT"
        assert json.loads(last_request().body) == LOCATION_TYPE

    def test_update_location_type_requires_the_same_fields(self, client, mocked):
        with pytest.raises(ParamValueException):
            client.locations.update_location_type(LOCATION_TYPE_ID, name="Warehouse")

        assert not mocked.calls

    def test_delete_location_type(self, client, mocked, last_request):
        mocked.add(responses.DELETE, f"{LOCATION_TYPES_V5}/{LOCATION_TYPE_ID}", json={"status": True}, status=200)

        assert client.locations.delete_location_type(LOCATION_TYPE_ID) == {"status": True}
        assert last_request().method == "DELETE"

    def test_a_location_type_id_with_a_slash_is_encoded(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{LOCATION_TYPES_V5}/a%2Fb", json={}, status=200)

        client.locations.get_location_type_by_id("a/b")

        assert last_request().path_url == "/modules/api/v5.0/address-book/locations/types/a%2Fb"

    @pytest.mark.parametrize("method", ["get_location_type_by_id", "delete_location_type"])
    def test_an_empty_location_type_id_is_rejected_before_any_request(self, client, mocked, method):
        with pytest.raises(ParamValueException):
            getattr(client.locations, method)("")

        assert not mocked.calls

    def test_update_with_an_empty_location_type_id_is_rejected(self, client, mocked):
        with pytest.raises(ParamValueException):
            client.locations.update_location_type("", **LOCATION_TYPE)

        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.GET, f"{LOCATION_TYPES_V5}/{LOCATION_TYPE_ID}", json={"errors": ["Not found"]}, status=404)

        assert client.locations.get_location_type_by_id(LOCATION_TYPE_ID) == {"errors": ["Not found"]}
