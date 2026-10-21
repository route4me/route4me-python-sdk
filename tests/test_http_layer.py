"""Tests for the HTTP layer in ``route4me/api.py``.

This layer had no direct coverage at all -- it was exercised only incidentally
by the two tests that called the real API. It is where the API key is
attached, where non-2xx becomes :class:`APIException`, and where every
resource module's request is actually issued, so it is worth testing directly.

Several tests here pin behaviour that is *currently wrong* and record what it
should become; each is marked ``xfail(strict=True)`` and names the phase that
fixes it. Strict xfail means that when the fix lands, the test starts failing
as XPASS and forces the marker to be removed -- the fix cannot land silently.
"""

import json

import pytest
import responses

from route4me import Route4Me
from route4me.api import HEADERS
from route4me.api_endpoints import ROUTE_HOST, TERRITORY_HOST
from route4me.config import DEFAULT_TIMEOUT, Route4MeConfig
from route4me.exceptions import APIException

ANY_URL = ROUTE_HOST


class _StopSend(Exception):
    """Raised by the spies below to abort once the kwargs are captured."""


class TestApiKeyInjection:
    def test_api_key_is_sent_as_a_query_parameter(self, client, mocked, query_of, last_request, api_key):
        """V4 authenticates by query string. This is the invariant the deleted
        ``test_api_key`` tautology was gesturing at but never checked."""
        mocked.add(responses.GET, ANY_URL, json=[], status=200)

        client.route.get_routes(limit=1, offset=0)

        assert query_of(last_request())["api_key"] == api_key

    def test_api_key_is_injected_even_when_absent_from_params(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.GET, ANY_URL, json={}, status=200)

        client._make_request(ANY_URL, {}, client._request_get)

        assert query_of(last_request())["api_key"] == api_key


class TestStatusHandling:
    @pytest.mark.parametrize("status", [200, 201, 204, 301, 302, 399])
    def test_2xx_and_3xx_are_returned(self, client, mocked, status):
        # A 204 must not carry a body; current urllib3 rejects one.
        if status == 204:
            mocked.add(responses.GET, ANY_URL, body=b"", status=status)
        else:
            mocked.add(responses.GET, ANY_URL, json={}, status=status)

        response = client._make_request(ANY_URL, {}, client._request_get)

        assert response.status_code == status

    @pytest.mark.parametrize("status", [400, 401, 403, 404, 422, 429, 500, 502, 503])
    def test_4xx_and_5xx_raise_api_exception(self, client, mocked, status):
        mocked.add(responses.GET, ANY_URL, json={"errors": ["nope"]}, status=status)

        with pytest.raises(APIException) as excinfo:
            client._make_request(ANY_URL, {}, client._request_get)

        assert excinfo.value.get_status_code() == status
        assert excinfo.value.to_dict() == {"errors": ["nope"]}

    def test_non_json_error_body_degrades_gracefully(self, client, mocked):
        """A 500 returning an HTML error page must not blow up ``to_dict()``."""
        mocked.add(responses.GET, ANY_URL, body="<html>Gateway Error</html>", status=500)

        with pytest.raises(APIException) as excinfo:
            client._make_request(ANY_URL, {}, client._request_get)

        assert excinfo.value.to_dict() == {"errors": "Unexpected server response"}


class TestVerbs:
    """Each ``_request_*`` helper issues the verb it claims."""

    @pytest.mark.parametrize(
        ("helper", "expected", "registered"),
        [
            ("_request_get", "GET", responses.GET),
            ("_request_post", "POST", responses.POST),
            ("_request_put", "PUT", responses.PUT),
            ("_request_delete", "DELETE", responses.DELETE),
        ],
    )
    def test_verb(self, client, mocked, last_request, helper, expected, registered):
        mocked.add(registered, ANY_URL, json={}, status=200)

        getattr(client, helper)(ANY_URL, {"api_key": "k"})

        assert last_request().method == expected

    def test_post_sends_a_json_body(self, client, mocked, last_request):
        mocked.add(responses.POST, TERRITORY_HOST, json={}, status=200)

        client._request_post(TERRITORY_HOST, {}, json={"territory_name": "X"})

        assert json.loads(last_request().body) == {"territory_name": "X"}

    def test_put_sends_a_json_body(self, client, mocked, last_request):
        mocked.add(responses.PUT, TERRITORY_HOST, json={}, status=200)

        client._request_put(TERRITORY_HOST, {}, json={"territory_name": "X"})

        assert json.loads(last_request().body) == {"territory_name": "X"}


