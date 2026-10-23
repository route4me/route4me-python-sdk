"""Request-level tests for :class:`route4me.members.Members` and :class:`route4me.gps.GPS`."""

import json
from urllib.parse import parse_qs

import pytest
import responses

from route4me.api_endpoints import (
    DEVICE_LOCATION_URL,
    GET_USERS_HOST,
    MEMBER_AUTHENTICATE,
    REGISTER_ACTION,
    SET_GPS_HOST,
    USER_LICENSE_HOST,
    USER_URL,
    VALIDATE_SESSION,
    VERIFY_DEVICE_LICENSE,
    WEBINAR_REGISTER,
)
from route4me.exceptions import ParamValueException

ROUTE_ID = "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"
MEMBER_ID = 123456

LICENSE = {
    "member_id": MEMBER_ID,
    "session_guid": "abc",
    "device_id": "device-1",
    "device_type": "iphone",
    "subscription_name": "IPAD_MONTHLY",
    "token": "receipt-token",
    "payload": "receipt-payload",
    "format": "json",
}
REGISTRATION = {
    "industry": "Gifting",
    "first_name": "Ada",
    "last_name": "Lovelace",
    "email_address": "ada@example.com",
    "check_terms": 1,
    "device_type": "web",
    "plan": "enterprise_plan",
    "password_1": "s3cret!",
    "password_2": "s3cret!",
    "format": "json",
}
WEBINAR = {
    "email_address": "ada@example.com",
    "first_name": "Ada",
    "last_name": "Lovelace",
    "phone_number": "555-0100",
    "company_name": "Analytical Engines",
    "member_id": MEMBER_ID,
}


class TestMembersPosts:
    @pytest.mark.parametrize(
        ("method", "endpoint", "kwargs"),
        [
            ("app_purchase_user_license", USER_LICENSE_HOST, LICENSE),
            (
                "verify_device_license",
                VERIFY_DEVICE_LICENSE,
                {"device_id": "d", "device_type": "iphone", "format": "json"},
            ),
        ],
    )
    def test_posts_the_kwargs_as_json(self, client, mocked, last_request, method, endpoint, kwargs):
        mocked.add(responses.POST, endpoint, json={"status": True}, status=200)

        result = getattr(client.members, method)(**dict(kwargs))

        assert result == {"status": True}
        assert last_request().method == "POST"
        assert json.loads(last_request().body) == kwargs

    def test_authenticate_renames_the_credentials(self, client, mocked, last_request):
        mocked.add(responses.POST, MEMBER_AUTHENTICATE, json={"status": True}, status=200)

        client.members.member_authenticate(email="ada@example.com", password="s3cret!")

        assert json.loads(last_request().body) == {"strEmail": "ada@example.com", "strPassword": "s3cret!"}

    def test_authenticate_never_puts_the_password_in_the_url(self, client, mocked, last_request):
        mocked.add(responses.POST, MEMBER_AUTHENTICATE, json={"status": True}, status=200)

        client.members.member_authenticate(email="ada@example.com", password="s3cret!")

        assert "s3cret" not in last_request().url

    def test_register_sends_the_plan_in_the_query_and_the_rest_as_a_form(self, client, mocked, query_of, last_request):
        mocked.add(responses.POST, REGISTER_ACTION, json={"status": True}, status=200)

        client.members.register(**dict(REGISTRATION))

        assert query_of(last_request()) == {"plan": "enterprise_plan", "api_key": client.key}
        form = parse_qs(last_request().body)
        assert form["strEmail"] == ["ada@example.com"]
        assert form["strPassword_1"] == ["s3cret!"]
        assert "s3cret" not in last_request().url

    def test_a_non_json_reply_is_returned_raw(self, client, mocked):
        mocked.add(responses.POST, VERIFY_DEVICE_LICENSE, body=b"Missing or Invalid Device ID", status=200)

        result = client.members.verify_device_license(device_id="d", device_type="iphone", format="json")

        assert result == b"Missing or Invalid Device ID"

    @pytest.mark.parametrize(
        ("method", "kwargs"),
        [
            ("app_purchase_user_license", {"member_id": MEMBER_ID}),
            ("verify_device_license", {"device_id": "d"}),
            ("member_authenticate", {"email": "ada@example.com"}),
            ("validate_session", {"member_id": MEMBER_ID}),
            ("webinar_registration", {"email_address": "ada@example.com"}),
            ("register", {"first_name": "Ada"}),
        ],
    )
    def test_missing_required_parameters_raise(self, client, method, kwargs):
        with pytest.raises(ParamValueException):
            getattr(client.members, method)(**kwargs)


