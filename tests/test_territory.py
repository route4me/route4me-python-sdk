"""Territory resource tests.

The previous contents of this file were a verbatim copy of
``test_utils.py::test_json2obj`` -- a test about JSON deserialisation, living
in a file named for territories, under a method named ``test_get_vehicles``.
It asserted nothing about any of the three. Replaced with real coverage of
``route4me.territory.Territory``.
"""

import json

import pytest
import responses

from route4me.api_endpoints import TERRITORY_HOST
from route4me.exceptions import ParamValueException

TERRITORY_ID = "0F3B8C2D5E7A419B6C8D0E2F4A6B8C1D"

VALID_TERRITORY = {
    "territory_name": "Manhattan Midtown",
    "territory_color": "ff0000",
    "territory": {"type": "circle", "data": ["40.7636197,-73.9744388", "5000"]},
}


class TestGetTerritories:
    def test_returns_the_territory_list(self, client, mocked, load_fixture):
        mocked.add(responses.GET, TERRITORY_HOST, json=load_fixture("territories"), status=200)

        result = client.territory.get_territories()

        assert len(result) == 2
        assert result[0]["territory_id"] == TERRITORY_ID

    def test_sends_the_api_key(self, client, mocked, load_fixture, query_of, last_request, api_key):
        mocked.add(responses.GET, TERRITORY_HOST, json=load_fixture("territories"), status=200)

        client.territory.get_territories()

        assert query_of(last_request())["api_key"] == api_key


class TestGetTerritory:
    def test_returns_a_single_territory(self, client, mocked, load_fixture):
        mocked.add(responses.GET, TERRITORY_HOST, json=load_fixture("territory"), status=200)

        result = client.territory.get_territory(territory_id=TERRITORY_ID)

        assert result["territory_id"] == TERRITORY_ID
        assert result["territory"]["type"] == "circle"

    def test_sends_the_territory_id(self, client, mocked, load_fixture, query_of, last_request):
        mocked.add(responses.GET, TERRITORY_HOST, json=load_fixture("territory"), status=200)

        client.territory.get_territory(territory_id=TERRITORY_ID)

        assert query_of(last_request())["territory_id"] == TERRITORY_ID

    def test_missing_territory_id_raises(self, client):
        with pytest.raises(ParamValueException):
            client.territory.get_territory()


class TestAddTerritory:
    def test_posts_the_territory_as_a_json_body(self, client, mocked, load_fixture, last_request):
        mocked.add(responses.POST, TERRITORY_HOST, json=load_fixture("territory"), status=200)

        result = client.territory.add_territory(**VALID_TERRITORY)

        assert result["territory_id"] == TERRITORY_ID
        assert json.loads(last_request().body) == VALID_TERRITORY

    @pytest.mark.parametrize("missing", ["territory_name", "territory_color", "territory"])
    def test_each_required_field_is_enforced(self, client, missing):
        payload = {k: v for k, v in VALID_TERRITORY.items() if k != missing}

        with pytest.raises(ParamValueException):
            client.territory.add_territory(**payload)


class TestUpdateTerritory:
    def test_puts_the_territory_id_as_a_query_param(self, client, mocked, load_fixture, query_of, last_request):
        mocked.add(responses.PUT, TERRITORY_HOST, json=load_fixture("territory"), status=200)

        client.territory.update_territory(TERRITORY_ID, **VALID_TERRITORY)

        request = last_request()
        assert request.method == "PUT"
        assert query_of(request)["territory_id"] == TERRITORY_ID
        assert json.loads(request.body) == VALID_TERRITORY

    def test_incomplete_payload_raises(self, client):
        with pytest.raises(ParamValueException):
            client.territory.update_territory(TERRITORY_ID, territory_name="Only a name")


class TestDeleteTerritory:
    def test_sends_a_delete_with_the_territory_id(self, client, mocked, load_fixture, query_of, last_request):
        mocked.add(responses.DELETE, TERRITORY_HOST, json=load_fixture("territory_deleted"), status=200)

        result = client.territory.delete_territory(territory_id=TERRITORY_ID)

        assert result == {"status": True}
        request = last_request()
        assert request.method == "DELETE"
        assert query_of(request)["territory_id"] == TERRITORY_ID

    def test_missing_territory_id_raises(self, client):
        with pytest.raises(ParamValueException):
            client.territory.delete_territory()
