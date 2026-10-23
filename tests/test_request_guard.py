"""Tests for the request guard in ``conftest.py``.

The guard checks every request the suite sends: https only, Route4Me hosts
only, registered endpoints only, and the API key only in the ``api_key`` query
parameter. These tests pin that behaviour so the guard cannot silently stop
guarding.
"""

from tests.conftest import API_KEY, check_request

V4_ROUTES = "https://api.route4me.com/api.v4/route.php"


def test_a_registered_https_endpoint_passes():
    assert check_request("GET", f"{V4_ROUTES}?api_key={API_KEY}", {}) == []


def test_plain_http_is_rejected():
    problems = check_request("GET", f"http://api.route4me.com/api.v4/route.php?api_key={API_KEY}", {})

    assert any("not https" in p for p in problems)


def test_a_foreign_host_is_rejected():
    problems = check_request("POST", f"https://example.com/collect?api_key={API_KEY}", {})

    assert any("not an allowed Route4Me host" in p for p in problems)


def test_an_unregistered_path_is_rejected():
    problems = check_request("GET", f"https://api.route4me.com/api.v4/no_such_endpoint.php?api_key={API_KEY}", {})

    assert any("not in tests/fixtures/endpoints.json" in p for p in problems)


def test_the_key_in_a_header_is_rejected():
    problems = check_request("GET", V4_ROUTES, {"X-Api-Key": API_KEY})

    assert any("outside the api_key query parameter" in p for p in problems)


def test_the_key_in_another_query_parameter_is_rejected():
    problems = check_request("GET", f"{V4_ROUTES}?api_key={API_KEY}&echo={API_KEY}", {})

    assert any("other than api_key" in p for p in problems)


def test_a_deprecated_endpoint_is_allowed():
    assert check_request("GET", f"https://rapid.route4me.com/street_data?api_key={API_KEY}", {}) == []
