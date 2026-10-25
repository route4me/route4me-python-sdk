"""Request-level tests for the :class:`route4me.route.Route` methods added in 1.0.0.

:meth:`~route4me.route.Route.rename_route`, and the query keywords of
:meth:`~route4me.route.Route.update_route`. The other methods are covered in
``tests/test_route_resource.py``.
"""

import json
from urllib.parse import parse_qs

import pytest
import responses

from route4me.api_endpoints import RENAME_ROUTE, ROUTE_HOST
from route4me.exceptions import ParamValueException

ROUTE_ID = "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"


class TestUpdateRouteQuery:
    def test_reoptimize_goes_in_the_query(self, client, mocked, last_request, query_of, api_key):
        mocked.add(responses.PUT, ROUTE_HOST, json={"route_id": ROUTE_ID}, status=200)

        result = client.route.update_route({}, ROUTE_ID, reoptimize=1, remaining=1)

        assert result == {"route_id": ROUTE_ID}
        assert last_request().method == "PUT"
        assert query_of(last_request()) == {
            "api_key": api_key,
            "route_id": ROUTE_ID,
            "reoptimize": "1",
            "remaining": "1",
        }
        assert json.loads(last_request().body) == {}

    def test_recompute_directions_goes_in_the_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.PUT, ROUTE_HOST, json={"route_id": ROUTE_ID}, status=200)

        client.route.update_route({"parameters": {"route_name": "Monday"}}, ROUTE_ID, recompute_directions=1)

        assert query_of(last_request())["recompute_directions"] == "1"
        assert json.loads(last_request().body) == {"parameters": {"route_name": "Monday"}}

    def test_query_keywords_do_not_leak_into_the_next_call(self, client, mocked, last_request, query_of, api_key):
        mocked.add(responses.PUT, ROUTE_HOST, json={}, status=200)
        client.route.update_route({}, ROUTE_ID, reoptimize=1)

        client.route.update_route({}, ROUTE_ID)

        assert query_of(last_request()) == {"api_key": api_key, "route_id": ROUTE_ID}

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked, load_fixture):
        mocked.add(responses.PUT, ROUTE_HOST, json=load_fixture("error_v4"), status=401)

        assert client.route.update_route({}, ROUTE_ID, reoptimize=1) == {"errors": ["The API key is invalid."]}


class TestRenameRoute:
    def test_posts_a_form(self, client, mocked, last_request, query_of, api_key):
        mocked.add(responses.POST, RENAME_ROUTE, json={"status": True}, status=200)

        assert client.route.rename_route(ROUTE_ID, "Monday North") == {"status": True}
        request = last_request()
        assert request.method == "POST"
        assert query_of(request) == {"api_key": api_key, "format": "json"}
        assert request.headers["Content-Type"] == "application/x-www-form-urlencoded"
        assert parse_qs(request.body) == {"route_id": [ROUTE_ID], "route_name": ["Monday North"]}

    @pytest.mark.parametrize(
        ("args", "missing"),
        [(("", "Monday"), "route_id"), ((ROUTE_ID, ""), "route_name"), ((None, None), "route_id, route_name")],
    )
    def test_requires_an_id_and_a_name(self, client, mocked, args, missing):
        with pytest.raises(ParamValueException) as raised:
            client.route.rename_route(*args)

        assert raised.value.param == missing
        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked, load_fixture):
        mocked.add(responses.POST, RENAME_ROUTE, json=load_fixture("error_v4"), status=401)

        assert client.route.rename_route(ROUTE_ID, "Monday") == {"errors": ["The API key is invalid."]}
