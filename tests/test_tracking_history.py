"""Request-level tests for :class:`route4me.tracking_history.TrackingHistory`.

The spec declares the export as POST with a JSON body; the issue's GET is not
what the API documents.
"""

import json

import responses

from route4me.api_endpoints import TRACKING_HISTORY_EXPORT_V5


class TestTrackingHistory:
    def test_export_posts_the_fields_and_returns_a_csv_file_as_bytes(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, TRACKING_HISTORY_EXPORT_V5, body=b"lat,lng\n40.7,-73.9\n", status=200)

        result = client.tracking_history.export_tracking_history(member_id=1, format="csv", time_period="today")

        assert result == b"lat,lng\n40.7,-73.9\n"
        assert last_request().method == "POST"
        assert query_of(last_request()) == {}
        assert json.loads(last_request().body) == {"member_id": 1, "format": "csv", "time_period": "today"}

    def test_export_decodes_a_json_reply(self, client, mocked):
        mocked.add(responses.POST, TRACKING_HISTORY_EXPORT_V5, json={"data": [{"lat": 40.7}]}, status=200)

        assert client.tracking_history.export_tracking_history(format="json") == {"data": [{"lat": 40.7}]}

    def test_export_returns_an_xml_reply_as_bytes(self, client, mocked):
        mocked.add(responses.POST, TRACKING_HISTORY_EXPORT_V5, body=b"<tracking/>", status=200)

        assert client.tracking_history.export_tracking_history(format="xml") == b"<tracking/>"

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.POST, TRACKING_HISTORY_EXPORT_V5, json={"errors": ["Invalid format"]}, status=406)

        assert client.tracking_history.export_tracking_history(format="pdf") == {"errors": ["Invalid format"]}
