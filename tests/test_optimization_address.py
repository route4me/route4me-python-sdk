"""Request-level tests for :class:`route4me.optimization.Optimization` and
:class:`route4me.address.Address`."""

import json
from urllib.parse import parse_qs

import pytest
import responses

from route4me.api_endpoints import ADD_ROUTE_NOTES_HOST, ADDRESS_HOST, API_HOST, BATCH_GEOCODER, SINGLE_GEOCODER
from route4me.exceptions import ParamValueException

OPTIMIZATION_ID = "0F3B8C2D5E7A419B6C8D0E2F4A6B8C1D"
ROUTE_ID = "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"
DESTINATION_ID = 98765
ADDRESS = {"address": "754 5th Ave New York, NY 10019", "lat": 40.7636197, "lng": -73.9744388}


class TestOptimizationReads:
    def test_get_optimizations(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.GET, API_HOST, json={"optimizations": []}, status=200)

        client.optimization.get_optimizations(limit=5, offset=0)

        assert query_of(last_request()) == {"limit": "5", "offset": "0", "api_key": api_key}

    def test_get_optimization(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, API_HOST, json={"optimization_problem_id": OPTIMIZATION_ID}, status=200)

        result = client.optimization.get_optimization(optimization_problem_id=OPTIMIZATION_ID)

        assert result["optimization_problem_id"] == OPTIMIZATION_ID
        assert query_of(last_request())["optimization_problem_id"] == OPTIMIZATION_ID

    @pytest.mark.parametrize(
        ("method", "kwargs"),
        [
            ("get_optimizations", {"limit": 5}),
            ("get_optimization", {}),
            ("update_optimization", {"optimization_problem_id": OPTIMIZATION_ID}),
            ("delete_optimization", {}),
            ("delete_address_from_optimization", {"optimization_problem_id": OPTIMIZATION_ID}),
        ],
    )
    def test_missing_required_parameters_raise(self, client, method, kwargs):
        with pytest.raises(ParamValueException):
            getattr(client.optimization, method)(**kwargs)


class TestOptimizationWrites:
    def test_update_optimization_is_a_put(self, client, mocked, last_request):
        mocked.add(responses.PUT, API_HOST, json={}, status=200)

        client.optimization.update_optimization(
            optimization_problem_id=OPTIMIZATION_ID, addresses=[ADDRESS], reoptimize=1
        )

        assert last_request().method == "PUT"

    def test_update_optimization_sends_the_addresses_as_json(self, client, mocked, last_request):
        mocked.add(responses.PUT, API_HOST, json={}, status=200)

        client.optimization.update_optimization(
            optimization_problem_id=OPTIMIZATION_ID, addresses=[ADDRESS], reoptimize=1
        )

        assert json.loads(last_request().body) == {"addresses": [ADDRESS]}

    def test_update_optimization_sends_the_problem_id_in_the_query(self, client, mocked, query_of, last_request):
        mocked.add(responses.PUT, API_HOST, json={}, status=200)

        client.optimization.update_optimization(
            optimization_problem_id=OPTIMIZATION_ID, addresses=[ADDRESS], reoptimize=1
        )

        query = query_of(last_request())
        assert (query["optimization_problem_id"], query["reoptimize"]) == (OPTIMIZATION_ID, "1")

    def test_update_optimization_keeps_the_key_out_of_the_body(self, client, mocked, last_request, api_key):
        mocked.add(responses.PUT, API_HOST, json={}, status=200)

        client.optimization.update_optimization(
            optimization_problem_id=OPTIMIZATION_ID, addresses=[ADDRESS], reoptimize=1
        )

        assert api_key not in last_request().body.decode()

    @pytest.mark.parametrize(("reoptimize", "sent"), [(True, "1"), (False, "0"), (1, "1")])
    def test_update_optimization_sends_reoptimize_as_0_or_1(
        self, client, mocked, query_of, last_request, reoptimize, sent
    ):
        """``True`` used to reach the API as ``reoptimize=True``."""
        mocked.add(responses.PUT, API_HOST, json={}, status=200)

        client.optimization.update_optimization(
            optimization_problem_id=OPTIMIZATION_ID, addresses=[ADDRESS], reoptimize=reoptimize
        )

        assert query_of(last_request())["reoptimize"] == sent

    def test_delete_optimization_sends_the_ids_as_json(self, client, mocked, last_request):
        mocked.add(responses.DELETE, API_HOST, json={"status": True}, status=200)

        client.optimization.delete_optimization(optimization_problem_ids=[OPTIMIZATION_ID])

        assert last_request().method == "DELETE"
        assert json.loads(last_request().body) == {"optimization_problem_ids": [OPTIMIZATION_ID]}

    def test_delete_address_from_optimization(self, client, mocked, query_of, last_request):
        mocked.add(responses.DELETE, ADDRESS_HOST, json={"deleted": True}, status=200)

        client.optimization.delete_address_from_optimization(
            optimization_problem_id=OPTIMIZATION_ID, route_destination_id=DESTINATION_ID
        )

        assert query_of(last_request())["route_destination_id"] == str(DESTINATION_ID)


