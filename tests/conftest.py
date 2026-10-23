"""Shared pytest fixtures.

The suite is **offline by design**. ``pytest-socket`` is armed in
``pyproject.toml`` via ``--disable-socket``, so any test that reaches a real
socket fails loudly instead of silently depending on the network, a live API
key, or Route4Me's uptime. Tests that need the real API are kept outside the
repository, so no key ever has to be configured here.

HTTP is faked with `responses <https://github.com/getsentry/responses>`_,
which patches ``HTTPAdapter.send``. That sits above urllib3, so the whole
``Route4Me`` request path -- parameter assembly, ``api_key`` injection, status
handling, ``APIException`` construction -- is exercised for real; only the
wire is replaced.
"""

import collections
import json
import pathlib
import re
from urllib.parse import parse_qs, urlsplit

import pytest
import requests
import responses as responses_lib

from route4me import Route4Me

#: The dummy key used throughout the suite. 32 hex chars, matching the shape of
#: a real Route4Me key so length/format assumptions are exercised, but
#: obviously fake so it can never be mistaken for a live credential.
API_KEY = "1" * 32

FIXTURE_DIR = pathlib.Path(__file__).resolve().parent / "fixtures"


#: Hosts the SDK talks to. Used to short-circuit proxy resolution below.
SDK_HOSTS = "route4me.com,swaggerhub.com,localhost,127.0.0.1"


@pytest.fixture(autouse=True)
def _isolate_proxy_environment(monkeypatch):
    """Keep the ambient proxy configuration out of the test run.

    Even with ``HTTPAdapter.send`` mocked, ``requests`` still calls
    ``merge_environment_settings`` -> ``should_bypass_proxies`` on every
    request. When ``no_proxy`` is unset that ends in
    ``urllib.request.proxy_bypass``, which on macOS consults the system network
    configuration and resolves the hostname -- tripping ``pytest-socket`` and
    failing the test for reasons that have nothing to do with the SDK.

    Setting ``no_proxy`` to cover the SDK's hosts makes ``requests`` return
    early on a pure string comparison. Clearing the proxy variables means a
    developer behind a corporate proxy gets the same result as CI, rather than
    a differently-shaped request.
    """
    for var in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("NO_PROXY", SDK_HOSTS)
    monkeypatch.setenv("no_proxy", SDK_HOSTS)


@pytest.fixture
def api_key():
    """The dummy API key the ``client`` fixture is built with."""
    return API_KEY


@pytest.fixture
def client():
    """A :class:`route4me.Route4Me` wired to the dummy key.

    Function-scoped on purpose: resource objects carry mutable ``self.params``
    and ``self.data`` that accumulate across calls, so sharing one client
    between tests would leak state between them.
    """
    return Route4Me(API_KEY)


@pytest.fixture
def mocked():
    """Activated ``responses`` mock.

    ``assert_all_requests_are_fired`` stays off: several tests register a
    response for a URL and then assert the SDK *doesn't* call it.
    """
    with responses_lib.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps


@pytest.fixture
def load_fixture():
    """Load a recorded JSON payload from ``tests/fixtures/``.

    Payloads are captured once against the real API and scrubbed of account
    identifiers before being committed.

        def test_x(mocked, load_fixture):
            mocked.add(responses.GET, URL, json=load_fixture("routes_list"))
    """

    def _load(name):
        path = FIXTURE_DIR / f"{name}.json"
        if not path.exists():
            available = sorted(p.stem for p in FIXTURE_DIR.glob("*.json"))
            raise AssertionError(f"no fixture named {name!r}; available: {available}")
        return json.loads(path.read_text(encoding="utf-8"))

    return _load


@pytest.fixture
def last_request(mocked):
    """Return the most recent request ``responses`` captured."""

    def _last():
        assert mocked.calls, "no HTTP request was made"
        return mocked.calls[-1].request

    return _last


@pytest.fixture
def query_of():
    """Parse a request URL's query string into a plain dict.

    ``parse_qs`` yields lists; this flattens single-valued keys, which is what
    assertions actually want to compare against.
    """

    def _query(request):
        raw = parse_qs(urlsplit(request.url).query, keep_blank_values=True)
        return {k: (v[0] if len(v) == 1 else v) for k, v in raw.items()}

    return _query


