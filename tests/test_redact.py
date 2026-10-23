"""Tests for ``route4me/_redact.py``.

The contract these enforce is unusual and worth stating: **no function in
_redact may raise.** They run on the error path, so a redactor that throws
converts a plain 401 into a traceback originating inside the SDK -- and worse,
if it throws *before* redacting, the credential escapes anyway.
"""

import pytest
from requests.structures import CaseInsensitiveDict

from route4me._redact import (
    REDACTED,
    SENSITIVE_HEADERS,
    SENSITIVE_PARAMS,
    redact_headers,
    redact_params,
    redact_text,
    redact_url,
)

KEY = "1" * 32


class TestRedactUrl:
    def test_replaces_the_api_key_value(self):
        result = redact_url(f"https://api.route4me.com/api.v4/route.php?api_key={KEY}&limit=1")

        assert KEY not in result
        assert REDACTED in result

    def test_preserves_host_path_and_innocuous_params(self):
        result = redact_url(f"https://api.route4me.com/api.v4/route.php?api_key={KEY}&limit=1&offset=0")

        assert result.startswith("https://api.route4me.com/api.v4/route.php")
        assert "limit=1" in result
        assert "offset=0" in result

    def test_the_marker_is_url_safe(self):
        """A marker needing percent-encoding would come back out of urlencode
        as %2A%2A%2A..., which is unreadable in exactly the place it matters."""
        result = redact_url(f"https://h/x?api_key={KEY}")

        assert f"api_key={REDACTED}" in result
        assert "%" not in result

    def test_a_url_without_a_query_string_is_untouched(self):
        url = "https://api.route4me.com/api.v4/route.php"
        assert redact_url(url) == url

    @pytest.mark.parametrize("param", sorted(SENSITIVE_PARAMS))
    def test_every_declared_sensitive_param_is_redacted(self, param):
        result = redact_url(f"https://h/x?{param}=secretvalue123")

        assert "secretvalue123" not in result

    def test_matching_is_case_insensitive(self):
        result = redact_url(f"https://h/x?API_KEY={KEY}&Api-Key={KEY}")

        assert KEY not in result

    @pytest.mark.parametrize("param", ["organization_api_key", "device_token", "client_secret", "new_password"])
    def test_credential_like_names_are_redacted(self, param):
        """V5 member-configuration-settings takes ``organization_api_key`` in
        the query; a name is redacted by its ending as well as by the list."""
        result = redact_url(f"https://h/x?{param}=secretvalue123&config_key=visible")

        assert "secretvalue123" not in result
        assert "config_key=visible" in result

    def test_repeated_params_are_all_redacted(self):
        result = redact_url(f"https://h/x?api_key={KEY}&api_key={KEY}")

        assert KEY not in result

    @pytest.mark.parametrize("value", [None, "", 12345, object()])
    def test_non_string_input_is_passed_through_without_raising(self, value):
        assert redact_url(value) == value

    def test_an_unparseable_url_still_drops_its_query_string(self):
        """Fallback path: if it cannot be parsed, discard everything after '?'
        rather than risk leaking a credential we failed to identify."""
        result = redact_url("http://[not-a-valid-host?api_key=" + KEY)

        assert KEY not in result


class TestRedactText:
    def test_replaces_the_secret(self):
        result = redact_text(f'{{"errors":["key {KEY} is invalid"]}}', KEY)

        assert KEY not in result
        assert REDACTED in result

    def test_replaces_multiple_occurrences(self):
        assert redact_text(f"{KEY} and {KEY}", KEY).count(REDACTED) == 2

    def test_accepts_several_secrets(self):
        other = "b" * 20
        result = redact_text(f"{KEY} {other}", KEY, other)

        assert KEY not in result
        assert other not in result

    @pytest.mark.parametrize("short", ["a", "ab", "abc", "1234567"])
    def test_short_secrets_are_ignored(self, short):
        """Replacing a 1-3 character string would shred the body without
        protecting anything meaningful."""
        body = f"the value {short} appears here"
        assert redact_text(body, short) == body

    @pytest.mark.parametrize("value", [None, "", 123])
    def test_non_string_input_is_passed_through(self, value):
        assert redact_text(value, KEY) == value

    def test_a_none_secret_is_skipped(self):
        assert redact_text("body", None) == "body"


class TestRedactHeaders:
    def test_redacts_authorization(self):
        result = redact_headers({"Authorization": "Bearer abc123", "Accept": "*/*"})

        assert result["Authorization"] == REDACTED
        assert result["Accept"] == "*/*"

    @pytest.mark.parametrize("header", sorted(SENSITIVE_HEADERS))
    def test_every_declared_sensitive_header_is_redacted(self, header):
        assert redact_headers({header: "secret"})[header] == REDACTED

    def test_matching_is_case_insensitive(self):
        assert redact_headers({"AUTHORIZATION": "x"})["AUTHORIZATION"] == REDACTED

    def test_empty_input_yields_an_empty_dict(self):
        assert redact_headers(None) == {}
        assert redact_headers({}) == {}

    def test_accepts_a_case_insensitive_dict(self):
        result = redact_headers(CaseInsensitiveDict({"Authorization": "x"}))

        assert result["Authorization"] == REDACTED


class TestRedactParams:
    def test_redacts_the_api_key(self):
        result = redact_params({"api_key": KEY, "limit": 1})

        assert result == {"api_key": REDACTED, "limit": 1}

    def test_redacts_credential_like_names(self):
        result = redact_params({"organization_api_key": KEY, "limit": 1})

        assert result == {"organization_api_key": REDACTED, "limit": 1}

    def test_empty_input_yields_an_empty_dict(self):
        assert redact_params(None) == {}


class TestTotality:
    """Nothing here may raise, whatever it is handed."""

    HOSTILE = [None, "", 0, [], {}, object(), b"bytes", 1.5, True]

    @pytest.mark.parametrize("value", HOSTILE)
    def test_redact_url_never_raises(self, value):
        redact_url(value)

    @pytest.mark.parametrize("value", HOSTILE)
    def test_redact_text_never_raises(self, value):
        redact_text(value, KEY)
        redact_text("body", value)

    @pytest.mark.parametrize("value", HOSTILE)
    def test_redact_headers_never_raises(self, value):
        redact_headers(value)

    @pytest.mark.parametrize("value", HOSTILE)
    def test_redact_params_never_raises(self, value):
        redact_params(value)
