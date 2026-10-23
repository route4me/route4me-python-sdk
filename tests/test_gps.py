import json
import unittest

import pytest
import responses

from route4me.api_endpoints import SET_GPS_HOST, USER_LOCATIONS_HOST, VEHICLE_LOCATIONS_V5
from route4me.exceptions import ParamValueException
from tests.base import Route4MeAPITestSuite

ROUTE_ID = "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"
PING = {"member_id": 1, "device_guid": "DEVICE-1", "route_id": ROUTE_ID, "lat": 40.7, "lng": -73.9, "speed": 12.9}


class Route4MeGPSTests(Route4MeAPITestSuite):
    """
    Route4Me Optimization Tests
    """

    def test_set_valid_device_timestamp(self):
        """
        Valid Timestamp
        :return:
        """
        gps = self.route4me.gps
        device_timestamp = "2014-36-99 57:83:85"
        return self.assertRaises(ParamValueException, gps.device_timestamp, device_timestamp)

    def test_param_dict_validation(self):
        gps = self.route4me.gps
        self.assertRaises(ParamValueException, gps.add, {"xxxx": 100})


class TestTrackingPings:
    def test_one_ping_is_posted_as_the_json_body(self, client, mocked, last_request, query_of, api_key):
        mocked.add(responses.POST, SET_GPS_HOST, json={"status": True, "tx_id": "TX-1"}, status=200)

        result = client.gps.set_tracking_pings(**PING)

        assert result == {"status": True, "tx_id": "TX-1"}
        assert last_request().method == "POST"
        assert query_of(last_request()) == {"api_key": api_key}
        assert json.loads(last_request().body) == PING

    def test_a_batch_is_posted_in_items(self, client, mocked, last_request):
        mocked.add(responses.POST, SET_GPS_HOST, json={"status": True, "items_errors": []}, status=200)
        items = [{"lat": 40.7, "lng": -73.9, "device_timestamp": 1792600000}, {"lat": 40.8, "lng": -74.0}]

        client.gps.set_tracking_pings(member_id=1, device_guid="DEVICE-1", items=items)

        assert json.loads(last_request().body) == {"member_id": 1, "device_guid": "DEVICE-1", "items": items}

    @pytest.mark.parametrize("field", ["lat", "lng"])
    def test_one_ping_needs_lat_and_lng(self, client, mocked, field):
        ping = {k: v for k, v in PING.items() if k != field}

        with pytest.raises(ParamValueException) as excinfo:
            client.gps.set_tracking_pings(**ping)

        assert field in str(excinfo.value)
        assert not mocked.calls

    def test_the_setters_do_not_leak_into_the_body(self, client, mocked, last_request):
        mocked.add(responses.POST, SET_GPS_HOST, json={"status": True}, status=200)
        client.gps.lat(33.1)

        client.gps.set_tracking_pings(**PING)

        assert json.loads(last_request().body)["lat"] == PING["lat"]

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.POST, SET_GPS_HOST, json={"errors": ["Field items can have at most 100 items"]}, status=400
        )

        assert client.gps.set_tracking_pings(items=[{"lat": 1, "lng": 1}] * 101) == {
            "errors": ["Field items can have at most 100 items"]
        }


class TestUserLocations:
    def test_gets_every_user_location(self, client, mocked, last_request, query_of, api_key):
        mocked.add(responses.GET, USER_LOCATIONS_HOST, json=[{"member_data": {"member_id": 1}}], status=200)

        assert client.gps.get_user_locations() == [{"member_data": {"member_id": 1}}]
        assert last_request().method == "GET"
        assert query_of(last_request()) == {"api_key": api_key}

    def test_searches_with_a_query(self, client, mocked, last_request, query_of, api_key):
        mocked.add(responses.GET, USER_LOCATIONS_HOST, json=[], status=200)

        client.gps.get_user_locations(query="driver@example.com")

        assert query_of(last_request()) == {"api_key": api_key, "query": "driver@example.com"}

    def test_a_search_does_not_leak_into_the_next_call(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, USER_LOCATIONS_HOST, json=[], status=200)
        client.gps.get_user_locations(query="driver@example.com")

        client.gps.get_user_locations()

        assert "query" not in query_of(last_request())

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.GET, USER_LOCATIONS_HOST, json={"errors": ["Authentication failed"]}, status=401)

        assert client.gps.get_user_locations() == {"errors": ["Authentication failed"]}


class TestVehicleLocations:
    def test_sends_each_vehicle_id_as_a_bracketed_query_key(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, VEHICLE_LOCATIONS_V5, json={"data": []}, status=200)

        result = client.gps.get_vehicle_locations(["VEHICLE-1", "VEHICLE-2"])

        assert result == {"data": []}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {"ids[]": ["VEHICLE-1", "VEHICLE-2"]}

    def test_a_single_vehicle_id_is_sent_as_a_list(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, VEHICLE_LOCATIONS_V5, json={"data": []}, status=200)

        client.gps.get_vehicle_locations("VEHICLE-1")

        assert query_of(last_request()) == {"ids[]": "VEHICLE-1"}

    @pytest.mark.parametrize("vehicle_ids", [[], ""])
    def test_needs_a_vehicle_id(self, client, mocked, vehicle_ids):
        with pytest.raises(ParamValueException):
            client.gps.get_vehicle_locations(vehicle_ids)

        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.GET,
            VEHICLE_LOCATIONS_V5,
            json={"status": False, "code": 406, "messages": {"vehicle_ids": ["The vehicle ids field is required."]}},
            status=406,
        )

        assert client.gps.get_vehicle_locations(["VEHICLE-1"]) == {"errors": ["The vehicle ids field is required."]}


if __name__ == "__main__":
    unittest.main()


class TestCoordinateSetters:
    """The coordinate and altitude setters of every resource (#126, #129)."""

    @pytest.mark.parametrize("value", [10, 0, -73, 40.7636197])
    @pytest.mark.parametrize("setter", ["lat", "lng", "altitude", "cached_lat", "cached_lng"])
    def test_whole_and_decimal_numbers_are_accepted(self, client, setter, value):
        getattr(client.gps, setter)(value)

        assert client.gps.params[setter] == value

    @pytest.mark.parametrize("value", [True, "40.7", None])
    @pytest.mark.parametrize("setter", ["lat", "lng", "altitude", "cached_lat", "cached_lng"])
    def test_booleans_and_text_are_rejected(self, client, setter, value):
        with pytest.raises(ParamValueException):
            getattr(client.gps, setter)(value)

    def test_cached_coordinates_keep_their_own_keys(self, client):
        """cached_lat and cached_lng wrote lat and lng, overwriting them."""
        gps = client.gps
        gps.lat(12.3)
        gps.lng(45.6)
        gps.cached_lat(78.9)
        gps.cached_lng(10.1)

        assert {key: gps.params[key] for key in ("lat", "lng", "cached_lat", "cached_lng")} == {
            "lat": 12.3,
            "lng": 45.6,
            "cached_lat": 78.9,
            "cached_lng": 10.1,
        }
