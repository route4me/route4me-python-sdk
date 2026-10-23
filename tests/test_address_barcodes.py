"""Request-level tests for :class:`route4me.address_barcodes.AddressBarcodes`."""

import json

import pytest
import responses

from route4me.api_endpoints import ADDRESS_BARCODES_V5
from route4me.exceptions import ParamValueException

ROUTE_ID = "ROUTE-1"
SCAN = {"barcode": "BARCODE-1", "scan_type": "QR-code", "lat": 40.1, "lng": -75.2, "scanned_at": "2026-10-22 10:00:00"}


def test_get_address_barcodes_sends_the_query(client, mocked, last_request, query_of):
    mocked.add(responses.GET, ADDRESS_BARCODES_V5, json={"status": True, "data": []}, status=200)

    result = client.address_barcodes.get_address_barcodes(
        route_id=ROUTE_ID, route_destination_id=42, limit=10, cursor="CURSOR-1"
    )

    request = last_request()
    assert result == {"status": True, "data": []}
    assert request.method == "GET"
    assert request.url.split("?")[0] == ADDRESS_BARCODES_V5
    assert query_of(request) == {
        "route_id": ROUTE_ID,
        "route_destination_id": "42",
        "limit": "10",
        "cursor": "CURSOR-1",
    }
    assert not request.body


def test_save_address_barcodes_posts_the_scans(client, mocked, last_request, query_of):
    mocked.add(responses.POST, ADDRESS_BARCODES_V5, json={"status": True}, status=200)

    result = client.address_barcodes.save_address_barcodes(route_id=ROUTE_ID, route_destination_id=42, barcodes=[SCAN])

    request = last_request()
    assert result == {"status": True}
    assert request.method == "POST"
    assert query_of(request) == {}
    assert json.loads(request.body) == {"route_id": ROUTE_ID, "route_destination_id": 42, "barcodes": [SCAN]}


def test_a_route_id_with_a_slash_is_encoded(client, mocked, last_request):
    mocked.add(responses.GET, ADDRESS_BARCODES_V5, json={"status": True, "data": []}, status=200)

    client.address_barcodes.get_address_barcodes(route_id="a/b")

    assert last_request().url == f"{ADDRESS_BARCODES_V5}?route_id=a%2Fb"


def test_get_address_barcodes_requires_a_route_id(client, mocked):
    with pytest.raises(ParamValueException) as excinfo:
        client.address_barcodes.get_address_barcodes(limit=10)

    assert excinfo.value.param == "route_id"
    assert not mocked.calls


def test_save_address_barcodes_names_every_missing_field(client, mocked):
    with pytest.raises(ParamValueException) as excinfo:
        client.address_barcodes.save_address_barcodes(route_id=ROUTE_ID)

    assert excinfo.value.param == "route_destination_id, barcodes"
    assert not mocked.calls


def test_an_api_error_is_returned_as_a_dict(client, mocked):
    mocked.add(
        responses.GET,
        ADDRESS_BARCODES_V5,
        json={"status": False, "code": 406, "messages": {"route_id": ["The route id is invalid."]}},
        status=406,
    )

    assert client.address_barcodes.get_address_barcodes(route_id=ROUTE_ID) == {"errors": ["The route id is invalid."]}