# ----------------------------------------------------------- request guard --

#: Endpoint registry shared with the Java SDK tests. Generated outside the repo
#: from the Route4Me OpenAPI specs, the C# SDK constants and a liveness probe.
REGISTRY = json.loads((FIXTURE_DIR / "endpoints.json").read_text(encoding="utf-8"))


def _pattern(path):
    """Compile a registry path, where ``{}`` stands for exactly one segment."""
    return re.compile("^" + re.escape(path).replace(r"\{\}", "[^/]+") + "$")


ALLOWED_HOSTS = frozenset(REGISTRY["allowed_hosts"])
ENDPOINTS = [(e["method"], e["host"], _pattern(e["path"])) for e in REGISTRY["endpoints"]]
DEPRECATED = [(d["host"], _pattern(d["path"]), d["reason"]) for d in REGISTRY["deprecated"]]

#: Deprecated endpoints hit during the run, reported once in the summary.
DEPRECATED_HITS = collections.Counter()


def check_request(method, url, headers):
    """Return a list of problems with one outgoing request (empty when it is fine).

    Every request the SDK sends must go over https to a Route4Me host, to an
    endpoint in the registry, and must carry the API key in one place only: an
    ``Authorization: Bearer`` header for API V5, the ``api_key`` query
    parameter for everything else. A deprecated endpoint is allowed but recorded.
    """
    parts = urlsplit(url)
    path = parts.path.rstrip("/") or "/"
    problems = []
    if parts.scheme != "https":
        problems.append(f"{method} {url}: scheme is {parts.scheme!r}, not https")
    for host, pattern, reason in DEPRECATED:
        if parts.hostname == host and pattern.match(path):
            DEPRECATED_HITS[f"{method} {host}{path} ({reason})"] += 1
            return problems
    if parts.hostname not in ALLOWED_HOSTS:
        problems.append(f"{method} {url}: host {parts.hostname!r} is not an allowed Route4Me host")
    elif not any(
        host == parts.hostname and m in ("*", method) and pattern.match(path) for m, host, pattern in ENDPOINTS
    ):
        problems.append(f"{method} {parts.hostname}{path}: endpoint is not in tests/fixtures/endpoints.json")
    query = parse_qs(parts.query)
    v5 = url.startswith("https://wh.route4me.com/modules/api/v5.")
    other_headers = {k: v for k, v in headers.items() if not (v5 and k.lower() == "authorization")}
    if API_KEY in parts.path or any(API_KEY in str(v) for v in other_headers.values()):
        problems.append(f"{method} {url}: the API key appears outside its expected place")
    if any(API_KEY in v for k, values in query.items() if k != "api_key" for v in values):
        problems.append(f"{method} {url}: the API key appears in a query parameter other than api_key")
    if v5 and "api_key" in query:
        problems.append(f"{method} {url}: an API V5 request carries the key in the URL instead of a bearer token")
    if v5 and headers.get("Authorization") != f"Bearer {API_KEY}":
        problems.append(f"{method} {url}: an API V5 request lacks the bearer token")
    return problems


@pytest.fixture(autouse=True)
def _request_guard(monkeypatch):
    """Check every request the SDK sends during a test.

    ``requests.Session.send`` is the single funnel for both the pooled session
    and ``requests.request``; ``responses`` patches the adapter below it, so the
    guard sees exactly what would have gone on the wire.
    """
    seen = []
    original = requests.Session.send

    def send(session, request, **kwargs):
        seen.append(request)
        return original(session, request, **kwargs)

    monkeypatch.setattr(requests.Session, "send", send)
    yield seen
    problems = [p for request in seen for p in check_request(request.method, request.url, request.headers)]
    if problems:
        pytest.fail("request guard:\n  " + "\n  ".join(problems), pytrace=False)


def pytest_terminal_summary(terminalreporter):
    """List the deprecated endpoints the suite exercised."""
    if DEPRECATED_HITS:
        terminalreporter.section("deprecated endpoints hit")
        for line, count in sorted(DEPRECATED_HITS.items()):
            terminalreporter.write_line(f"{count:4}  {line}")
