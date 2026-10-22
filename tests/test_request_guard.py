"""Tests for the request guard in ``conftest.py``.

The guard checks every request the suite sends: https only, Route4Me hosts
only, registered endpoints only, and the API key only in the ``api_key`` query
parameter. These tests pin that behaviour so the guard cannot silently stop
guarding.
"""

import pytest

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

    assert any("outside its expected place" in p for p in problems)


V5_STATUS = "https://wh.route4me.com/modules/api/v5.0/route-status/ABC"


def test_a_v5_request_with_a_bearer_token_passes():
    assert check_request("GET", V5_STATUS, {"Authorization": f"Bearer {API_KEY}"}) == []


def test_a_v5_request_with_the_key_in_the_url_is_rejected():
    problems = check_request("GET", f"{V5_STATUS}?api_key={API_KEY}", {"Authorization": f"Bearer {API_KEY}"})

    assert any("instead of a bearer token" in p for p in problems)


def test_a_v5_request_without_a_bearer_token_is_rejected():
    problems = check_request("GET", V5_STATUS, {})

    assert any("lacks the bearer token" in p for p in problems)


def test_the_key_in_another_query_parameter_is_rejected():
    problems = check_request("GET", f"{V4_ROUTES}?api_key={API_KEY}&echo={API_KEY}", {})

    assert any("other than api_key" in p for p in problems)


def test_a_deprecated_endpoint_is_allowed_without_the_key():
    assert check_request("GET", "https://rapid.route4me.com/street_data", {}) == []


@pytest.mark.parametrize(
    "url",
    [
        f"https://rapid.route4me.com/street_data?api_key={API_KEY}",
        f"https://telematics.route4me.com/api/vendors.php?api_key={API_KEY}",
    ],
)
def test_the_key_is_rejected_on_any_other_host_even_a_deprecated_one(url):
    """The PHP SDK once sent its key to a retired host; the guard forbids that class."""
    problems = check_request("GET", url, {})

    assert any("not an API host" in p for p in problems)
