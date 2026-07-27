"""Shared pytest fixtures.

The suite is **offline by design**. ``pytest-socket`` is armed in
``pyproject.toml`` via ``--disable-socket``, so any test that reaches a real
socket fails loudly instead of silently depending on the network, a live API
key, or Route4Me's uptime. Tests that are *supposed* to dial out live under
``tests/live/`` and carry ``@pytest.mark.live``, which the default run
deselects.

HTTP is faked with `responses <https://github.com/getsentry/responses>`_,
which patches ``HTTPAdapter.send``. That sits above urllib3, so the whole
``Route4Me`` request path -- parameter assembly, ``api_key`` injection, status
handling, ``APIException`` construction -- is exercised for real; only the
wire is replaced.
"""

import json
import pathlib

import pytest
import responses as responses_lib

from route4me import Route4Me

#: The dummy key used throughout the suite. 32 hex chars, matching the shape of
#: a real Route4Me key so length/format assumptions are exercised, but
#: obviously fake so it can never be mistaken for a live credential.
API_KEY = "1" * 32

FIXTURE_DIR = pathlib.Path(__file__).resolve().parent / "fixtures"


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
    from urllib.parse import parse_qs, urlsplit

    def _query(request):
        raw = parse_qs(urlsplit(request.url).query, keep_blank_values=True)
        return {k: (v[0] if len(v) == 1 else v) for k, v in raw.items()}

    return _query
