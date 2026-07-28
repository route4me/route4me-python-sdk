"""Retry with exponential backoff, and a circuit breaker.

Mirrors the C# SDK's Polly policy (``Resilience/HttpResiliencePolicy.cs``):
retry on transient failures with exponential backoff plus jitter, and an
optional circuit breaker that trips after a run of consecutive failures.

**Why this is hand-rolled rather than ``urllib3.Retry``**, despite ``Retry``
being free with ``requests``:

* ``backoff_jitter`` only exists in urllib3 >= 2.0, and this package supports
  whatever urllib3 the installed ``requests`` pulls in. Without jitter, a fleet
  of clients retries in lockstep and hammers a recovering server.
* urllib3 has no circuit breaker, so half the C# parity would be missing.
* There is no ``on_retry`` hook, because retries happen below ``requests``
  inside the connection pool -- nothing to observe or log.
* ``raise_on_status=True`` surfaces ``requests.exceptions.RetryError``, a type
  callers' ``except APIException`` blocks do not catch, so it perturbs the
  error contract. ``raise_on_status=False`` swallows connection errors instead.
* Decisively: the ``responses`` mock library patches ``HTTPAdapter.send``,
  which sits *above* ``Retry`` -- so urllib3-level retries are untestable in
  this suite.

``Session`` + ``HTTPAdapter`` are still used, for connection pooling; the
adapter is just mounted with retries disabled.

One place this is deliberately *more* conservative than the C# SDK: only
idempotent verbs are retried. See :data:`RETRYABLE_METHODS`.
"""

import logging
import random
import threading
import time

import requests

logger = logging.getLogger(__name__)

#: HTTP statuses worth retrying. 408 Request Timeout, 429 Too Many Requests,
#: and the 5xx family that indicates a transient server-side fault.
RETRYABLE_STATUSES = frozenset({408, 429, 500, 502, 503, 504})

#: Transport-level exceptions worth retrying. Note ``requests.Timeout`` is a
#: subclass of ``RequestException`` but *not* of ``ConnectionError``.
RETRYABLE_EXCEPTIONS = (
    requests.ConnectionError,
    requests.Timeout,
)

#: Only idempotent verbs are retried.
#:
#: POST is excluded deliberately. Retrying ``POST /orders-platform/batch-create``
#: after a 503 can create the orders twice -- the server may well have processed
#: the first request and failed only while responding. The C# Polly policy does
#: retry POST; that is a hazard this SDK does not reproduce.
RETRYABLE_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "PUT", "DELETE"})

#: Ceiling on a server-supplied ``Retry-After``. Without it, a misconfigured
#: proxy sending ``Retry-After: 86400`` would hang the caller for a day.
MAX_RETRY_AFTER = 120.0


class CircuitBreakerOpen(requests.RequestException):
    """Raised when the breaker is open and a request is short-circuited.

    Subclasses ``requests.RequestException`` so that callers already handling
    transport failures catch this too, rather than seeing a novel exception
    type escape from the SDK.
    """


def parse_retry_after(value):
    """Parse a ``Retry-After`` header into seconds, or ``None``.

    Handles the delta-seconds form. The HTTP-date form is accepted but treated
    as unparseable rather than pulling in a date parser -- Route4Me sends
    delta-seconds, and guessing wrong here would be worse than backing off
    normally. Clamped to :data:`MAX_RETRY_AFTER`.

    The C# SDK ignores this header entirely; honouring it is strictly better
    behaviour toward a rate-limited server.
    """
    if not value:
        return None
    try:
        seconds = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if seconds < 0:
        return None
    return min(seconds, MAX_RETRY_AFTER)


class CircuitBreaker:
    """Consecutive-failure circuit breaker.

    Defaults mirror the C# ``CircuitBreakerFailureThreshold`` (5) and
    ``CircuitBreakerDuration`` (30s). Disabled unless explicitly enabled on
    :class:`route4me.config.Route4MeConfig` or the client.

    Thread-safe: all state transitions are taken under a lock, and the clock is
    ``time.monotonic`` so a wall-clock adjustment cannot wedge it open.
    """

    def __init__(self, failure_threshold=5, reset_timeout=30.0, on_open=None):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.on_open = on_open
        self._lock = threading.Lock()
        self._failures = 0
        self._opened_at = None

    @property
    def is_open(self):
        with self._lock:
            return self._opened_at is not None

    @property
    def failure_count(self):
        with self._lock:
            return self._failures

    def before_request(self):
        """Short-circuit if the breaker is open.

        :raise CircuitBreakerOpen: while the breaker is open. After
            ``reset_timeout`` elapses the breaker half-opens and lets a single
            probe through; if that probe fails the breaker re-opens.
        """
        with self._lock:
            if self._opened_at is None:
                return
            elapsed = time.monotonic() - self._opened_at
            if elapsed < self.reset_timeout:
                raise CircuitBreakerOpen(
                    f"Route4Me circuit breaker is open; retry in {self.reset_timeout - elapsed:.1f}s"
                )
            # Half-open: let one probe through.
            self._opened_at = None
            self._failures = 0
            logger.debug("Route4Me circuit breaker half-open; allowing a probe request")

    def record_success(self):
        with self._lock:
            self._failures = 0
            self._opened_at = None

    def record_failure(self, exc=None):
        with self._lock:
            self._failures += 1
            if self._failures >= self.failure_threshold and self._opened_at is None:
                self._opened_at = time.monotonic()
                callback = self.on_open
                threshold, timeout = self._failures, self.reset_timeout
            else:
                callback = None
        if callback is not None:
            logger.warning(
                "Route4Me circuit breaker opened after %d consecutive failures; requests will fail fast for %.1fs",
                threshold,
                timeout,
            )
            # Called outside the lock: a user callback must not be able to
            # deadlock the breaker by touching it re-entrantly.
            try:
                callback(exc, timeout)
            except Exception:
                logger.exception("Route4Me on_circuit_breaker_open callback raised")

    def reset(self):
        """Force the breaker closed. Intended for tests and manual recovery."""
        with self._lock:
            self._failures = 0
            self._opened_at = None


