"""Request-level tests for :class:`route4me.autocomplete.Autocomplete`."""

import responses

from route4me.api_endpoints import AUTOCOMPLETE


class TestAutocomplete:
    def test_autocomplete_address_sends_the_keywords_as_the_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, AUTOCOMPLETE, json={"status": "OK", "results": 1}, status=200)

        # The parameter names are undocumented; any keyword goes through as given.
        assert client.autocomplete.autocomplete_address(param_a="1 Example") == {"status": "OK", "results": 1}
        assert last_request().method == "GET"
        assert last_request().url.split("?")[0] == AUTOCOMPLETE
        assert query_of(last_request()) == {"api_key": client.key, "param_a": "1 Example"}

    def test_a_plain_text_reply_is_returned_raw(self, client, mocked):
        mocked.add(responses.GET, AUTOCOMPLETE, body=b"No address specified", status=200)

        assert client.autocomplete.autocomplete_address() == b"No address specified"

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked, load_fixture):
        mocked.add(responses.GET, AUTOCOMPLETE, json=load_fixture("error_v4"), status=401)

        assert client.autocomplete.autocomplete_address() == {"errors": ["The API key is invalid."]}
