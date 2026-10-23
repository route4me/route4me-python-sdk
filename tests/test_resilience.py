"""Tests for ``route4me/_resilience.py``.

The retry loop is deliberately hand-rolled rather than delegated to
``urllib3.Retry`` -- see that module's docstring. A consequence is that it is
*our* correctness to prove, so these tests are thorough about the things that
go wrong in retry code: retrying non-idempotent verbs, unbounded
``Retry-After``, jitter that isn't random, breakers that never close, and
callbacks that can take down the caller.

``sleep`` and ``rng`` are injected everywhere, so the suite never actually
waits and the jitter is deterministic.
"""

import random

import pytest
import requests

from route4me._resilience import (
    MAX_RETRY_AFTER,
    RETRYABLE_METHODS,
    RETRYABLE_STATUSES,
    CircuitBreaker,
    CircuitBreakerOpen,
    backoff_delay,
    execute_with_retry,
    parse_retry_after,
    should_retry_exception,
    should_retry_response,
)


class FakeResponse:
    def __init__(self, status_code=200, headers=None):
        self.status_code = status_code
        self.headers = headers or {}


class Recorder:
    """A ``send`` callable returning a scripted sequence of outcomes."""

    def __init__(self, *outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def __call__(self):
        self.calls += 1
        outcome = self.outcomes[min(self.calls - 1, len(self.outcomes) - 1)]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


@pytest.fixture
def slept():
    """Collect sleep durations instead of waiting."""
    return []


@pytest.fixture
def sleep(slept):
    return slept.append


@pytest.fixture
def rng():
    """Seeded RNG so jitter is reproducible."""
    return random.Random(1234)


class TestParseRetryAfter:
    @pytest.mark.parametrize(("value", "expected"), [("5", 5.0), ("0", 0.0), (" 10 ", 10.0), ("1.5", 1.5), (30, 30.0)])
    def test_delta_seconds(self, value, expected):
        assert parse_retry_after(value) == expected

    @pytest.mark.parametrize("value", [None, "", "Wed, 21 Oct 2015 07:28:00 GMT", "soon", "-1"])
    def test_unparseable_or_negative_yields_none(self, value):
        assert parse_retry_after(value) is None

    def test_it_is_clamped(self):
        """A misconfigured proxy sending `Retry-After: 86400` must not hang the
        caller for a day."""
        assert parse_retry_after("86400") == MAX_RETRY_AFTER


class TestBackoffDelay:
    def test_it_doubles_each_attempt(self):
        """Jitter neutralised by an rng whose uniform() returns 0."""

        class NoJitter:
            @staticmethod
            def uniform(a, b):
                return 0.0

        delays = [backoff_delay(n, 0.2, rng=NoJitter()) for n in (1, 2, 3, 4)]
        assert delays == [0.2, 0.4, 0.8, 1.6]

    def test_jitter_stays_within_the_declared_band(self, rng):
        for attempt in range(1, 6):
            base = 0.2 * (2 ** (attempt - 1))
            for _ in range(50):
                delay = backoff_delay(attempt, 0.2, jitter_ratio=0.2, rng=rng)
                assert 0.8 * base <= delay <= 1.2 * base

    def test_jitter_actually_varies(self, rng):
        """Lockstep retries are the failure mode jitter exists to prevent."""
        delays = {backoff_delay(3, 0.2, rng=rng) for _ in range(20)}
        assert len(delays) > 1

    def test_it_is_never_negative(self):
        class Extreme:
            @staticmethod
            def uniform(a, b):
                return -5.0

        assert backoff_delay(1, 0.2, rng=Extreme()) == 0.0


class TestRetryEligibility:
    @pytest.mark.parametrize("status", sorted(RETRYABLE_STATUSES))
    def test_transient_statuses_are_retried_on_get(self, status):
        assert should_retry_response(FakeResponse(status), "GET")

    @pytest.mark.parametrize("status", [200, 201, 301, 400, 401, 403, 404, 422])
    def test_success_and_client_errors_are_not_retried(self, status):
        assert not should_retry_response(FakeResponse(status), "GET")

    @pytest.mark.parametrize("method", sorted(RETRYABLE_METHODS))
    def test_idempotent_verbs_are_retryable(self, method):
        assert should_retry_response(FakeResponse(503), method)

    def test_post_is_never_retried(self):
        """Replaying `POST /orders-platform/batch-create` after a 503 can create
        the orders twice: the server may have processed the first request and
        failed only while responding. The C# Polly policy does retry POST; this
        SDK deliberately does not."""
        assert not should_retry_response(FakeResponse(503), "POST")
        assert not should_retry_exception(requests.ConnectionError(), "POST")

    @pytest.mark.parametrize("method", ["PUT", "PATCH"])
    def test_updates_are_never_retried(self, method):
        """``PUT /api.v4/route.php`` appends the addresses it is given (#19), and
        a PATCH is no safer to replay."""
        assert not should_retry_response(FakeResponse(503), method)
        assert not should_retry_exception(requests.ConnectionError(), method)

    def test_method_matching_is_case_insensitive(self):
        assert should_retry_response(FakeResponse(503), "get")

    @pytest.mark.parametrize("exc", [requests.ConnectionError(), requests.Timeout(), requests.ReadTimeout()])
    def test_transport_failures_are_retryable(self, exc):
        assert should_retry_exception(exc, "GET")

    @pytest.mark.parametrize("exc", [requests.TooManyRedirects(), requests.URLRequired(), ValueError()])
    def test_non_transient_failures_are_not_retryable(self, exc):
        assert not should_retry_exception(exc, "GET")


class TestExecuteWithRetry:
    def test_a_success_is_returned_without_sleeping(self, sleep, slept):
        send = Recorder(FakeResponse(200))

        result = execute_with_retry(send, "GET", retry_count=3, sleep=sleep)

        assert result.status_code == 200
        assert send.calls == 1
        assert slept == []

    def test_retry_is_off_by_default(self, sleep, slept):
        """Matching C# `RetryCount = 0`, so upgrading cannot silently multiply
        the number of requests a service emits."""
        send = Recorder(FakeResponse(503))

        result = execute_with_retry(send, "GET", sleep=sleep)

        assert result.status_code == 503
        assert send.calls == 1
        assert slept == []

    def test_it_retries_then_succeeds(self, sleep, slept, rng):
        send = Recorder(FakeResponse(503), FakeResponse(503), FakeResponse(200))

        result = execute_with_retry(send, "GET", retry_count=3, sleep=sleep, rng=rng)

        assert result.status_code == 200
        assert send.calls == 3
        assert len(slept) == 2

    def test_retries_are_bounded_and_the_last_response_is_returned(self, sleep, slept, rng):
        send = Recorder(FakeResponse(503))

        result = execute_with_retry(send, "GET", retry_count=2, sleep=sleep, rng=rng)

        assert result.status_code == 503
        assert send.calls == 3  # the initial attempt plus two retries
        assert len(slept) == 2

    def test_the_final_exception_propagates_unwrapped(self, sleep, rng):
        """A caller that exhausts retries must see the real exception, not a
        wrapper type their `except` blocks do not know about."""
        original = requests.ConnectionError("boom")
        send = Recorder(original)

        with pytest.raises(requests.ConnectionError) as excinfo:
            execute_with_retry(send, "GET", retry_count=2, sleep=sleep, rng=rng)

        assert excinfo.value is original
        assert send.calls == 3

    def test_a_non_transient_exception_is_not_retried(self, sleep, slept):
        send = Recorder(requests.TooManyRedirects())

        with pytest.raises(requests.TooManyRedirects):
            execute_with_retry(send, "GET", retry_count=3, sleep=sleep)

        assert send.calls == 1
        assert slept == []

    def test_a_post_is_not_retried_even_on_503(self, sleep, slept):
        send = Recorder(FakeResponse(503))

        result = execute_with_retry(send, "POST", retry_count=3, sleep=sleep)

        assert result.status_code == 503
        assert send.calls == 1
        assert slept == []

    def test_retry_after_overrides_the_backoff(self, sleep, slept, rng):
        send = Recorder(FakeResponse(429, {"Retry-After": "7"}), FakeResponse(200))

        execute_with_retry(send, "GET", retry_count=2, sleep=sleep, rng=rng)

        assert slept == [7.0]

    def test_an_absurd_retry_after_is_clamped(self, sleep, slept, rng):
        send = Recorder(FakeResponse(429, {"Retry-After": "99999"}), FakeResponse(200))

        execute_with_retry(send, "GET", retry_count=2, sleep=sleep, rng=rng)

        assert slept == [MAX_RETRY_AFTER]

    def test_on_retry_is_called_with_the_outcome_delay_and_attempt(self, sleep, rng):
        seen = []
        send = Recorder(FakeResponse(503), FakeResponse(200))

        execute_with_retry(
            send, "GET", retry_count=2, on_retry=lambda o, d, a: seen.append((o.status_code, a)), sleep=sleep, rng=rng
        )

        assert seen == [(503, 1)]

    def test_a_raising_on_retry_callback_cannot_break_the_request(self, sleep, rng):
        """A user callback must never turn a recoverable failure into a crash."""

        def bad(outcome, delay, attempt):
            raise RuntimeError("callback exploded")

        send = Recorder(FakeResponse(503), FakeResponse(200))

        result = execute_with_retry(send, "GET", retry_count=2, on_retry=bad, sleep=sleep, rng=rng)

        assert result.status_code == 200


class TestCircuitBreaker:
    def test_it_starts_closed(self):
        assert not CircuitBreaker().is_open

    def test_it_opens_after_the_threshold(self):
        breaker = CircuitBreaker(failure_threshold=3)

        for _ in range(3):
            breaker.record_failure()

        assert breaker.is_open

    def test_it_stays_closed_below_the_threshold(self):
        breaker = CircuitBreaker(failure_threshold=3)

        breaker.record_failure()
        breaker.record_failure()

        assert not breaker.is_open

    def test_a_success_resets_the_counter(self):
        """The counter is *consecutive* failures, so an intermittent error does
        not eventually trip the breaker."""
        breaker = CircuitBreaker(failure_threshold=3)

        breaker.record_failure()
        breaker.record_failure()
        breaker.record_success()
        breaker.record_failure()

        assert not breaker.is_open
        assert breaker.failure_count == 1

    def test_an_open_breaker_short_circuits(self):
        breaker = CircuitBreaker(failure_threshold=1, reset_timeout=30.0)
        breaker.record_failure()

        with pytest.raises(CircuitBreakerOpen):
            breaker.before_request()

    def test_it_half_opens_after_the_timeout(self):
        breaker = CircuitBreaker(failure_threshold=1, reset_timeout=0.0)
        breaker.record_failure()

        breaker.before_request()  # must not raise

        assert not breaker.is_open

    def test_open_is_a_requests_exception(self):
        """So callers already handling transport failures catch it, rather than
        a novel type escaping the SDK."""
        assert issubclass(CircuitBreakerOpen, requests.RequestException)

    def test_on_open_is_called_once(self):
        seen = []
        breaker = CircuitBreaker(failure_threshold=2, on_open=lambda exc, t: seen.append(t))

        breaker.record_failure()
        breaker.record_failure()
        breaker.record_failure()

        assert len(seen) == 1

    def test_a_raising_on_open_callback_is_contained(self):
        def bad(exc, timeout):
            raise RuntimeError("nope")

        breaker = CircuitBreaker(failure_threshold=1, on_open=bad)

        breaker.record_failure()  # must not raise

        assert breaker.is_open

    def test_half_open_lets_exactly_one_probe_through(self):
        breaker = CircuitBreaker(failure_threshold=5, reset_timeout=0.0)
        for _ in range(5):
            breaker.record_failure()

        breaker.before_request()  # the probe

        assert breaker.state == "half-open"
        with pytest.raises(CircuitBreakerOpen):
            breaker.before_request()

    def test_a_failed_probe_reopens_at_once_whatever_the_threshold(self):
        breaker = CircuitBreaker(failure_threshold=5, reset_timeout=30.0)
        for _ in range(5):
            breaker.record_failure()
        breaker._opened_at -= 31.0  # pretend the reset timeout elapsed
        breaker.before_request()

        breaker.record_failure()

        assert breaker.state == "open"
        with pytest.raises(CircuitBreakerOpen):
            breaker.before_request()

    def test_a_successful_probe_closes_it(self):
        breaker = CircuitBreaker(failure_threshold=2, reset_timeout=0.0)
        breaker.record_failure()
        breaker.record_failure()
        breaker.before_request()

        breaker.record_success()

        assert breaker.state == "closed"
        assert breaker.failure_count == 0

    def test_an_unexpected_error_releases_the_probe(self):
        breaker = CircuitBreaker(failure_threshold=1, reset_timeout=0.0)
        breaker.record_failure()

        def broken_send():
            raise ValueError("bug in a hook")

        with pytest.raises(ValueError):
            execute_with_retry(broken_send, "GET", circuit_breaker=breaker)

        assert breaker.state == "open"

    def test_reset_forces_it_closed(self):
        breaker = CircuitBreaker(failure_threshold=1)
        breaker.record_failure()

        breaker.reset()

        assert not breaker.is_open
        assert breaker.failure_count == 0

    def test_execute_with_retry_short_circuits_on_an_open_breaker(self, sleep):
        breaker = CircuitBreaker(failure_threshold=1, reset_timeout=30.0)
        breaker.record_failure()
        send = Recorder(FakeResponse(200))

        with pytest.raises(CircuitBreakerOpen):
            execute_with_retry(send, "GET", retry_count=3, circuit_breaker=breaker, sleep=sleep)

        assert send.calls == 0, "the request should never have been attempted"

    def test_a_5xx_counts_as_a_breaker_failure(self, sleep, rng):
        breaker = CircuitBreaker(failure_threshold=10)
        send = Recorder(FakeResponse(503))

        execute_with_retry(send, "GET", retry_count=2, circuit_breaker=breaker, sleep=sleep, rng=rng)

        assert breaker.failure_count == 3

    def test_a_4xx_does_not_count(self, sleep):
        """A 404 is the server working correctly; it must not trip the breaker."""
        breaker = CircuitBreaker(failure_threshold=2)
        send = Recorder(FakeResponse(404))

        execute_with_retry(send, "GET", retry_count=0, circuit_breaker=breaker, sleep=sleep)

        assert breaker.failure_count == 0
        assert not breaker.is_open
