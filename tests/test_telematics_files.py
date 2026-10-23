"""Request-level tests for :class:`route4me.telematics.Telematics` and
:class:`route4me.file_uploading.FileUploading`."""

import io
import json

import pytest
import responses

from route4me.api_endpoints import (
    FILE_UPLOAD_GEOCODE_HOST,
    FILE_UPLOAD_HOST,
    FILE_UPLOAD_PREVIEW_HOST,
    TELEMATICS_CONNECTIONS_V4,
    TELEMATICS_REGISTER_V4,
    TELEMATICS_VENDORS_INFO_V4,
    TELEMATICS_VENDORS_V4,
)
from route4me.exceptions import ParamValueException
from route4me.telematics import Telematics

API_TOKEN = "telematics-api-token"
CONNECTION_TOKEN = "connection-token"
UPLOAD_ID = "upload-0001"


class TestTelematicsVendors:
    """The vendor directory lives on telematics.route4me.com, which is retired."""

    def test_get_vendors(self, client, mocked, last_request):
        mocked.add(responses.GET, TELEMATICS_VENDORS_V4, json={"vendors": []}, status=200)

        assert client.telematics.get_vendors() == {"vendors": []}
        assert last_request().method == "GET"

    def test_get_vendor_sends_the_vendor_id(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, TELEMATICS_VENDORS_V4, json={"vendor": {}}, status=200)

        client.telematics.get_vendor(55)

        assert query_of(last_request())["vendor_id"] == "55"

    def test_search_vendor_sends_the_filters(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, TELEMATICS_VENDORS_V4, json={"vendors": []}, status=200)

        client.telematics.search_vendor(country="GB", is_integrated=1, page=1, per_page=5)

        query = query_of(last_request())
        assert (query["country"], query["is_integrated"], query["per_page"]) == ("GB", "1", "5")

    def test_compare_vendors_sends_the_ids(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, TELEMATICS_VENDORS_V4, json={"vendors": []}, status=200)

        client.telematics.compare_vendors("55,56,57")

        assert query_of(last_request())["vendors"] == "55,56,57"

    @pytest.mark.xfail(
        strict=True, raises=AssertionError, reason="#36: get_vendor leaves vendor_id in Telematics.params"
    )
    def test_get_vendor_does_not_leak_into_get_vendors(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, TELEMATICS_VENDORS_V4, json={}, status=200)
        client.telematics.get_vendor(55)

        client.telematics.get_vendors()

        assert "vendor_id" not in query_of(last_request())

    @pytest.mark.xfail(
        strict=True, raises=AssertionError, reason="#36: compare_vendors leaves vendors in Telematics.params"
    )
    def test_compare_vendors_does_not_leak_into_get_vendors(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, TELEMATICS_VENDORS_V4, json={}, status=200)
        client.telematics.compare_vendors("55,56")

        client.telematics.get_vendors()

        assert "vendors" not in query_of(last_request())


class TestTelematicsConnections:
    def test_register_member(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, TELEMATICS_REGISTER_V4, json={"api_token": API_TOKEN}, status=200)

        client.telematics.register_member(123456)

        assert query_of(last_request())["member_id"] == "123456"

    @pytest.mark.parametrize(
        ("method", "endpoint"),
        [("get_connections", TELEMATICS_CONNECTIONS_V4), ("get_vendors_info", TELEMATICS_VENDORS_INFO_V4)],
    )
    def test_token_listings(self, client, mocked, query_of, last_request, method, endpoint):
        mocked.add(responses.GET, endpoint, json=[], status=200)

        getattr(client.telematics, method)(API_TOKEN)

        assert query_of(last_request())["api_token"] == API_TOKEN

    def test_register_connection_validates_the_credentials_remotely(self, client, mocked, query_of, last_request):
        mocked.add(responses.POST, TELEMATICS_CONNECTIONS_V4, json={"connection_token": CONNECTION_TOKEN}, status=200)

        client.telematics.register_connection(API_TOKEN, vendor_id=55, account_id="acct", username="u", password="p")

        assert last_request().method == "POST"
        body = json.loads(last_request().body)
        assert body["validate_remote_credentials"] == "true"
        assert body["vendor_id"] == 55
        assert "password" not in last_request().url

    @pytest.mark.parametrize(
        ("method", "verb"),
        [("get_connection", responses.GET), ("delete_connection", responses.DELETE)],
    )
    def test_connection_lookups(self, client, mocked, query_of, last_request, method, verb):
        mocked.add(verb, TELEMATICS_CONNECTIONS_V4, json={}, status=200)

        getattr(client.telematics, method)(API_TOKEN, CONNECTION_TOKEN)

        assert last_request().method == verb
        assert query_of(last_request())["connection_token"] == CONNECTION_TOKEN

    def test_update_connection_puts_json(self, client, mocked, query_of, last_request):
        mocked.add(responses.PUT, TELEMATICS_CONNECTIONS_V4, json={}, status=200)

        client.telematics.update_connection(API_TOKEN, CONNECTION_TOKEN, vendor_id=55, metadata="x")

        assert last_request().method == "PUT"
        assert json.loads(last_request().body)["metadata"] == "x"

    @pytest.mark.parametrize("method", ["register_connection", "update_connection"])
    def test_a_vendor_id_is_required(self, client, method):
        args = (API_TOKEN,) if method == "register_connection" else (API_TOKEN, CONNECTION_TOKEN)

        with pytest.raises(ParamValueException):
            getattr(client.telematics, method)(*args)

    def test_delete_connection_returns_the_error_dict(self, client, mocked):
        mocked.add(responses.DELETE, TELEMATICS_CONNECTIONS_V4, json={"errors": ["Not found"]}, status=404)

        assert client.telematics.delete_connection(API_TOKEN, CONNECTION_TOKEN) == {"errors": ["Not found"]}


