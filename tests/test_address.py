"""Request-level tests for the :class:`route4me.address.Address` methods added in 1.0.0.

Moving, deleting and marking the destinations of routes. The other methods are
covered in ``tests/test_optimization_address.py``.
"""

from urllib.parse import parse_qs

import pytest
import responses

from route4me.api_endpoints import (
    DELETE_ROUTE_DESTINATION,
    MARK_ADDRESS_DEPARTED,
    MARK_ADDRESS_VISITED,
    MOVE_ROUTE_DESTINATION,
)
from route4me.exceptions import ParamValueException

ROUTE_ID = "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"
OTHER_ROUTE_ID = "BADC0DE0BADC0DE0BADC0DE0BADC0DE0"
DESTINATION_ID = 98765


def form_of(request):
    """Decode a form-encoded request body into single values."""
    return {k: v[0] for k, v in parse_qs(request.body).items()}


class TestMoveDestinationToRoute:
    def test_posts_a_form(self, client, mocked, last_request, query_of, api_key):
        mocked.add(responses.POST, MOVE_ROUTE_DESTINATION, json={"success": True}, status=200)

        result = client.address.move_destination_to_route(OTHER_ROUTE_ID, DESTINATION_ID, after_destination_id=12345)

        assert result == {"success": True}
        request = last_request()
        assert request.method == "POST"
        assert query_of(request) == {"api_key": api_key}
        assert request.headers["Content-Type"] == "application/x-www-form-urlencoded"
        assert form_of(request) == {
            "to_route_id": OTHER_ROUTE_ID,
            "route_destination_id": str(DESTINATION_ID),
            "after_destination_id": "12345",
        }

    def test_the_position_is_optional(self, client, mocked, last_request):
        mocked.add(responses.POST, MOVE_ROUTE_DESTINATION, json={"success": True}, status=200)

        client.address.move_destination_to_route(OTHER_ROUTE_ID, DESTINATION_ID)

        assert form_of(last_request()) == {"to_route_id": OTHER_ROUTE_ID, "route_destination_id": str(DESTINATION_ID)}

    @pytest.mark.parametrize(
        ("args", "missing"),
        [(("", DESTINATION_ID), "to_route_id"), ((OTHER_ROUTE_ID, None), "route_destination_id")],
    )
    def test_requires_the_route_and_the_destination(self, client, mocked, args, missing):
        with pytest.raises(ParamValueException) as raised:
            client.address.move_destination_to_route(*args)

        assert raised.value.param == missing
        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked, load_fixture):
        mocked.add(responses.POST, MOVE_ROUTE_DESTINATION, json=load_fixture("error_v4"), status=401)

        result = client.address.move_destination_to_route(OTHER_ROUTE_ID, DESTINATION_ID)

        assert result == {"errors": ["The API key is invalid."]}


class TestDeleteRouteDestinations:
    def test_posts_the_ids_comma_separated(self, client, mocked, last_request, query_of, api_key):
        mocked.add(responses.POST, DELETE_ROUTE_DESTINATION, json={"deleted": True}, status=200)

        assert client.address.delete_route_destinations([DESTINATION_ID, 98766]) == {"deleted": True}
        request = last_request()
        assert request.method == "POST"
        assert query_of(request) == {"api_key": api_key, "format": "json"}
        assert form_of(request) == {"route_destination_ids": "98765,98766"}

    @pytest.mark.parametrize("ids", [DESTINATION_ID, str(DESTINATION_ID)])
    def test_takes_one_id(self, client, mocked, last_request, ids):
        mocked.add(responses.POST, DELETE_ROUTE_DESTINATION, json={"deleted": True}, status=200)

        client.address.delete_route_destinations(ids)

        assert form_of(last_request()) == {"route_destination_ids": "98765"}

    @pytest.mark.parametrize("ids", [[], ""])
    def test_requires_an_id(self, client, mocked, ids):
        with pytest.raises(ParamValueException) as raised:
            client.address.delete_route_destinations(ids)

        assert raised.value.param == "route_destination_ids"
        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked, load_fixture):
        mocked.add(responses.POST, DELETE_ROUTE_DESTINATION, json=load_fixture("error_v4"), status=401)

        assert client.address.delete_route_destinations([DESTINATION_ID]) == {"errors": ["The API key is invalid."]}


class TestMarkAddress:
    def test_mark_address_departed_is_a_get(self, client, mocked, last_request, query_of, api_key):
        mocked.add(responses.GET, MARK_ADDRESS_DEPARTED, json={"status": True}, status=200)

        result = client.address.mark_address_departed(ROUTE_ID, DESTINATION_ID, member_id=1, utc_time=1792600000)

        assert result == {"status": True}
        assert last_request().method == "GET"
        assert last_request().body is None
        assert query_of(last_request()) == {
            "api_key": api_key,
            "route_id": ROUTE_ID,
            "address_id": str(DESTINATION_ID),
            "is_departed": "1",
            "member_id": "1",
            "utc_time": "1792600000",
        }

    def test_mark_address_visited_is_a_put(self, client, mocked, last_request, query_of, api_key):
        mocked.add(responses.PUT, MARK_ADDRESS_VISITED, json={"status": True}, status=200)

        client.address.mark_address_visited(ROUTE_ID, DESTINATION_ID, lat=40.7, lng=-73.9)

        assert last_request().method == "PUT"
        assert query_of(last_request()) == {
            "api_key": api_key,
            "route_id": ROUTE_ID,
            "address_id": str(DESTINATION_ID),
            "is_visited": "1",
            "lat": "40.7",
            "lng": "-73.9",
        }

    @pytest.mark.parametrize(
        ("method", "endpoint", "http_method", "flag"),
        [
            ("mark_address_departed", MARK_ADDRESS_DEPARTED, responses.GET, "is_departed"),
            ("mark_address_visited", MARK_ADDRESS_VISITED, responses.PUT, "is_visited"),
        ],
    )
    def test_false_clears_the_mark(self, client, mocked, last_request, query_of, method, endpoint, http_method, flag):
        mocked.add(http_method, endpoint, json={"status": True}, status=200)

        getattr(client.address, method)(ROUTE_ID, DESTINATION_ID, False)

        assert query_of(last_request())[flag] == "0"

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked, load_fixture):
        mocked.add(responses.PUT, MARK_ADDRESS_VISITED, json=load_fixture("error_v4"), status=401)

        assert client.address.mark_address_visited(ROUTE_ID, DESTINATION_ID) == {"errors": ["The API key is invalid."]}
