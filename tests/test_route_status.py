"""Request-level tests for :meth:`route4me.route_status.RouteStatus.set_route_stop_status`.

The route-level methods of :class:`~route4me.route_status.RouteStatus` are
covered in ``tests/test_v5_resources.py``.
"""

import json

import pytest
import responses

from route4me.api_endpoints import ROUTE_STOP_STATUS_V5
from route4me.exceptions import ParamValueException


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

    def test_requires_destinations(self, client, mocked):
        with pytest.raises(ParamValueException) as raised:
            client.route_status.set_route_stop_status("Failed")

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
