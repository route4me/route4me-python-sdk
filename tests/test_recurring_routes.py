"""Request-level tests for :class:`route4me.recurring_routes.RecurringRoutes`.

Each test pins the HTTP method, URL, query and JSON body of one method. The
request guard in ``conftest.py`` also checks that every request goes to a
registered endpoint, with the key as a bearer token on API V5 and as
``api_key`` on API V4.
"""

import json

import pytest
import responses

from route4me.api_endpoints import (
    RECURRING_MASTER_ROUTES_V5,
    RECURRING_ROUTE_SCHEDULES_REPLACE_V5,
    RECURRING_ROUTE_SCHEDULES_V5,
    RECURRING_SCHEDULED_ROUTES_GET_COPIES_V5,
    RECURRING_SCHEDULED_ROUTES_IS_COPY_V5,
    RECURRING_SCHEDULES_V5,
    SCHEDULE_CALENDAR,
)
from route4me.exceptions import ParamValueException

ROUTE_ID = "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"
SCHEDULE_UID = "SCHEDULE-1"
RULES = [{"mode": "daily", "enabled": True, "daily": {"every": 1}}]
SCHEDULE = {
    "name": "Every weekday",
    "schedule": RULES,
    "advance_interval": 1,
    "advance_schedule_interval_days": 7,
    "timezone": "UTC",
}


def body_of(request):
    """Decode a JSON request body."""
    return json.loads(request.body)


class TestSchedules:
    def test_get_schedules_list(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, RECURRING_SCHEDULES_V5, json={"data": []}, status=200)

        assert client.recurring_routes.get_schedules_list() == {"data": []}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {}

    def test_create_schedule_posts_the_schedule(self, client, mocked, last_request):
        mocked.add(responses.POST, RECURRING_SCHEDULES_V5, json={"data": [SCHEDULE]}, status=200)

        client.recurring_routes.create_schedule(**SCHEDULE)

        assert last_request().method == "POST"
        assert body_of(last_request()) == SCHEDULE

    def test_create_schedule_names_the_missing_fields(self, client, mocked):
        with pytest.raises(ParamValueException) as error:
            client.recurring_routes.create_schedule(name="Every weekday", schedule=RULES)

        assert error.value.param == "advance_interval, advance_schedule_interval_days, timezone"
        assert not mocked.calls

    def test_get_schedule(self, client, mocked, last_request):
        url = f"{RECURRING_SCHEDULES_V5}/{SCHEDULE_UID}"
        mocked.add(responses.GET, url, json={"data": [SCHEDULE]}, status=200)

        assert client.recurring_routes.get_schedule(SCHEDULE_UID) == {"data": [SCHEDULE]}
        assert last_request().url == url

    def test_update_schedule_puts_the_changes(self, client, mocked, last_request):
        url = f"{RECURRING_SCHEDULES_V5}/{SCHEDULE_UID}"
        mocked.add(responses.PUT, url, json={"data": []}, status=200)

        client.recurring_routes.update_schedule(SCHEDULE_UID, name="Weekends")

        assert last_request().method == "PUT"
        assert last_request().url == url
        assert body_of(last_request()) == {"name": "Weekends"}

    @pytest.mark.parametrize(("with_routes", "sent"), [(False, "0"), (True, "1")])
    def test_delete_schedule_sends_with_routes_as_0_or_1(
        self, client, mocked, query_of, last_request, with_routes, sent
    ):
        mocked.add(responses.DELETE, f"{RECURRING_SCHEDULES_V5}/{SCHEDULE_UID}", json={"data": []}, status=200)

        client.recurring_routes.delete_schedule(SCHEDULE_UID, with_routes=with_routes)

        assert last_request().method == "DELETE"
        assert query_of(last_request()) == {"with-routes": sent}
        assert last_request().body is None

    def test_delete_schedule_keeps_the_routes_by_default(self, client, mocked, query_of, last_request):
        mocked.add(responses.DELETE, f"{RECURRING_SCHEDULES_V5}/{SCHEDULE_UID}", json={"data": []}, status=200)

        client.recurring_routes.delete_schedule(SCHEDULE_UID)

        assert query_of(last_request()) == {"with-routes": "0"}


