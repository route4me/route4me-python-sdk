"""Request-level tests for :class:`route4me.drivers.Drivers`."""

import responses

from route4me.api_endpoints import VIEW_DRIVERS


class TestDrivers:
    def test_get_drivers(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, VIEW_DRIVERS, json=[{"member_id": 7}], status=200)

        assert client.drivers.get_drivers(limit=10) == [{"member_id": 7}]
        assert last_request().method == "GET"
        assert last_request().url.split("?")[0] == VIEW_DRIVERS
        assert query_of(last_request()) == {"api_key": client.key, "limit": "10"}

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked, load_fixture):
        mocked.add(responses.GET, VIEW_DRIVERS, json=load_fixture("error_v4"), status=401)

        assert client.drivers.get_drivers() == {"errors": ["The API key is invalid."]}
