"""Request-level tests for :class:`route4me.asset_tracking.AssetTracking`."""

import responses

from route4me.api_endpoints import ASSET_TRACKING


class TestAssetTracking:
    def test_find_asset_sends_the_tracking_number(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, ASSET_TRACKING, json={"tracking_number": "TRACK-1"}, status=200)

        assert client.asset_tracking.find_asset("TRACK-1") == {"tracking_number": "TRACK-1"}
        assert last_request().method == "GET"
        assert last_request().url.split("?")[0] == ASSET_TRACKING
        assert query_of(last_request()) == {"api_key": client.key, "tracking": "TRACK-1"}

    def test_an_unknown_tracking_number_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.GET, ASSET_TRACKING, json={"errors": ["Please enter a valid tracking number."]}, status=400
        )

        assert client.asset_tracking.find_asset("TRACK-0") == {"errors": ["Please enter a valid tracking number."]}