class TestPrettyPrinters:
    def test_pp_response_writes_one_line_per_key(self):
        out = io.StringIO()

        Telematics.pp_response({"a": 1, "b": 2}, file=out)

        assert out.getvalue() == "a : 1\nb : 2\n\n"

    def test_pp_vendor_comparison_writes_a_tab_separated_row(self):
        out = io.StringIO()

        Telematics.pp_vendor_comparison({"id": 55, "name": "Geotab", "features": [{"name": "GPS"}]}, file=out)

        assert out.getvalue() == "55\tGeotab\tGPS\n"


class TestFileUploading:
    def test_preview_is_a_get_returning_raw_content(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, FILE_UPLOAD_PREVIEW_HOST, body=b"preview", status=200)

        assert client.file_uploading.get_file_preview(strUploadID=UPLOAD_ID, format="json") == b"preview"
        assert query_of(last_request())["strUploadID"] == UPLOAD_ID

    def test_upload_sends_the_file_as_multipart(self, client, mocked, last_request):
        mocked.add(responses.POST, FILE_UPLOAD_HOST, body=b'{"optimization_problem_id": "x"}', status=200)

        client.file_uploading.upload_file(files={"strFilename": ("stops.csv", b"address\n1 Main St\n")}, format="json")

        assert last_request().method == "POST"
        assert last_request().headers["Content-Type"].startswith("multipart/form-data")
        assert b"1 Main St" in last_request().body

    def test_upload_does_not_put_the_file_in_the_query(self, client, mocked, query_of, last_request):
        mocked.add(responses.POST, FILE_UPLOAD_HOST, body=b"{}", status=200)

        client.file_uploading.upload_file(files={"strFilename": ("stops.csv", b"x")}, format="json")

        assert "files" not in query_of(last_request())

    def test_upload_geocode(self, client, mocked, query_of, last_request):
        mocked.add(responses.POST, FILE_UPLOAD_GEOCODE_HOST, body=b"{}", status=200)

        client.file_uploading.upload_file_geocode(strUploadID=UPLOAD_ID, files={"strFilename": ("a.csv", b"x")})

        assert query_of(last_request())["strUploadID"] == UPLOAD_ID

    @pytest.mark.parametrize(
        ("method", "kwargs"),
        [
            ("get_file_preview", {"format": "json"}),
            ("upload_file", {"format": "json"}),
            ("upload_file_geocode", {"strUploadID": UPLOAD_ID}),
        ],
    )
    def test_missing_required_parameters_raise(self, client, method, kwargs):
        with pytest.raises(ParamValueException):
            getattr(client.file_uploading, method)(**kwargs)

    def test_an_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.GET, FILE_UPLOAD_PREVIEW_HOST, json={"errors": ["Invalid API key"]}, status=401)

        assert client.file_uploading.get_file_preview(strUploadID=UPLOAD_ID, format="json") == {
            "errors": ["Invalid API key"]
        }
