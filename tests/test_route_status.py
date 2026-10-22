"""Request-level tests for the stop and bulk methods of :class:`~route4me.route_status.RouteStatus`.

:meth:`~route4me.route_status.RouteStatus.set_route_stop_status` and
:meth:`~route4me.route_status.RouteStatus.update_route_status_as_planned` are
tested here; the route-level methods are covered in ``tests/test_v5_resources.py``.
"""

import json

import pytest
import responses

from route4me.api_endpoints import ROUTE_STATUS_PLANNED_V5, ROUTE_STOP_STATUS_V5
from route4me.exceptions import ParamValueException

ROUTE_IDS = ["C0FFEE00C0FFEE00C0FFEE00C0FFEE00", "BADC0DE0BADC0DE0BADC0DE0BADC0DE0"]


class TestSetRouteStopStatus:
    def test_posts_the_ids_and_the_status(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, ROUTE_STOP_STATUS_V5, json={"status": True}, status=200)

        result = client.route_status.set_route_stop_status("Completed", destination_ids=[101, 102])

        assert result == {"status": True}
        assert last_request().method == "POST"
        assert query_of(last_request()) == {}
        assert json.loads(last_request().body) == {"status": "Completed", "destination_ids": [101, 102]}

    def test_posts_the_uuids_and_the_timestamp(self, client, mocked, last_request):
        mocked.add(responses.POST, ROUTE_STOP_STATUS_V5, json={"status": True}, status=200)

        client.route_status.set_route_stop_status(
            "Skipped", destination_uuids=["C0FFEE00C0FFEE00C0FFEE00C0FFEE00"], event_timestamp=1792600000
        )

        assert json.loads(last_request().body) == {
            "status": "Skipped",
            "destination_uuids": ["C0FFEE00C0FFEE00C0FFEE00C0FFEE00"],
            "event_timestamp": 1792600000,
        }

    @pytest.mark.parametrize(
        "kwargs", [{}, {"destination_ids": [101], "destination_uuids": ["C0FFEE00C0FFEE00C0FFEE00C0FFEE00"]}]
    )
    def test_requires_either_ids_or_uuids(self, client, mocked, kwargs):
        with pytest.raises(ParamValueException) as raised:
            client.route_status.set_route_stop_status("Failed", **kwargs)

        assert raised.value.param == "destination_ids, destination_uuids"
        assert not mocked.calls

    @pytest.mark.parametrize("status", ["", None])
    def test_requires_a_status(self, client, mocked, status):
        with pytest.raises(ParamValueException) as raised:
            client.route_status.set_route_stop_status(status, destination_ids=[101])

        assert raised.value.param == "status"
        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.POST,
            ROUTE_STOP_STATUS_V5,
            json={"status": False, "code": 406, "messages": {"status": ["The selected status is invalid."]}},
            status=406,
        )

        result = client.route_status.set_route_stop_status("Done", destination_ids=[101])

        assert result == {"errors": ["The selected status is invalid."]}


class TestUpdateRouteStatusAsPlanned:
    def test_posts_the_route_ids(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, ROUTE_STATUS_PLANNED_V5, json={"data": []}, status=200)

        assert client.route_status.update_route_status_as_planned(tuple(ROUTE_IDS)) == {"data": []}
        assert last_request().method == "POST"
        assert last_request().url.split("?")[0] == ROUTE_STATUS_PLANNED_V5
        assert query_of(last_request()) == {}
        assert json.loads(last_request().body) == {"route_ids": ROUTE_IDS}

    @pytest.mark.parametrize("route_ids", [None, [], "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"])
    def test_needs_a_non_empty_list(self, client, mocked, route_ids):
        with pytest.raises(ParamValueException) as error:
            client.route_status.update_route_status_as_planned(route_ids)

        assert error.value.param == "route_ids"
        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.POST,
            ROUTE_STATUS_PLANNED_V5,
            json={"status": False, "code": 422, "messages": {"route_ids": ["The route_ids field is required."]}},
            status=422,
        )

        result = client.route_status.update_route_status_as_planned(ROUTE_IDS)

        assert result == {"errors": ["The route_ids field is required."]}
