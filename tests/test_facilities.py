"""Request-level tests for :class:`route4me.facilities.Facilities`."""

import json

import pytest
import responses

from route4me._params import nested_query
from route4me.api_endpoints import FACILITIES_V5, FACILITY_TYPES_V5
from route4me.exceptions import ParamValueException

FACILITY_ID = "FACILITY-1"
FACILITY = {
    "facility_alias": "Example Depot",
    "address": "123 Example St, Springfield",
    "coordinates": {"lat": 40.7, "lng": -73.9},
    "facility_types": [{"facility_type_id": 1, "is_default": True}],
}


class TestFacilities:
    def test_get_facilities_sends_the_filters_as_bracketed_query_keys(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, FACILITIES_V5, json={"data": [], "total": 0}, status=200)

        result = client.facilities.get_facilities(
            page=2, per_page=10, search_query="depot", filters={"status": [1, 2]}, order_by={"facility_alias": "asc"}
        )

        assert result == {"data": [], "total": 0}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {
            "page": "2",
            "per_page": "10",
            "search_query": "depot",
            "filters[status][]": ["1", "2"],
            "order_by[facility_alias]": "asc",
        }

    def test_get_facilities_without_filters_sends_no_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, FACILITIES_V5, json={"data": []}, status=200)

        client.facilities.get_facilities()

        assert query_of(last_request()) == {}

    def test_get_facility(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{FACILITIES_V5}/{FACILITY_ID}", json={"facility_id": FACILITY_ID}, status=200)

        assert client.facilities.get_facility(FACILITY_ID) == {"facility_id": FACILITY_ID}
        assert last_request().method == "GET"
        assert last_request().body is None

    def test_create_facility_posts_the_fields(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, FACILITIES_V5, json={"facility_id": FACILITY_ID}, status=200)

        client.facilities.create_facility(status=1, **FACILITY)

        assert last_request().method == "POST"
        assert query_of(last_request()) == {}
        assert json.loads(last_request().body) == dict(FACILITY, status=1)

    @pytest.mark.parametrize("field", ["facility_alias", "address", "coordinates", "facility_types"])
    def test_create_facility_names_a_missing_required_field(self, client, mocked, field):
        fields = {k: v for k, v in FACILITY.items() if k != field}

        with pytest.raises(ParamValueException) as excinfo:
            client.facilities.create_facility(**fields)

        assert field in str(excinfo.value)
        assert not mocked.calls

    def test_update_facility_puts_the_fields(self, client, mocked, last_request):
        mocked.add(responses.PUT, f"{FACILITIES_V5}/{FACILITY_ID}", json={"facility_id": FACILITY_ID}, status=200)

        client.facilities.update_facility(FACILITY_ID, **FACILITY)

        assert last_request().method == "PUT"
        assert json.loads(last_request().body) == FACILITY

    def test_update_facility_requires_the_same_fields(self, client, mocked):
        with pytest.raises(ParamValueException):
            client.facilities.update_facility(FACILITY_ID, facility_alias="Example Depot")

        assert not mocked.calls

    def test_delete_facility(self, client, mocked, last_request):
        mocked.add(responses.DELETE, f"{FACILITIES_V5}/{FACILITY_ID}", json=[{"facility_id": FACILITY_ID}], status=200)

        assert client.facilities.delete_facility(FACILITY_ID) == [{"facility_id": FACILITY_ID}]
        assert last_request().method == "DELETE"

    def test_get_facility_types(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, FACILITY_TYPES_V5, json={"data": [{"facility_type_id": 1}]}, status=200)

        assert client.facilities.get_facility_types() == {"data": [{"facility_type_id": 1}]}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {}

    def test_get_facility_type(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{FACILITY_TYPES_V5}/3", json={"facility_type_id": 3}, status=200)

        assert client.facilities.get_facility_type(3) == {"facility_type_id": 3}
        assert last_request().method == "GET"

    @pytest.mark.parametrize("bad_id", ["", "a/b", -1])
    def test_a_facility_type_id_must_be_an_integer(self, client, mocked, bad_id):
        with pytest.raises(ParamValueException):
            client.facilities.get_facility_type(bad_id)

        assert not mocked.calls

    def test_a_facility_id_with_a_slash_is_encoded(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{FACILITIES_V5}/a%2Fb", json={}, status=200)

        client.facilities.get_facility("a/b")

        assert last_request().path_url == "/modules/api/v5.0/facilities/a%2Fb"

    @pytest.mark.parametrize("method", ["get_facility", "delete_facility"])
    def test_an_empty_facility_id_is_rejected_before_any_request(self, client, mocked, method):
        with pytest.raises(ParamValueException):
            getattr(client.facilities, method)("")

        assert not mocked.calls

    def test_update_with_an_empty_facility_id_is_rejected(self, client, mocked):
        with pytest.raises(ParamValueException):
            client.facilities.update_facility("", **FACILITY)

        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.POST, FACILITIES_V5, json={"errors": ["The address field is required."]}, status=406)

        assert client.facilities.create_facility(**FACILITY) == {"errors": ["The address field is required."]}


class TestNestedQuery:
    def test_plain_values_are_kept(self):
        assert nested_query({"page": 1, "search_query": "x"}) == {"page": 1, "search_query": "x"}

    def test_a_dict_becomes_bracketed_keys(self):
        assert nested_query({"filters": {"status": 1, "type": {"id": 2}}}) == {
            "filters[status]": 1,
            "filters[type][id]": 2,
        }

    def test_a_list_of_plain_values_becomes_a_bracketed_list(self):
        assert nested_query({"ids": ("A", "B")}) == {"ids[]": ["A", "B"]}

    def test_a_list_of_dicts_is_indexed(self):
        assert nested_query({"order_by": [{"name": "asc"}, ["date", "desc"]]}) == {
            "order_by[0][name]": "asc",
            "order_by[1][]": ["date", "desc"],
        }
