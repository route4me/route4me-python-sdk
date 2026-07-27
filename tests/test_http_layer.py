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
from route4me.exceptions import APIException

ANY_URL = ROUTE_HOST


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

    @pytest.mark.xfail(
        strict=True,
        reason="Phase 4: HEADERS is a mutable module-level dict used as a default "
        "argument, so every client shares one object. Remove this marker when "
        "the constructor copies it.",
    )
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

    @pytest.mark.xfail(
        strict=True,
        reason="Phase 4: the API key currently leaks through APIException.url. "
        "Remove this marker once URLs are redacted.",
    )
    def test_api_key_is_not_in_the_exception_string(self, client, mocked, api_key):
        mocked.add(responses.GET, ANY_URL, json={"errors": ["bad key"]}, status=401)

        with pytest.raises(APIException) as excinfo:
            client.route.get_routes(limit=1, offset=0)

        rendered = f"{excinfo.value!s} {excinfo.value!r} {excinfo.value.args}"
        assert api_key not in rendered

    @pytest.mark.xfail(
        strict=True,
        reason="Phase 4: APIException.url is the raw resolved URL. Remove this marker once it holds the redacted form.",
    )
    def test_api_key_is_not_in_the_exception_url_attribute(self, client, mocked, api_key):
        mocked.add(responses.GET, ANY_URL, json={"errors": ["bad key"]}, status=401)

        with pytest.raises(APIException) as excinfo:
            client.route.get_routes(limit=1, offset=0)

        assert api_key not in excinfo.value.url


class TestTimeouts:
    @pytest.mark.xfail(
        strict=True,
        reason="Phase 4: no timeout is passed to requests, so a stalled socket "
        "hangs the caller forever. Remove this marker once a default lands.",
    )
    def test_requests_carry_a_default_timeout(self, client, mocked):
        """Captured via the adapter, since ``responses`` records the prepared
        request but not the send kwargs."""
        captured = {}
        original = client._request_get

        def spy(url, request_params, **kwargs):
            captured.update(kwargs)
            return original(url, request_params, **kwargs)

        mocked.add(responses.GET, ANY_URL, json={}, status=200)
        client._request_get = spy
        client._make_request(ANY_URL, {}, client._request_get)

        assert captured.get("timeout") is not None


class TestParamsMutation:
    @pytest.mark.xfail(
        strict=True,
        reason="Phase 5: _make_request mutates the caller's params dict. Every "
        "resource passes its long-lived self.params, so query params accumulate "
        "across calls. Remove this marker once the dict is copied.",
    )
    def test_make_request_does_not_mutate_the_callers_params(self, client, mocked):
        mocked.add(responses.GET, ANY_URL, json={}, status=200)
        params = {"limit": 1}

        client._make_request(ANY_URL, params, client._request_get)

        assert params == {"limit": 1}, "api_key was written into the caller's dict"
