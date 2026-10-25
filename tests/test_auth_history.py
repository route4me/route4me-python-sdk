"""Request-level tests for :class:`route4me.auth_history.AuthHistory`."""

import responses

from route4me.api_endpoints import AUTH_HISTORY_API_CONFIG_V5


class TestAuthHistory:
    def test_get_api_config(self, client, mocked, last_request, query_of):
        reply = {"api_capabilities": {"search": True}, "api_preferences": {"partial_load": False}}
        mocked.add(responses.GET, AUTH_HISTORY_API_CONFIG_V5, json=reply, status=200)

        assert client.auth_history.get_api_config() == reply
        assert last_request().method == "GET"
        assert last_request().url == AUTH_HISTORY_API_CONFIG_V5
        assert query_of(last_request()) == {}

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        error = {"status": False, "code": 401, "exit_code": 1, "messages": ["Unauthenticated"]}
        mocked.add(responses.GET, AUTH_HISTORY_API_CONFIG_V5, json=error, status=401)

        assert client.auth_history.get_api_config() == {"errors": ["Unauthenticated"]}
