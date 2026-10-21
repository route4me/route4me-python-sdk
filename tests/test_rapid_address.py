"""Tests for ``route4me/rapid_address.py``.

This was the worst-covered module in the package (13.2%) and also the one with
the injection surface, a dead code path, and an ``UnboundLocalError`` in its
error handler.
"""

import re

import pytest
import responses

from route4me.api_endpoints import RAPID_ADDRESS, RAPID_ADDRESS_SERVICE, RAPID_ADDRESS_ZIP
from route4me.exceptions import ParamValueException

STREET_DATA = [{"zipcode": "00602", "street": "Calle 1"}]

#: Catch-all so a test can assert on whatever URL the SDK actually built.
ANY_RAPID_URL = re.compile(r"https://rapid\.route4me\.com/.*")


# The street-data endpoints are retired; these tests pin the request shape the
# deprecated methods still send.
pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")


@pytest.mark.filterwarnings("default::DeprecationWarning")
@pytest.mark.parametrize(
    ("method", "kwargs"),
    [
        ("get_street_data", {}),
        ("get_street_data_zip", {"zipcode": "00602"}),
        ("get_street_data_service", {"zipcode": "00602", "housenumber": "17"}),
    ],
)
def test_every_street_data_method_is_deprecated(client, mocked, method, kwargs):
    mocked.add(responses.GET, re.compile(r"https://rapid\.route4me\.com/street_data/.*"), json=[], status=200)

    with pytest.warns(DeprecationWarning, match="no replacement"):
        getattr(client.rapid_address, method)(**kwargs)


class TestGetStreetData:
    def test_a_pk_lands_in_the_path(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{RAPID_ADDRESS}PK1/", json=STREET_DATA, status=200)

        result = client.rapid_address.get_street_data(pk="PK1")

        assert result == STREET_DATA
        assert last_request().url.startswith(f"{RAPID_ADDRESS}PK1/")

    def test_offset_and_limit_actually_issue_a_request(self, client, mocked, last_request):
        """Regression: this branch used to build a URL and then fall off the end
        of the function, returning None without ever calling the API."""
        mocked.add(responses.GET, f"{RAPID_ADDRESS}10/20/", json=STREET_DATA, status=200)

        result = client.rapid_address.get_street_data(offset=10, limit=20)

        assert result == STREET_DATA
        assert last_request().url.startswith(f"{RAPID_ADDRESS}10/20/")

    def test_no_arguments_still_issues_a_request(self, client, mocked):
        """Regression: previously returned None without calling the API."""
        mocked.add(responses.GET, RAPID_ADDRESS, json=STREET_DATA, status=200)

        assert client.rapid_address.get_street_data() == STREET_DATA

    def test_a_traversal_attempt_cannot_escape_the_path(self, client, mocked, last_request):
        mocked.add(responses.GET, ANY_RAPID_URL, json=STREET_DATA, status=200)

        client.rapid_address.get_street_data(pk="../../admin")

        url = last_request().url
        assert "/admin" not in url
        assert "..%2F..%2Fadmin" in url

    def test_an_api_error_is_returned_not_raised(self, client, mocked):
        mocked.add(responses.GET, RAPID_ADDRESS, json={"errors": ["nope"]}, status=400)

        assert client.rapid_address.get_street_data() == {"errors": ["nope"]}

    def test_a_non_json_body_returns_raw_content(self, client, mocked):
        mocked.add(responses.GET, RAPID_ADDRESS, body="plain text", status=200)

        assert client.rapid_address.get_street_data() == b"plain text"

    def test_an_error_before_the_response_exists_does_not_raise_unbound_local(self, client, mocked):
        """Regression: the old handler was
        ``except ValueError: return response.content`` wrapped around the
        request itself, so a failure before the assignment died with
        UnboundLocalError and hid the real error."""
        mocked.add(responses.GET, RAPID_ADDRESS, body="not json", status=500)

        result = client.rapid_address.get_street_data()

        assert result == {"errors": ["Unexpected server response"]}


class TestGetStreetDataZip:
    def test_the_zipcode_lands_in_the_path(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{RAPID_ADDRESS_ZIP}00602/", json=STREET_DATA, status=200)

        result = client.rapid_address.get_street_data_zip(zipcode="00602")

        assert result == STREET_DATA
        assert last_request().url.startswith(f"{RAPID_ADDRESS_ZIP}00602/")

    def test_pagination_is_appended_after_the_zipcode(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{RAPID_ADDRESS_ZIP}00602/1/5/", json=STREET_DATA, status=200)

        client.rapid_address.get_street_data_zip(zipcode="00602", offset=1, limit=5)

        assert last_request().url.startswith(f"{RAPID_ADDRESS_ZIP}00602/1/5/")

    def test_a_missing_zipcode_raises(self, client):
        with pytest.raises(ParamValueException):
            client.rapid_address.get_street_data_zip()

    def test_an_injected_zipcode_is_encoded(self, client, mocked, last_request):
        mocked.add(responses.GET, ANY_RAPID_URL, json=STREET_DATA, status=200)

        client.rapid_address.get_street_data_zip(zipcode="00602/../../secret")

        assert "/secret" not in last_request().url

    def test_a_non_integer_offset_raises(self, client):
        with pytest.raises(ParamValueException):
            client.rapid_address.get_street_data_zip(zipcode="00602", offset="abc", limit=5)


class TestGetStreetDataService:
    def test_zipcode_and_housenumber_land_in_the_path(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{RAPID_ADDRESS_SERVICE}00602/17/", json=STREET_DATA, status=200)

        result = client.rapid_address.get_street_data_service(zipcode="00602", housenumber="17")

        assert result == STREET_DATA
        assert last_request().url.startswith(f"{RAPID_ADDRESS_SERVICE}00602/17/")

    def test_pagination_is_appended(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{RAPID_ADDRESS_SERVICE}00602/17/1/5/", json=STREET_DATA, status=200)

        client.rapid_address.get_street_data_service(zipcode="00602", housenumber="17", offset=1, limit=5)

        assert last_request().url.startswith(f"{RAPID_ADDRESS_SERVICE}00602/17/1/5/")

    @pytest.mark.parametrize("missing", ["zipcode", "housenumber"])
    def test_each_required_field_is_enforced(self, client, missing):
        payload = {"zipcode": "00602", "housenumber": "17"}
        del payload[missing]

        with pytest.raises(ParamValueException):
            client.rapid_address.get_street_data_service(**payload)

    def test_an_injected_housenumber_is_encoded(self, client, mocked, last_request):
        mocked.add(responses.GET, ANY_RAPID_URL, json=STREET_DATA, status=200)

        client.rapid_address.get_street_data_service(zipcode="00602", housenumber="17/../../secret")

        assert "/secret" not in last_request().url


class TestApiKeyIsSent:
    def test_the_api_key_is_still_a_query_parameter(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.GET, RAPID_ADDRESS, json=STREET_DATA, status=200)

        client.rapid_address.get_street_data()

        assert query_of(last_request())["api_key"] == api_key
