"""Smoke tests against the real Route4Me API.

**Deselected by default.** ``pyproject.toml`` sets ``-m "not live"``, and
``pytest-socket`` blocks outbound connections for the rest of the suite. These
run only in the nightly `live-smoke` workflow, or locally with:

    ROUTE4ME_API_KEY=<real key> pytest -m live

They exist so that a real API change is noticed, and deliberately assert
*shape* rather than content -- an account's route list is not stable, so
asserting on specific routes would produce a permanently flaky job. Failures
here are informational; the workflow is ``continue-on-error``.

This is what replaced the two tests that used to hit the API with a dummy key
during every ordinary test run and fail every time.
"""

import os

import pytest

from route4me import Route4Me

pytestmark = [
    pytest.mark.live,
    # pytest-socket is armed globally; these tests are the exception.
    pytest.mark.enable_socket,
]

API_KEY = os.environ.get("ROUTE4ME_API_KEY")

requires_key = pytest.mark.skipif(
    not API_KEY,
    reason="ROUTE4ME_API_KEY is not set",
)


@pytest.fixture(scope="module")
def live_client():
    return Route4Me(API_KEY)


def _assert_not_an_error(payload, what):
    """Fail with the API's own message rather than an opaque shape error."""
    if isinstance(payload, dict) and "errors" in payload:
        pytest.fail(f"{what} returned an API error: {payload['errors']}")


@requires_key
def test_get_routes(live_client):
    result = live_client.route.get_routes(limit=1, offset=0)

    _assert_not_an_error(result, "get_routes")
    assert isinstance(result, list)
    if result:
        assert "route_id" in result[0]


@requires_key
def test_get_vehicles(live_client):
    result = live_client.vehicles.get_vehicles()

    _assert_not_an_error(result, "get_vehicles")
    assert isinstance(result, list)
    if result:
        assert "vehicle_id" in result[0]


@requires_key
def test_get_territories(live_client):
    result = live_client.territory.get_territories()

    _assert_not_an_error(result, "get_territories")
    assert isinstance(result, list)


@requires_key
def test_an_invalid_key_is_rejected():
    """The error contract holds against the real API, not just mocks."""
    result = Route4Me("0" * 32).route.get_routes(limit=1, offset=0)

    assert isinstance(result, dict)
    assert "errors" in result