class TestOptimizationBuilders:
    def test_set_slowdowns_writes_both_values(self, client):
        client.optimization.set_slowdowns(10, 20)

        assert client.optimization.data["parameters"]["slowdowns"] == {"service_time": 10, "travel_time": 20}

    def test_set_order_aggregation_groups(self, client):
        client.optimization.set_order_aggregation_groups(["2026-10-01"], "agg-1", ["new"], {"x": 1}, split=False)

        groups = client.optimization.data["order_aggregation_groups"]
        assert groups["split"] is False
        assert groups["filters"] == {"scheduled_for_range": ["2026-10-01"], "order_status": ["new"]}

    def test_route_start_date_local_rejects_a_bad_date(self, client):
        with pytest.raises(ParamValueException):
            client.optimization.route_start_date_local("10/21/2026")

    def test_route_start_date_local_accepts_an_iso_date(self, client):
        client.optimization.route_start_date_local("2026-10-21")

        assert client.optimization.data["parameters"]["route_start_date_local"] == "2026-10-21"


class TestAddressCollection:
    def test_add_address_stages_it_on_the_optimization(self, client):
        client.address.add_address(**ADDRESS)

        assert client.address.get_addresses() == [ADDRESS]
        assert client.optimization.data["addresses"] == [ADDRESS]

    @pytest.mark.parametrize("extra", [{"order_id": 1}, {"contact_id": 2}])
    def test_an_order_or_contact_id_can_stand_in_for_coordinates(self, client, extra):
        client.address.add_address(**extra)

        assert client.address.get_addresses() == [extra]

    def test_an_address_without_coordinates_or_ids_is_rejected(self, client):
        with pytest.raises(ParamValueException):
            client.address.add_address(address="nowhere")

    def test_get_route_id_reads_the_last_response(self, client):
        client.address.response = {"route_id": ROUTE_ID}

        assert client.address.get_route_id() == ROUTE_ID


class TestAddressRequests:
    def test_get_address(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, ADDRESS_HOST, json={"route_destination_id": DESTINATION_ID}, status=200)

        result = client.address.get_address(ROUTE_ID, DESTINATION_ID)

        assert result == {"route_destination_id": DESTINATION_ID}
        assert query_of(last_request())["route_id"] == ROUTE_ID

    def test_get_address_notes_asks_for_notes(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, ADDRESS_HOST, json={"notes": []}, status=200)

        client.address.get_address_notes(ROUTE_ID, DESTINATION_ID)

        assert query_of(last_request())["notes"] == "1"

    def test_get_address_returns_the_error_dict(self, client, mocked):
        mocked.add(responses.GET, ADDRESS_HOST, json={"errors": ["Not found"]}, status=404)

        assert client.address.get_address(ROUTE_ID, DESTINATION_ID) == {"errors": ["Not found"]}

    def test_update_address_puts_json(self, client, mocked, last_request):
        mocked.add(responses.PUT, ADDRESS_HOST, json={}, status=200)

        client.address.update_address({"is_departed": True}, ROUTE_ID, DESTINATION_ID)

        assert last_request().method == "PUT"
        assert json.loads(last_request().body) == {"is_departed": True}

    def test_delete_address_from_route(self, client, mocked, last_request):
        mocked.add(responses.DELETE, ADDRESS_HOST, json={"deleted": True}, status=200)

        assert client.address.delete_address_from_route(ROUTE_ID, DESTINATION_ID) == {"deleted": True}
        assert last_request().method == "DELETE"

    def test_add_address_notes_posts_a_form(self, client, mocked, query_of, last_request):
        mocked.add(responses.POST, ADD_ROUTE_NOTES_HOST, json={"status": True}, status=200)

        client.address.add_address_notes(
            "Left at door", address_id=DESTINATION_ID, route_id=ROUTE_ID, activity_type="dropoff"
        )

        assert query_of(last_request())["route_id"] == ROUTE_ID
        assert parse_qs(last_request().body) == {"strUpdateType": ["dropoff"], "strNoteContents": ["Left at door"]}

    def test_add_address_notes_without_an_activity_type(self, client, mocked):
        mocked.add(responses.POST, ADD_ROUTE_NOTES_HOST, json={"status": True}, status=200)

        client.address.add_address_notes("Left at door", address_id=DESTINATION_ID, route_id=ROUTE_ID)