def backoff_delay(attempt, initial_delay, jitter_ratio=0.2, rng=None):
    """Return the delay before ``attempt``, exponential with jitter.

    ``initial_delay * 2 ** (attempt - 1)``, then multiplied by a factor drawn
    uniformly from ``1 +/- jitter_ratio`` -- matching the C# policy's +/-20%.

    With ``initial_delay=0.2`` the un-jittered sequence is 0.2s, 0.4s, 0.8s,
    1.6s. The jitter is what stops a fleet of clients from retrying in lockstep
    and re-flooding a server that is only just recovering.

    :param attempt: 1-based retry number.
    :param rng: injectable ``random.Random`` for deterministic tests.
    """
    base = initial_delay * (2 ** (attempt - 1))
    generator = rng or random
    factor = 1.0 + generator.uniform(-jitter_ratio, jitter_ratio)
    return max(0.0, base * factor)


def should_retry_response(response, method):
    """Whether ``response`` on ``method`` is worth retrying."""
    if method.upper() not in RETRYABLE_METHODS:
        return False
    return response.status_code in RETRYABLE_STATUSES


def should_retry_exception(exc, method):
    """Whether ``exc`` on ``method`` is worth retrying."""
    if method.upper() not in RETRYABLE_METHODS:
        return False
    return isinstance(exc, RETRYABLE_EXCEPTIONS)


def execute_with_retry(
    send,
    method,
    retry_count=0,
    initial_delay=0.2,
    circuit_breaker=None,
    on_retry=None,
    sleep=time.sleep,
    rng=None,
):
    """Call ``send()``, retrying transient failures.

    :param send: zero-argument callable performing one attempt.
    :param method: HTTP verb, used to decide whether retrying is safe at all.
    :param retry_count: retries *after* the first attempt. 0 disables retrying,
        matching the C# default of ``RetryCount = 0``.
    :param initial_delay: exponential-backoff base, in seconds.
    :param circuit_breaker: optional :class:`CircuitBreaker`.
    :param on_retry: ``callback(exc_or_response, delay, attempt)``, invoked
        before each sleep. Exceptions from it are logged, never propagated.
    :param sleep: injectable for tests, so they need not actually wait.
    :param rng: injectable randomness for deterministic jitter in tests.
    :returns: the final :class:`requests.Response`.
    :raise CircuitBreakerOpen: if the breaker is open.

    The last attempt's outcome is returned or raised as-is, so a caller that
    exhausts its retries sees the real response or the real exception -- never
    a wrapper type they are not expecting.
    """
    attempts = max(0, retry_count) + 1
    last_exc = None

    for attempt in range(1, attempts + 1):
        if circuit_breaker is not None:
            circuit_breaker.before_request()

        try:
            response = send()
        except RETRYABLE_EXCEPTIONS as exc:
            last_exc = exc
            if circuit_breaker is not None:
                circuit_breaker.record_failure(exc)
            if attempt >= attempts or not should_retry_exception(exc, method):
                raise
            _wait(attempt, initial_delay, None, exc, on_retry, sleep, rng)
            continue
        except requests.RequestException as exc:
            # Not transient (e.g. TooManyRedirects, InvalidURL): the breaker
            # still counts it, but there is nothing to gain by retrying.
            if circuit_breaker is not None:
                circuit_breaker.record_failure(exc)
            raise

        if circuit_breaker is not None:
            if 500 <= response.status_code < 600:
                circuit_breaker.record_failure()
            else:
                circuit_breaker.record_success()

        if attempt >= attempts or not should_retry_response(response, method):
            return response

        retry_after = parse_retry_after(response.headers.get("Retry-After"))
        _wait(attempt, initial_delay, retry_after, response, on_retry, sleep, rng)

    # Unreachable: the loop either returns or raises. Kept as a guard so a
    # future edit to the control flow fails loudly instead of returning None.
    raise last_exc or RuntimeError("retry loop exited without a result")


def _wait(attempt, initial_delay, retry_after, outcome, on_retry, sleep, rng):
    """Sleep before the next attempt, honouring ``Retry-After`` when present."""
    delay = retry_after if retry_after is not None else backoff_delay(attempt, initial_delay, rng=rng)
    logger.debug("Route4Me retrying after %.3fs (attempt %d)", delay, attempt)
    if on_retry is not None:
        try:
            on_retry(outcome, delay, attempt)
        except Exception:
            logger.exception("Route4Me on_retry callback raised")
    if delay > 0:
        sleep(delay)
