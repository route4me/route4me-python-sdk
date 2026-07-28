"""Integration tests for the client's transport: pooling, retry, breaker, close.

``tests/test_resilience.py`` covers the retry primitives in isolation; these
verify they are actually *wired up*, so that every resource module -- and every
API V5 manager added later -- inherits them without knowing they exist.
"""

import pytest
import requests
import responses

from route4me import Route4Me
from route4me._resilience import CircuitBreakerOpen
from route4me.api_endpoints import ROUTE_HOST, TERRITORY_HOST
from route4me.config import Route4MeConfig


class TestSessionPooling:
    def test_a_session_is_created_and_reused(self, client):
        first = client.session

        assert isinstance(first, requests.Session)
        assert client.session is first, "a second access rebuilt the session"

    def test_an_https_adapter_is_mounted_for_pooling(self, client):
        adapter = client.session.get_adapter("https://wh.route4me.com/x")

        assert adapter is not None
        # Retries are handled in _resilience, not urllib3 -- see that module.
        assert adapter.max_retries.total == 0

    def test_pooling_can_be_disabled(self):
        assert Route4Me("k" * 32, use_session=False).session is None

    def test_an_injected_session_is_used_as_is(self):
        injected = requests.Session()

        assert Route4Me("k" * 32, session=injected).session is injected

    def test_requests_still_work_without_a_session(self, mocked):
        client = Route4Me("1" * 32, use_session=False)
        mocked.add(responses.GET, ROUTE_HOST, json=[], status=200)

        assert client.route.get_routes(limit=1, offset=0) == []


class TestLifecycle:
    def test_close_releases_the_session(self, client):
        assert client.session is not None  # force creation
        client.close()

        assert client._session is None

    def test_close_is_idempotent(self, client):
        assert client.session is not None
        client.close()
        client.close()  # must not raise

    def test_close_is_safe_when_pooling_is_disabled(self):
        Route4Me("k" * 32, use_session=False).close()

    def test_a_new_session_is_built_after_close(self, client):
        first = client.session
        client.close()

        assert client.session is not first

    def test_it_works_as_a_context_manager(self, mocked):
        mocked.add(responses.GET, ROUTE_HOST, json=[], status=200)

        with Route4Me("1" * 32) as client:
            client.route.get_routes(limit=1, offset=0)
            assert client._session is not None

        assert client._session is None

    def test_the_context_manager_does_not_swallow_exceptions(self):
        with pytest.raises(ValueError), Route4Me("k" * 32):
            raise ValueError("should propagate")


class TestRetryWiring:
    def test_retry_is_off_by_default(self, client, mocked):
        """Upgrading must not silently multiply the requests a service emits."""
        mocked.add(responses.GET, ROUTE_HOST, json={"errors": ["down"]}, status=503)

        client.route.get_routes(limit=1, offset=0)

        assert len(mocked.calls) == 1

    def test_a_503_is_retried_when_enabled(self, mocked, monkeypatch):
        monkeypatch.setattr("route4me._resilience.time.sleep", lambda _: None)
        client = Route4Me("1" * 32, retry_count=2, retry_initial_delay=0.001)
        mocked.add(responses.GET, ROUTE_HOST, json={"errors": ["down"]}, status=503)
        mocked.add(responses.GET, ROUTE_HOST, json={"errors": ["down"]}, status=503)
        mocked.add(responses.GET, ROUTE_HOST, json=[{"route_id": "R1"}], status=200)

        result = client.route.get_routes(limit=1, offset=0)

        assert result == [{"route_id": "R1"}]
        assert len(mocked.calls) == 3

    def test_a_400_is_not_retried(self, mocked, monkeypatch):
        monkeypatch.setattr("route4me._resilience.time.sleep", lambda _: None)
        client = Route4Me("1" * 32, retry_count=3, retry_initial_delay=0.001)
        mocked.add(responses.GET, ROUTE_HOST, json={"errors": ["bad"]}, status=400)

        result = client.route.get_routes(limit=1, offset=0)

        assert result == {"errors": ["bad"]}
        assert len(mocked.calls) == 1

    def test_a_post_is_not_retried(self, mocked, monkeypatch):
        """Replaying a create can duplicate server-side work."""
        monkeypatch.setattr("route4me._resilience.time.sleep", lambda _: None)
        client = Route4Me("1" * 32, retry_count=3, retry_initial_delay=0.001)
        mocked.add(responses.POST, TERRITORY_HOST, json={"errors": ["down"]}, status=503)

        client.territory.add_territory(
            territory_name="X",
            territory_color="ff0000",
            territory={"type": "circle", "data": ["0,0", "10"]},
        )

        assert len(mocked.calls) == 1

    def test_the_global_config_enables_retry(self, mocked, monkeypatch):
        monkeypatch.setattr("route4me._resilience.time.sleep", lambda _: None)
        monkeypatch.setattr(Route4MeConfig, "retry_count", 1)
        monkeypatch.setattr(Route4MeConfig, "retry_initial_delay", 0.001)
        client = Route4Me("1" * 32)
        mocked.add(responses.GET, ROUTE_HOST, json={"errors": ["down"]}, status=503)
        mocked.add(responses.GET, ROUTE_HOST, json=[], status=200)

        client.route.get_routes(limit=1, offset=0)

        assert len(mocked.calls) == 2

    def test_the_constructor_overrides_the_global(self, mocked, monkeypatch):
        monkeypatch.setattr(Route4MeConfig, "retry_count", 5)
        client = Route4Me("1" * 32, retry_count=0)
        mocked.add(responses.GET, ROUTE_HOST, json={"errors": ["down"]}, status=503)

        client.route.get_routes(limit=1, offset=0)

        assert len(mocked.calls) == 1

    def test_on_retry_is_invoked(self, mocked, monkeypatch):
        monkeypatch.setattr("route4me._resilience.time.sleep", lambda _: None)
        seen = []
        client = Route4Me("1" * 32, retry_count=1, retry_initial_delay=0.001, on_retry=lambda o, d, a: seen.append(a))
        mocked.add(responses.GET, ROUTE_HOST, json={"errors": ["down"]}, status=503)
        mocked.add(responses.GET, ROUTE_HOST, json=[], status=200)

        client.route.get_routes(limit=1, offset=0)

        assert seen == [1]