class TestClientConfiguration:
    def test_default_headers_are_sent(self, client, mocked, last_request):
        mocked.add(responses.GET, ANY_URL, json={}, status=200)

        client._request_get(ANY_URL, {})

        sent = last_request().headers
        assert sent["User-Agent"] == "Route4Me Python SDK"

    def test_custom_headers_override_the_defaults(self, mocked, last_request):
        client = Route4Me("k" * 32, headers={"User-Agent": "custom/1.0"})
        mocked.add(responses.GET, ANY_URL, json={}, status=200)

        client._request_get(ANY_URL, {})

        assert last_request().headers["User-Agent"] == "custom/1.0"

    def test_verify_ssl_defaults_to_on(self):
        assert Route4Me("k" * 32).verify_ssl is True

    def test_proxies_default_to_an_empty_dict_not_none(self):
        """A ``None`` default would be a mutable-default hazard and would also
        break ``requests``, which expects a mapping."""
        assert Route4Me("k" * 32).proxies == {}

    def test_clients_do_not_share_one_headers_dict(self):
        first = Route4Me("a" * 32)
        second = Route4Me("b" * 32)

        first.headers["X-Test"] = "leaked"

        assert "X-Test" not in second.headers
        assert "X-Test" not in HEADERS


class TestApiKeyLeakage:
    """The API key must not escape into anything that gets logged.

    ``requests`` resolves ``Response.url`` to the fully expanded request URL,
    which for V4 carries ``?api_key=<plaintext>``. ``api.py`` passes that into
    ``APIException``, which puts it in ``Exception.args`` -- so it shows up in
    ``str(exc)``, ``repr(exc)``, and every traceback frame, and gets shipped
    verbatim to Sentry, Datadog and any other log aggregator.
    """

    @staticmethod
    def _raise(client, mocked, body=None):
        """Trigger a real ``APIException`` through the transport.

        Note this goes through ``_make_request`` rather than a resource method:
        resource methods catch ``APIException`` and return ``e.to_dict()``, so
        ``pytest.raises`` would never see anything.
        """
        mocked.add(responses.GET, ANY_URL, json=body or {"errors": ["bad key"]}, status=401)
        with pytest.raises(APIException) as excinfo:
            client._make_request(ANY_URL, {"limit": 1}, client._request_get)
        return excinfo.value

    def test_api_key_is_not_in_the_exception_string(self, client, mocked, api_key):
        exc = self._raise(client, mocked)

        rendered = f"{exc!s} {exc!r} {exc.args}"
        assert api_key not in rendered

    def test_api_key_is_not_in_the_exception_url_attribute(self, client, mocked, api_key):
        exc = self._raise(client, mocked)

        assert api_key not in exc.url
        assert "REDACTED" in exc.url

    def test_the_endpoint_is_still_identifiable_after_redaction(self, client, mocked):
        """Redaction must not destroy the diagnostic value of the URL."""
        exc = self._raise(client, mocked)

        assert exc.url.startswith("https://api.route4me.com/api.v4/route.php")
        assert "limit=1" in exc.url

    def test_the_raw_url_is_not_retained_anywhere_on_the_instance(self, client, mocked, api_key):
        """A private attribute would still escape via ``vars()``, ``pickle``
        and any error reporter that serialises exception attributes."""
        exc = self._raise(client, mocked)

        for value in vars(exc).values():
            assert api_key not in str(value)

    def test_the_api_key_is_scrubbed_from_the_response_body(self, client, mocked, api_key):
        """Several V4 endpoints echo the request parameters back in errors."""
        exc = self._raise(client, mocked, body={"errors": [f"key {api_key} is invalid"]})

        assert api_key not in exc.response
        assert api_key not in str(exc.to_dict())

    def test_redaction_can_be_disabled_for_debugging(self, client, mocked, api_key, monkeypatch):
        monkeypatch.setattr(Route4MeConfig, "redact_urls", False)

        exc = self._raise(client, mocked)

        assert api_key in exc.url


