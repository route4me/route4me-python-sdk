"""The API hosts come from ``ROUTE4ME_API_HOST`` / ``ROUTE4ME_API_V5_HOST`` (route4me.api_endpoints).

They are read once, at import, and every module copies the endpoint URLs it needs at its own import. So each case
imports the SDK in a fresh interpreter with its own environment: that is the only way to see what a process started
with those variables really gets.
"""

import json
import os
import pathlib
import subprocess
import sys

import pytest

from route4me.api_endpoints import _host_url

REPO = pathlib.Path(__file__).resolve().parent.parent

PROBE = r"""
import json
import route4me
from route4me import _url, api_endpoints, gps
from route4me.api import Route4Me

sent = []

class _Ok:
    status_code = 200

def capture(url, params, **kwargs):
    sent.append({"url": url, "params": params, "auth": (kwargs.get("headers") or {}).get("Authorization")})
    return _Ok()

client = Route4Me("K" * 32)
client._make_request(api_endpoints.ROUTE_HOST, {}, capture)
client._make_request(api_endpoints.ROUTE_STATUS_V5, {}, capture)
client._make_request("https://api.route4me.com/api.v4/route.php", {}, capture)
print(json.dumps({
    "main": api_endpoints.MAIN_HOST, "v5": api_endpoints.API_V5, "route": api_endpoints.ROUTE_HOST,
    "exporter": api_endpoints.EXPORTER_V5.format(route_id="R1"), "key_hosts": list(_url.API_KEY_HOSTS),
    "v5_prefix": _url.API_V5_PREFIX, "copied": [v for k, v in vars(gps).items() if k.isupper() and isinstance(v, str)
                                                and v.startswith("https://")],
    "sent": sent,
}))
"""


def probe(**env):
    """Import the SDK in a fresh interpreter with these ROUTE4ME_* variables -> what it resolved."""
    clean = {k: v for k, v in os.environ.items() if not k.startswith("ROUTE4ME_")}
    clean.update(env)
    clean["PYTHONPATH"] = str(REPO)
    # Python 3.13+ colours tracebacks when FORCE_COLOR is set (CI sets it), which wraps the error line in ANSI codes.
    # PYTHON_COLORS=0 wins over FORCE_COLOR; older interpreters ignore it.
    clean["PYTHON_COLORS"] = "0"
    done = subprocess.run(  # noqa: S603 - the interpreter running the tests, on the constant PROBE script
        [sys.executable, "-c", PROBE], cwd=REPO, env=clean, capture_output=True, text=True, timeout=60, check=False
    )
    if done.returncode:
        return {"error": done.stderr.strip().splitlines()[-1]}
    return json.loads(done.stdout.strip().splitlines()[-1])


def test_without_the_variables_the_sdk_talks_to_production():
    got = probe()
    assert got["main"] == "https://api.route4me.com"
    assert got["v5"] == "https://wh.route4me.com/modules/api/v5.0"
    assert got["exporter"] == "https://wh.route4me.com/modules/api/v5.0/route-export/R1/export"
    assert got["key_hosts"] == ["api.route4me.com", "wh.route4me.com"]
    assert got["v5_prefix"] == "https://wh.route4me.com/modules/api/v5."


def test_the_variables_move_every_endpoint_and_the_api_key_with_them():
    got = probe(ROUTE4ME_API_HOST="api.staging.example", ROUTE4ME_API_V5_HOST="https://WH.staging.example/")
    assert got["main"] == "https://api.staging.example"
    assert got["route"] == "https://api.staging.example/api.v4/route.php"
    assert got["v5"] == "https://wh.staging.example/modules/api/v5.0"
    assert got["exporter"] == "https://wh.staging.example/modules/api/v5.0/route-export/R1/export"
    assert got["key_hosts"] == ["api.staging.example", "wh.staging.example"]
    # a module that copied its URLs at import has the staging ones
    assert got["copied"] and all(
        u.startswith(("https://api.staging.example", "https://wh.staging.example")) for u in got["copied"]
    )
    v4, v5, production = got["sent"]
    assert v4["params"]["api_key"] == "K" * 32 and v4["auth"] is None  # V4: key as a query parameter
    assert v5["auth"] == f"Bearer {'K' * 32}" and "api_key" not in v5["params"]  # V5: key as a bearer token
    assert "api_key" not in production["params"] and production["auth"] is None  # never to the other environment


def test_one_host_can_be_moved_alone():
    got = probe(ROUTE4ME_API_HOST="api.staging.example")
    assert got["main"] == "https://api.staging.example"
    assert got["v5"] == "https://wh.route4me.com/modules/api/v5.0"
    assert got["key_hosts"] == ["api.staging.example", "wh.route4me.com"]


def test_a_port_is_kept():
    got = probe(ROUTE4ME_API_HOST="https://api.staging.example:8443")
    assert got["route"] == "https://api.staging.example:8443/api.v4/route.php"
    assert got["key_hosts"][0] == "api.staging.example"


# ------------------------------------------------------------------------------------- the value itself


@pytest.mark.parametrize(
    ("value", "url"),
    [
        ("api.staging.example", "https://api.staging.example"),
        (" https://API.Staging.example/ ", "https://api.staging.example"),
        ("api.staging.example:8443", "https://api.staging.example:8443"),
    ],
)
def test_a_host_name_or_https_url_becomes_the_base(monkeypatch, value, url):
    monkeypatch.setenv("ROUTE4ME_API_HOST", value)
    assert _host_url("ROUTE4ME_API_HOST", "https://api.route4me.com") == url


def test_unset_or_blank_is_the_default(monkeypatch):
    monkeypatch.delenv("ROUTE4ME_API_HOST", raising=False)
    assert _host_url("ROUTE4ME_API_HOST", "https://api.route4me.com") == "https://api.route4me.com"
    monkeypatch.setenv("ROUTE4ME_API_HOST", "   ")
    assert _host_url("ROUTE4ME_API_HOST", "https://api.route4me.com") == "https://api.route4me.com"


@pytest.mark.parametrize(
    "value",
    [
        "http://api.staging.example",  # the key never goes over plain http
        "https://api.staging.example/api.v4",  # a path would double up with every endpoint's
        "https://user:secret@api.staging.example",
        "https://api.staging.example?x=1",
        "https://",
    ],
)
def test_a_value_that_is_not_an_https_host_is_refused(monkeypatch, value):
    monkeypatch.setenv("ROUTE4ME_API_HOST", value)
    with pytest.raises(ValueError, match="ROUTE4ME_API_HOST must be a host name or an https:// URL"):
        _host_url("ROUTE4ME_API_HOST", "https://api.route4me.com")


def test_a_refused_value_stops_the_import():
    got = probe(ROUTE4ME_API_HOST="http://api.staging.example")
    assert got["error"].startswith("ValueError: ROUTE4ME_API_HOST must be a host name or an https:// URL")


def test_a_blank_variable_means_production():
    assert probe(ROUTE4ME_API_HOST="  ", ROUTE4ME_API_V5_HOST="")["main"] == "https://api.route4me.com"
