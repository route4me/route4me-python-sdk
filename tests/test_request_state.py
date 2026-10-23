"""One call's parameters must never leak into the next request.

Resources keep a long-lived ``params`` dict. Writing per-call values into it
(a route ID, a vendor ID, ``redirect=0``) made them silently ride along on
every later request from the same client: the class of bug behind the PHP
SDK's base-URL leak and issue #36.
"""

import json

import pytest
import responses

from route4me import Route4Me
from route4me.api_endpoints import (
    API_HOST,
    AVOIDANCE,
    TELEMATICS_REGISTER_V4,
    TELEMATICS_VENDORS_ALL_V5,
    TERRITORY_HOST,
)
from route4me.exceptions import ParamValueException

OPTIMIZATION_ID = "0F3B8C2D5E7A419B6C8D0E2F4A6B8C1D"
TERRITORY_ID = "A1B2C3D4E5F60718293A4B5C6D7E8F90"
ZONE = {"territory_name": "Zone", "territory_color": "ff0000", "territory": {"type": "circle", "data": ["1,1", "5"]}}


@pytest.mark.parametrize(
    ("resource", "host", "update", "read"),
    [
        ("territory", TERRITORY_HOST, "update_territory", "get_territories"),
        ("avoidance_zones", AVOIDANCE, "update_avoidance_zone", "get_avoidance_zones"),
    ],
)
def test_an_update_does_not_leak_its_territory_id(client, mocked, query_of, last_request, resource, host, update, read):
    mocked.add(responses.PUT, host, json={}, status=200)
    mocked.add(responses.GET, host, json=[], status=200)

    getattr(getattr(client, resource), update)(TERRITORY_ID, **ZONE)
    assert query_of(last_request())["territory_id"] == TERRITORY_ID

    getattr(getattr(client, resource), read)()
    assert "territory_id" not in query_of(last_request())


@pytest.mark.parametrize("resource", ["territory", "avoidance_zones"])
def test_a_rejected_update_leaves_the_resource_unchanged(client, resource):
    method = "update_territory" if resource == "territory" else "update_avoidance_zone"

    with pytest.raises(ParamValueException):
        getattr(getattr(client, resource), method)(TERRITORY_ID)

    assert getattr(client, resource).params == {"api_key": client.key}


def test_register_member_does_not_leak_the_member_id(client, mocked, query_of, last_request):
    mocked.add(responses.GET, TELEMATICS_REGISTER_V4, json={}, status=200)
    mocked.add(responses.GET, TELEMATICS_VENDORS_ALL_V5, json={}, status=200)
    client.telematics.register_member(123456)

    client.telematics.get_vendors_v5()

    assert "member_id" not in query_of(last_request())


class TestOptimizationCalls:
    def test_get_optimization_does_not_leak_into_the_next_run(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, API_HOST, json={"optimization_problem_id": OPTIMIZATION_ID}, status=200)
        mocked.add(responses.POST, API_HOST, json={"optimization_problem_id": "NEW"}, status=200)
        client.get_optimization(OPTIMIZATION_ID)

        client.run_optimization()

        assert "optimization_problem_id" not in query_of(last_request())

    def test_re_optimization_does_not_leak_into_the_next_run(self, client, mocked, query_of, last_request):
        mocked.add(responses.PUT, API_HOST, json={}, status=200)
        mocked.add(responses.POST, API_HOST, json={}, status=200)
        client.re_optimization(OPTIMIZATION_ID)

        client.run_optimization()

        query = query_of(last_request())
        assert "optimization_problem_id" not in query
        assert "reoptimize" not in query

    def test_re_optimization_sends_the_id_and_the_flag(self, client, mocked, query_of, last_request):
        mocked.add(responses.PUT, API_HOST, json={}, status=200)

        client.re_optimization(OPTIMIZATION_ID, {"route_name": "Again"})

        query = query_of(last_request())
        assert (query["optimization_problem_id"], query["reoptimize"]) == (OPTIMIZATION_ID, "1")
        assert json.loads(last_request().body) == {"parameters": {"route_name": "Again"}}

    def test_redirect_flag_is_not_stored_on_the_optimization(self, mocked):
        client = Route4Me("1" * 32, redirects=False)
        mocked.add(responses.POST, API_HOST, json={}, status=200)

        client.run_optimization()

        assert "redirect" not in client.optimization.params

    def test_a_non_string_id_is_rejected(self, client):
        with pytest.raises(ParamValueException):
            client.get_optimization(12345)


def test_validated_params_leaves_the_resource_unchanged(client):
    query = client.route.validated_params(route_id="C0FFEE00C0FFEE00C0FFEE00C0FFEE00")

    assert query["route_id"] == "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"
    assert "route_id" not in client.route.params


def test_reset_clears_the_staged_optimization(client):
    client.optimization.route_name("First")
    client.address.add_address(address="x", lat=1.0, lng=2.0)

    client.optimization.reset()

    assert client.optimization.params == {"api_key": client.key}
    assert client.optimization.data == {"parameters": {}}
    assert not client.address.get_addresses()