class TestGeocoding:
    def test_get_geocode(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, SINGLE_GEOCODER, json=[ADDRESS], status=200)

        assert client.address.get_geocode({"format": "json", "address": ADDRESS["address"]}) == [ADDRESS]
        assert query_of(last_request())["address"] == ADDRESS["address"]
        assert not last_request().body

    def test_batch_geocodes_posts_the_addresses_as_a_form(self, client, mocked, last_request):
        mocked.add(responses.POST, BATCH_GEOCODER, json=[], status=200)

        client.address.get_batch_geocodes({"format": "json"}, {"addresses": "a||b"})

        assert parse_qs(last_request().body) == {"addresses": ["a||b"]}

    def test_fix_geocode_merges_the_result(self, client, mocked):
        mocked.add(responses.GET, SINGLE_GEOCODER, json={"lat": 1.5, "lng": 2.5}, status=200)

        error, address = client.address.fix_geocode({"address": "x"})

        assert error is None
        assert (address["lat"], address["lng"]) == (1.5, 2.5)

    def test_batch_fix_geocodes_updates_matched_addresses(self, client, mocked):
        mocked.add(
            responses.POST,
            BATCH_GEOCODER,
            json=[{"original": "1 Main St", "lat": 1.0, "lng": 2.0}],
            status=200,
        )
        stops = [{"address": "1 Main St"}]

        errors, addresses = client.address.batch_fix_geocodes(stops)

        assert errors == []
        assert addresses[0]["lat"] == 1.0

    def test_batch_fix_geocodes_reports_an_unmatched_address(self, client, mocked):
        mocked.add(
            responses.POST,
            BATCH_GEOCODER,
            json=[{"original": "somewhere else", "lat": 1.0, "lng": 2.0}],
            status=200,
        )

        errors, _ = client.address.batch_fix_geocodes([{"address": "1 Main St"}])

        assert len(errors) == 1

    def test_geocode_sends_the_addresses_in_the_body(self, client, mocked, query_of, last_request):
        mocked.add(responses.POST, BATCH_GEOCODER, body=b"csv", status=200)

        client.address.geocode(addresses="1 Main St||2 Main St")

        assert "addresses" not in query_of(last_request())

    def test_geocode_requires_addresses(self, client):
        with pytest.raises(ParamValueException):
            client.address.geocode()


class TestGeocodingReplies:
    """The geocoder answers with a list of results, or the error dict."""

    def test_fix_geocode_takes_the_first_result_of_a_list(self, client, mocked):
        mocked.add(
            responses.GET,
            SINGLE_GEOCODER,
            json=[{"address": "x", "lat": 1.5, "lng": 2.5, "type": "street"}, {"lat": 9.0, "lng": 9.0}],
            status=200,
        )
        stop = {"address": "x"}

        error, address = client.address.fix_geocode(stop)

        assert error is None
        assert address == {"address": "x", "lat": 1.5, "lng": 2.5}

    def test_fix_geocode_reports_an_api_error_as_a_failure(self, client, mocked):
        mocked.add(responses.GET, SINGLE_GEOCODER, json={"errors": ["Invalid API key"]}, status=401)
        stop = {"address": "x"}

        error, address = client.address.fix_geocode(stop)

        assert error is stop
        assert address == {"address": "x"}

    def test_batch_fix_geocodes_reports_every_address_on_an_api_error(self, client, mocked):
        mocked.add(responses.POST, BATCH_GEOCODER, json={"errors": ["Invalid API key"]}, status=401)
        stops = [{"address": "1 Main St"}, {"address": "2 Main St"}]

        errors, addresses = client.address.batch_fix_geocodes(stops)

        assert errors == stops
        assert addresses is stops

    def test_geocode_keeps_the_format_in_the_query(self, client, mocked, query_of, last_request):
        mocked.add(responses.POST, BATCH_GEOCODER, body=b"csv", status=200)

        client.address.geocode(addresses="1 Main St||2 Main St")

        assert query_of(last_request())["format"] == "csv"
        assert parse_qs(last_request().body) == {"addresses": ["1 Main St||2 Main St"]}


class TestAddressLookups:
    def test_get_address_notes_returns_the_error_dict(self, client, mocked):
        mocked.add(responses.GET, ADDRESS_HOST, json={"errors": ["Not found"]}, status=404)

        assert client.address.get_address_notes(ROUTE_ID, DESTINATION_ID) == {"errors": ["Not found"]}

    def test_request_address_leaves_the_callers_dict_alone(self, client, mocked):
        mocked.add(responses.GET, ADDRESS_HOST, json={}, status=200)
        params = {"route_id": ROUTE_ID, "route_destination_id": DESTINATION_ID}

        client.address.request_address(params)

        assert params == {"route_id": ROUTE_ID, "route_destination_id": DESTINATION_ID}

    def test_route_ids_come_from_the_last_lookup(self, client, mocked):
        mocked.add(
            responses.GET,
            ADDRESS_HOST,
            json={"route_id": ROUTE_ID, "route_destination_id": DESTINATION_ID},
            status=200,
        )

        client.address.get_address(ROUTE_ID, DESTINATION_ID)

        assert client.address.get_route_id() == ROUTE_ID
        assert client.address.get_route_destination_id() == DESTINATION_ID

    def test_route_ids_before_any_request_raise(self, client):
        with pytest.raises(ParamValueException):
            client.address.get_route_id()