class TestMissingParameters:
    def test_the_error_names_the_missing_parameters(self, client):
        with pytest.raises(ParamValueException) as excinfo:
            client.members.member_authenticate(email="ada@example.com")

        assert excinfo.value.param == "password"


class TestWebinarRegistration:
    def test_posts_a_form(self, client, mocked, last_request):
        mocked.add(responses.POST, WEBINAR_REGISTER, json={"status": True}, status=200)

        client.members.webinar_registration(webinar_date="2026-11-01 10:00:00", **WEBINAR)

        assert parse_qs(last_request().body)["email_address"] == ["ada@example.com"]

    def test_sends_webinar_date(self, client, mocked, last_request):
        mocked.add(responses.POST, WEBINAR_REGISTER, json={"status": True}, status=200)

        client.members.webinar_registration(webinar_date="2026-11-01 10:00:00", **WEBINAR)

        assert parse_qs(last_request().body)["webinar_date"] == ["2026-11-01 10:00:00"]

    def test_the_old_misspelling_still_works_with_a_warning(self, client, mocked, last_request):
        mocked.add(responses.POST, WEBINAR_REGISTER, json={"status": True}, status=200)

        with pytest.warns(DeprecationWarning):
            client.members.webinar_registration(webiinar_date="2026-11-01 10:00:00", **WEBINAR)

        form = parse_qs(last_request().body)
        assert form["webinar_date"] == ["2026-11-01 10:00:00"]
        assert "webiinar_date" not in form


class TestMembersGets:
    @pytest.mark.parametrize(
        ("method", "endpoint", "kwargs"),
        [
            ("get_users", GET_USERS_HOST, {"limit": 10, "offset": 0}),
            ("get_api_key_users", USER_URL, {}),
            ("validate_session", VALIDATE_SESSION, {"session_guid": "abc", "member_id": MEMBER_ID}),
        ],
    )
    def test_sends_kwargs_as_query_parameters(self, client, mocked, query_of, last_request, method, endpoint, kwargs):
        mocked.add(responses.GET, endpoint, json={"ok": True}, status=200)

        result = getattr(client.members, method)(**kwargs)

        assert result == {"ok": True}
        assert last_request().method == "GET"
        expected = {k: str(v) for k, v in kwargs.items()}
        expected["api_key"] = client.key
        assert query_of(last_request()) == expected

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.GET, USER_URL, json={"errors": ["Invalid API key"]}, status=401)

        assert client.members.get_api_key_users() == {"errors": ["Invalid API key"]}


class TestGPS:
    POSITION = {
        "format": "json",
        "member_id": MEMBER_ID,
        "route_id": ROUTE_ID,
        "course": 1,
        "speed": 120,
        "lat": 41.8927521,
        "lng": -109.0803888,
        "device_type": "iphone",
        "device_guid": "TEST_GPS",
        "device_timestamp": "2026-10-21 11:15:00",
    }

    def test_set_gps_track_is_a_get_with_query_parameters(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, SET_GPS_HOST, json={"status": True}, status=200)

        client.gps.set_gps_track(**self.POSITION)

        assert last_request().method == "GET"
        assert last_request().body is None
        assert query_of(last_request())["route_id"] == ROUTE_ID

    def test_set_gps_track_requires_every_field(self, client):
        position = dict(self.POSITION)
        del position["lat"]

        with pytest.raises(ParamValueException):
            client.gps.set_gps_track(**position)

    def test_get_locations(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, DEVICE_LOCATION_URL, json=[], status=200)

        client.gps.get_locations(format="json", route_id=ROUTE_ID, member_id=MEMBER_ID, time_period="today")

        assert query_of(last_request())["time_period"] == "today"

    def test_get_locations_requires_a_time_period(self, client):
        with pytest.raises(ParamValueException):
            client.gps.get_locations(format="json", route_id=ROUTE_ID, member_id=MEMBER_ID)