class TestTimeouts:
    """Every request must carry a timeout.

    ``requests`` defaults to *no* timeout, so before 0.2.0 a stalled socket
    blocked the calling thread forever -- the highest-impact defect for anyone
    embedding the SDK in a server.

    The timeout is resolved inside each ``_request_*`` helper, and ``responses``
    records the prepared request but not the send kwargs, so these assert
    against the ``requests`` entry points directly.
    """

    @staticmethod
    def _capture_timeout(monkeypatch):
        """Record the ``timeout`` kwarg that reaches the transport.

        Patches ``requests.Session.request`` -- since 0.3.0 every call is
        issued through a pooled session, not the module-level helpers.
        """
        captured = {}

        def spy(self, method, url, **kwargs):
            captured["timeout"] = kwargs.get("timeout", "NOT PASSED")
            captured["method"] = method
            raise _StopSend

        monkeypatch.setattr("requests.sessions.Session.request", spy)
        return captured

    @pytest.mark.parametrize(
        ("helper", "verb"),
        [
            ("_request_get", "GET"),
            ("_request_post", "POST"),
            ("_request_put", "PUT"),
            ("_request_delete", "DELETE"),
        ],
    )
    def test_every_verb_passes_a_timeout(self, client, monkeypatch, helper, verb):
        captured = self._capture_timeout(monkeypatch)

        with pytest.raises(_StopSend):
            getattr(client, helper)(ANY_URL, {})

        assert captured["timeout"] == DEFAULT_TIMEOUT
        assert captured["method"] == verb

    def test_the_default_is_a_connect_read_pair(self):
        """A scalar would make a blackholed SYN cost the full read timeout."""
        assert DEFAULT_TIMEOUT == (6.05, 30.0)

    def test_a_constructor_timeout_overrides_the_default(self, monkeypatch):
        client = Route4Me("k" * 32, timeout=5)
        captured = self._capture_timeout(monkeypatch)

        with pytest.raises(_StopSend):
            client._request_get(ANY_URL, {})

        assert captured["timeout"] == 5.0

    def test_a_per_call_timeout_wins_over_the_constructor(self, monkeypatch):
        client = Route4Me("k" * 32, timeout=5)
        captured = self._capture_timeout(monkeypatch)

        with pytest.raises(_StopSend):
            client._request_get(ANY_URL, {}, timeout=(1, 2))

        assert captured["timeout"] == (1.0, 2.0)

    def test_none_restores_the_pre_0_2_0_unbounded_behaviour(self, monkeypatch):
        """An explicit, greppable opt-out."""
        client = Route4Me("k" * 32, timeout=None)
        captured = self._capture_timeout(monkeypatch)

        with pytest.raises(_StopSend):
            client._request_get(ANY_URL, {})

        assert captured["timeout"] is None

    def test_the_global_config_is_the_last_fallback(self, client, monkeypatch):
        monkeypatch.setattr(Route4MeConfig, "timeout", 12)
        captured = self._capture_timeout(monkeypatch)

        with pytest.raises(_StopSend):
            client._request_get(ANY_URL, {})

        assert captured["timeout"] == 12.0

    @pytest.mark.parametrize("bad", [0, -1, "30", (1,), (1, 2, 3), (0, 5), True, object()])
    def test_an_invalid_timeout_is_rejected_at_construction(self, bad):
        """Fail where the mistake is, not on the first request."""
        with pytest.raises(ValueError):
            Route4Me("k" * 32, timeout=bad)


class TestParamsMutation:
    def test_make_request_does_not_mutate_the_callers_params(self, client, mocked):
        mocked.add(responses.GET, ANY_URL, json={}, status=200)
        params = {"limit": 1}

        client._make_request(ANY_URL, params, client._request_get)

        assert params == {"limit": 1}, "api_key was written into the caller's dict"
