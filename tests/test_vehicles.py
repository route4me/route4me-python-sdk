"""Vehicle resource tests.

Previously this file made a real HTTPS call with the dummy key and was
documented as "fails by design". It now runs against a recorded payload.
"""

import responses

from route4me.api_endpoints import VEHICLES_HOST


class TestGetVehicles:
    def test_returns_the_vehicle_list(self, client, mocked, load_fixture):
        mocked.add(responses.GET, VEHICLES_HOST, json=load_fixture("vehicles"), status=200)

        result = client.vehicles.get_vehicles()

        assert len(result) == 2
        for field in ("vehicle_id", "vehicle_alias", "member_id", "created_time"):
            assert field in result[0], f"{field} missing from the vehicle payload"

    def test_sends_the_api_key(self, client, mocked, load_fixture, query_of, last_request, api_key):
        mocked.add(responses.GET, VEHICLES_HOST, json=load_fixture("vehicles"), status=200)

        client.vehicles.get_vehicles()

        assert query_of(last_request())["api_key"] == api_key

    def test_api_error_is_returned_not_raised(self, client, mocked, load_fixture):
        mocked.add(responses.GET, VEHICLES_HOST, json=load_fixture("error_v4"), status=401)

        result = client.vehicles.get_vehicles()

        assert result == {"errors": ["The API key is invalid."]}
