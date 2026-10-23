"""Request-level tests for :class:`route4me.account_profile.AccountProfile`."""

import responses

from route4me.api_endpoints import ACCOUNT_PROFILE_V5


class TestAccountProfile:
    def test_get_account_profile(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, ACCOUNT_PROFILE_V5, json={"member_id": 1, "root_member_id": 1}, status=200)

        assert client.account_profile.get_account_profile() == {"member_id": 1, "root_member_id": 1}
        assert last_request().method == "GET"
        assert last_request().url == ACCOUNT_PROFILE_V5
        assert query_of(last_request()) == {}

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        error = {"status": False, "code": 401, "exit_code": 1, "messages": ["Unauthenticated"]}
        mocked.add(responses.GET, ACCOUNT_PROFILE_V5, json=error, status=401)

        assert client.account_profile.get_account_profile() == {"errors": ["Unauthenticated"]}
