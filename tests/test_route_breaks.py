"""Request-level tests for :class:`route4me.route_breaks.RouteBreaks`.

The four "insert a break after ..." operations of the Java SDK are one
endpoint with a different break ``type``; each is pinned here.
"""

import json

import pytest
import responses

from route4me.api_endpoints import ROUTE_BREAKS_V5
from route4me.route_breaks import ROUTE_BREAK_TYPE

ROUTE_ID = "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"
OTHER_ROUTE_ID = "BADC0DE0BADC0DE0BADC0DE0BADC0DE0"


class TestRouteBreaks:
    @pytest.mark.parametrize(
        "break_type",
        [
            ROUTE_BREAK_TYPE.CERTAIN_NUMBER_OF_TOTAL_ELAPSED_TIME,
            ROUTE_BREAK_TYPE.CERTAIN_NUMBER_OF_LOCATIONS,
            ROUTE_BREAK_TYPE.CERTAIN_NUMBER_OF_SERVICE_TIME,
            ROUTE_BREAK_TYPE.CERTAIN_NUMBER_OF_TRAVEL_TIME,
            ROUTE_BREAK_TYPE.APPROXIMATE_TIME_OF_DAY,
        ],
    )
    def test_posts_the_breaks(self, client, mocked, last_request, query_of, break_type):
        mocked.add(responses.POST, ROUTE_BREAKS_V5, json={"status": True}, status=200)
        breaks = [{"type": break_type, "duration": 900, "params": [3600, 3600]}]

        result = client.route_breaks.insert_route_breaks([ROUTE_ID, OTHER_ROUTE_ID], breaks, True)

        assert result == {"status": True}
        assert last_request().method == "POST"
        assert query_of(last_request()) == {}
        assert json.loads(last_request().body) == {
            "route_id": [ROUTE_ID, OTHER_ROUTE_ID],
            "breaks": breaks,
            "replace_existing_breaks": True,
        }

    def test_a_single_route_id_is_sent_as_a_list(self, client, mocked, last_request):
        mocked.add(responses.POST, ROUTE_BREAKS_V5, json={"status": True}, status=200)

        client.route_breaks.insert_route_breaks(ROUTE_ID, [], replace_existing_breaks=False)

        body = json.loads(last_request().body)
        assert body["route_id"] == [ROUTE_ID]
        assert body["replace_existing_breaks"] is False

    def test_the_break_types_match_the_spec_enum(self):
        assert sorted(ROUTE_BREAK_TYPE.reverse_mapping) == [
            "approximate_time_of_day",
            "certain_number_of_locations",
            "certain_number_of_service_time",
            "certain_number_of_total_elapsed_time",
            "certain_number_of_travel_time",
        ]

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.POST, ROUTE_BREAKS_V5, json={"errors": ["The breaks field is required."]}, status=406)

        assert client.route_breaks.insert_route_breaks([ROUTE_ID], [], True) == {
            "errors": ["The breaks field is required."]
        }