class TestRouteSchedules:
    def test_get_route_schedules_list(self, client, mocked, last_request):
        mocked.add(responses.GET, RECURRING_ROUTE_SCHEDULES_V5, json={"data": []}, status=200)

        assert client.recurring_routes.get_route_schedules_list() == {"data": []}
        assert last_request().method == "GET"

    def test_create_route_schedule_posts_the_link(self, client, mocked, last_request):
        mocked.add(responses.POST, RECURRING_ROUTE_SCHEDULES_V5, json={"data": []}, status=200)

        client.recurring_routes.create_route_schedule(route_id=ROUTE_ID, schedule_uid=SCHEDULE_UID)

        assert last_request().method == "POST"
        assert body_of(last_request()) == {"route_id": ROUTE_ID, "schedule_uid": SCHEDULE_UID}

    def test_create_route_schedule_requires_the_schedule(self, client, mocked):
        with pytest.raises(ParamValueException) as error:
            client.recurring_routes.create_route_schedule(route_id=ROUTE_ID)

        assert error.value.param == "schedule_uid"
        assert not mocked.calls

    def test_get_route_schedule(self, client, mocked, last_request):
        url = f"{RECURRING_ROUTE_SCHEDULES_V5}/{ROUTE_ID}"
        mocked.add(responses.GET, url, json={"data": []}, status=200)

        client.recurring_routes.get_route_schedule(ROUTE_ID)

        assert (last_request().method, last_request().url) == ("GET", url)

    def test_update_route_schedule_puts_the_spec_fields(self, client, mocked, last_request):
        url = f"{RECURRING_ROUTE_SCHEDULES_V5}/{ROUTE_ID}"
        mocked.add(responses.PUT, url, json={"data": [], "status": True}, status=200)
        update = {"route_uid": ROUTE_ID, "schedule_uid": SCHEDULE_UID, "root_member_id": 1, "vehicle_id": "VEHICLE-1"}

        client.recurring_routes.update_route_schedule(ROUTE_ID, **update)

        assert (last_request().method, last_request().url) == ("PUT", url)
        assert body_of(last_request()) == update

    def test_update_route_schedule_names_the_missing_fields(self, client, mocked):
        with pytest.raises(ParamValueException) as error:
            client.recurring_routes.update_route_schedule(ROUTE_ID, schedule_uid=SCHEDULE_UID)

        assert error.value.param == "route_uid, root_member_id"
        assert not mocked.calls

    @pytest.mark.parametrize(
        ("method", "suffix"),
        [("delete_route_schedule", ""), ("delete_route_schedule_items", "/items")],
    )
    def test_deletes_go_to_the_route(self, client, mocked, last_request, method, suffix):
        url = f"{RECURRING_ROUTE_SCHEDULES_V5}/{ROUTE_ID}{suffix}"
        mocked.add(responses.DELETE, url, json={"status": True}, status=200)

        assert getattr(client.recurring_routes, method)(ROUTE_ID) == {"status": True}
        assert (last_request().method, last_request().url) == ("DELETE", url)
        assert last_request().body is None

    def test_get_route_schedule_preview_sends_the_date_range(self, client, mocked, query_of, last_request):
        url = f"{RECURRING_ROUTE_SCHEDULES_V5}/{ROUTE_ID}/preview"
        mocked.add(responses.GET, url, json={"dates": []}, status=200)

        client.recurring_routes.get_route_schedule_preview(ROUTE_ID, start="2026-11-01", end="2026-11-30")

        assert last_request().url.split("?")[0] == url
        assert query_of(last_request()) == {"start": "2026-11-01", "end": "2026-11-30"}

    def test_get_route_schedule_preview_requires_the_date_range(self, client, mocked):
        with pytest.raises(ParamValueException) as error:
            client.recurring_routes.get_route_schedule_preview(ROUTE_ID, start="2026-11-01")

        assert error.value.param == "end"
        assert not mocked.calls

    def test_replace_route_schedule_puts_the_new_schedule(self, client, mocked, last_request):
        url = f"{RECURRING_ROUTE_SCHEDULES_REPLACE_V5}/{ROUTE_ID}"
        mocked.add(responses.PUT, url, json={"data": []}, status=200)

        client.recurring_routes.replace_route_schedule(ROUTE_ID, schedule=RULES, timezone="UTC")

        assert (last_request().method, last_request().url) == ("PUT", url)
        assert body_of(last_request()) == {"schedule": RULES, "timezone": "UTC"}

    def test_replace_route_schedule_requires_the_schedule(self, client, mocked):
        with pytest.raises(ParamValueException):
            client.recurring_routes.replace_route_schedule(ROUTE_ID, timezone="UTC")

        assert not mocked.calls