class TestCircuitBreakerWiring:
    def test_it_is_disabled_by_default(self, client):
        assert client.circuit_breaker is None

    def test_it_is_created_when_enabled(self):
        client = Route4Me("k" * 32, enable_circuit_breaker=True)

        breaker = client.circuit_breaker
        assert breaker is not None
        assert client.circuit_breaker is breaker, "a second access rebuilt the breaker"

    def test_thresholds_are_honoured(self):
        client = Route4Me(
            "k" * 32,
            enable_circuit_breaker=True,
            circuit_breaker_failure_threshold=2,
            circuit_breaker_duration=7.0,
        )

        assert client.circuit_breaker.failure_threshold == 2
        assert client.circuit_breaker.reset_timeout == 7.0

    def test_it_opens_and_then_fails_fast(self, mocked):
        client = Route4Me(
            "1" * 32,
            enable_circuit_breaker=True,
            circuit_breaker_failure_threshold=2,
            circuit_breaker_duration=30.0,
        )
        mocked.add(responses.GET, ROUTE_HOST, json={"errors": ["down"]}, status=503)

        client.route.get_routes(limit=1, offset=0)
        client.route.get_routes(limit=1, offset=0)
        calls_before = len(mocked.calls)

        # The breaker is open now: the next call must not reach the transport.
        with pytest.raises(CircuitBreakerOpen):
            client.route.get_routes(limit=1, offset=0)

        assert len(mocked.calls) == calls_before

    def test_the_global_config_enables_it(self, monkeypatch):
        monkeypatch.setattr(Route4MeConfig, "enable_circuit_breaker", True)

        assert Route4Me("k" * 32).circuit_breaker is not None


class TestParamsAreNotMutated:
    def test_a_resources_params_dict_does_not_accumulate(self, client, mocked):
        """Regression: `_make_request` used to write `api_key` into the dict it
        was handed. Every resource passes its own long-lived `self.params`, so
        query parameters accumulated on it and leaked between calls."""
        mocked.add(responses.GET, ROUTE_HOST, json=[], status=200)
        mocked.add(responses.GET, ROUTE_HOST, json=[], status=200)
        before = dict(client.route.params)

        client.route.get_routes(limit=1, offset=0)
        client.route.get_routes(limit=2, offset=5)

        assert client.route.params == before

    def test_the_caller_of_make_request_keeps_its_dict(self, client, mocked):
        mocked.add(responses.GET, ROUTE_HOST, json={}, status=200)
        params = {"limit": 1}

        client._make_request(ROUTE_HOST, params, client._request_get)

        assert params == {"limit": 1}

    def test_a_none_params_argument_is_tolerated(self, client, mocked):
        mocked.add(responses.GET, ROUTE_HOST, json={}, status=200)

        client._make_request(ROUTE_HOST, None, client._request_get)

        assert len(mocked.calls) == 1
