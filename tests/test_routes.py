"""Route resource tests.

Previously this file made a real HTTPS call to ``api.route4me.com`` with the
dummy key and was documented as "fails by design". It now runs against
recorded payloads; the honest smoke coverage it was standing in for moved to
``tests/live/test_smoke.py``.

The old version also had a broken guard -- ``if hasattr(response, "errors")``
against a ``dict``, which is always ``False``, so the error branch it was
meant to take was dead and the test failed on the success branch instead.
"""

import pytest
import responses

from route4me.api_endpoints import ROUTE_HOST
from route4me.exceptions import ParamValueException

ROUTE_ID = "5B1E0EFBB8FF6D3A2F6F0BD2C0E60E1E"


class TestGetRoutes:
    def test_returns_the_route_list(self, client, mocked, load_fixture):
        mocked.add(responses.GET, ROUTE_HOST, json=load_fixture("routes_list"), status=200)

        result = client.route.get_routes(limit=1, offset=0)

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["route_id"] == ROUTE_ID

    def test_sends_limit_offset_and_api_key(self, client, mocked, load_fixture, query_of, last_request, api_key):
        mocked.add(responses.GET, ROUTE_HOST, json=load_fixture("routes_list"), status=200)

        client.route.get_routes(limit=1, offset=0)

        query = query_of(last_request())
        assert query["limit"] == "1"
        assert query["offset"] == "0"
        assert query["api_key"] == api_key

    def test_missing_required_params_raises(self, client):
        """``limit`` and ``offset`` are required; no HTTP call should happen."""
        with pytest.raises(ParamValueException):
            client.route.get_routes()

    def test_api_error_is_returned_not_raised(self, client, mocked, load_fixture):
        """The established contract: API errors come back as a dict."""
        mocked.add(responses.GET, ROUTE_HOST, json=load_fixture("error_v4"), status=401)

        result = client.route.get_routes(limit=1, offset=0)

        assert result == {"errors": ["The API key is invalid."]}


class TestGetRoute:
    def test_returns_a_single_route(self, client, mocked, load_fixture):
        mocked.add(responses.GET, ROUTE_HOST, json=load_fixture("route"), status=200)

        result = client.route.get_route(route_id=ROUTE_ID)

        assert result["route_id"] == ROUTE_ID
        assert result["addresses"][0]["alias"] == "Bergdorf Goodman"

    def test_sends_the_route_id(self, client, mocked, load_fixture, query_of, last_request):
        mocked.add(responses.GET, ROUTE_HOST, json=load_fixture("route"), status=200)

        client.route.get_route(route_id=ROUTE_ID)

        assert query_of(last_request())["route_id"] == ROUTE_ID

    def test_rejects_a_non_string_route_id(self, client):
        """``route_id`` is a ValidatedField of type ``str``."""
        with pytest.raises(ParamValueException):
            client.route.get_route(route_id=12345)