class TestMasterRoutesAndCopies:
    def test_create_master_route_posts_the_route_and_schedule(self, client, mocked, last_request):
        mocked.add(responses.POST, RECURRING_MASTER_ROUTES_V5, json={"status": True}, status=200)

        client.recurring_routes.create_master_route(route_id=ROUTE_ID, schedule=RULES, name="Weekday route")

        assert last_request().method == "POST"
        assert body_of(last_request()) == {"route_id": ROUTE_ID, "schedule": RULES, "name": "Weekday route"}

    def test_create_master_route_requires_the_schedule(self, client, mocked):
        with pytest.raises(ParamValueException) as error:
            client.recurring_routes.create_master_route(route_id=ROUTE_ID)

        assert error.value.param == "schedule"
        assert not mocked.calls

    def test_is_route_schedule_copied(self, client, mocked, last_request):
        url = f"{RECURRING_SCHEDULED_ROUTES_IS_COPY_V5}/{ROUTE_ID}"
        mocked.add(responses.GET, url, json={"status": False}, status=200)

        assert client.recurring_routes.is_route_schedule_copied(ROUTE_ID) == {"status": False}
        assert (last_request().method, last_request().url) == ("GET", url)

    def test_get_route_schedule_copies_posts_the_route(self, client, mocked, last_request):
        reply = {"parent_route_id": ROUTE_ID, "scheduled_routes": []}
        mocked.add(responses.POST, RECURRING_SCHEDULED_ROUTES_GET_COPIES_V5, json=reply, status=200)

        result = client.recurring_routes.get_route_schedule_copies(route_id=ROUTE_ID, route_date="2026-11-02")

        assert result == reply
        assert body_of(last_request()) == {"route_id": ROUTE_ID, "route_date": "2026-11-02"}

    def test_get_route_schedule_copies_requires_the_route(self, client, mocked):
        with pytest.raises(ParamValueException):
            client.recurring_routes.get_route_schedule_copies(route_date="2026-11-02")

        assert not mocked.calls


class TestScheduleCalendar:
    def test_sends_the_query_with_flags_as_0_or_1(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.GET, SCHEDULE_CALENDAR, json={"orders": {}, "routes_count": {}}, status=200)

        client.recurring_routes.get_schedule_calendar(
            date_from_string="2026-11-01",
            date_to_string="2026-11-30",
            timezone_offset_minutes=-300,
            orders=True,
            ab=False,
            routes_count=True,
        )

        assert last_request().method == "GET"
        assert query_of(last_request()) == {
            "api_key": api_key,
            "date_from_string": "2026-11-01",
            "date_to_string": "2026-11-30",
            "timezone_offset_minutes": "-300",
            "orders": "1",
            "ab": "0",
            "routes_count": "1",
        }


class TestPathAndErrors:
    def test_a_route_id_cannot_escape_its_path_segment(self, client, mocked, last_request):
        url = f"{RECURRING_ROUTE_SCHEDULES_V5}/a%2Fb/items"
        mocked.add(responses.DELETE, url, json={"status": True}, status=200)

        client.recurring_routes.delete_route_schedule_items("a/b")

        assert last_request().url == url

    @pytest.mark.parametrize(
        "method",
        [
            "get_schedule",
            "update_schedule",
            "delete_schedule",
            "get_route_schedule",
            "update_route_schedule",
            "delete_route_schedule",
            "delete_route_schedule_items",
            "get_route_schedule_preview",
            "replace_route_schedule",
            "is_route_schedule_copied",
        ],
    )
    def test_an_empty_id_is_rejected_before_any_request(self, client, mocked, method):
        with pytest.raises(ParamValueException):
            getattr(client.recurring_routes, method)("")

        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.GET,
            f"{RECURRING_SCHEDULES_V5}/{SCHEDULE_UID}",
            json={"status": False, "code": 404, "messages": ["Schedule not found"]},
            status=404,
        )

        assert client.recurring_routes.get_schedule(SCHEDULE_UID) == {"errors": ["Schedule not found"]}
