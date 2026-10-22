"""Request-level tests for :class:`route4me.orders_v5.OrdersV5`.

Each test pins the HTTP method, URL, query and JSON body of one method. The
request guard in ``conftest.py`` also checks that every request goes to a
registered endpoint and carries the key as a bearer token only.
"""

import json

import pytest
import responses

from route4me.api_endpoints import (
    ORDERS_ARCHIVE_V5,
    ORDERS_CUSTOM_FIELDS_V5,
    ORDERS_HISTORY_V5,
    ORDERS_PLATFORM_BATCH_DELETE_V5,
    ORDERS_PLATFORM_BATCH_UPDATE_FILTER_V5,
    ORDERS_PLATFORM_BATCH_UPDATE_V5,
    ORDERS_PLATFORM_CUSTOM_USER_FIELDS_V5,
)
from route4me.exceptions import ParamValueException

ORDER_UUID = "ORDER-UUID-1"
FIELD_UUID = "FIELD-UUID-1"
FIELD_ID = 7
CUSTOM_USER_FIELD = {
    "order_custom_field_name": "cf_gate",
    "order_custom_field_type": "text",
    "order_custom_field_label": "Gate code",
    "order_custom_field_type_info": {"short_label": "Gate"},
}


def body_of(request):
    """Decode a JSON request body."""
    return json.loads(request.body)


class TestOrders:
    def test_archive_orders_posts_the_page_request(self, client, mocked, query_of, last_request):
        mocked.add(responses.POST, ORDERS_ARCHIVE_V5, json={"items": [], "next_page_cursor": None}, status=200)

        result = client.orders_v5.archive_orders(per_page=10, filters={"statuses": [1]})

        assert result == {"items": [], "next_page_cursor": None}
        assert last_request().method == "POST"
        assert query_of(last_request()) == {}
        assert body_of(last_request()) == {"per_page": 10, "filters": {"statuses": [1]}}

    def test_get_order_history_sends_the_query(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, ORDERS_HISTORY_V5, json={"results": []}, status=200)

        assert client.orders_v5.get_order_history(order_uuid=ORDER_UUID) == {"results": []}
        assert last_request().method == "GET"
        assert last_request().body is None
        assert query_of(last_request()) == {"order_uuid": ORDER_UUID}

    def test_get_order_history_keeps_no_state_between_calls(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, ORDERS_HISTORY_V5, json={"results": []}, status=200)
        client.orders_v5.get_order_history(order_id=5)

        client.orders_v5.get_order_history(tracking_number="TRACK-1")

        assert query_of(last_request()) == {"tracking_number": "TRACK-1"}

    @pytest.mark.parametrize(
        ("method", "http", "url", "kwargs"),
        [
            ("batch_delete", "POST", ORDERS_PLATFORM_BATCH_DELETE_V5, {"order_ids": [ORDER_UUID]}),
            (
                "batch_update",
                "POST",
                ORDERS_PLATFORM_BATCH_UPDATE_V5,
                {"order_ids": [ORDER_UUID], "data": {"color": "ff0000"}},
            ),
            (
                "batch_update_filter",
                "PUT",
                ORDERS_PLATFORM_BATCH_UPDATE_FILTER_V5,
                {"data": {"color": "ff0000"}, "filters": {"statuses": [1]}},
            ),
        ],
    )
    def test_batch_actions_send_the_body(self, client, mocked, query_of, last_request, method, http, url, kwargs):
        mocked.add(http, url, json={"status": True}, status=200)

        assert getattr(client.orders_v5, method)(**kwargs) == {"status": True}
        assert last_request().method == http
        assert last_request().url.split("?")[0] == url
        assert query_of(last_request()) == {}
        assert body_of(last_request()) == kwargs


class TestCustomUserFields:
    def test_get_custom_user_fields(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, ORDERS_PLATFORM_CUSTOM_USER_FIELDS_V5, json={"data": []}, status=200)

        assert client.orders_v5.get_custom_user_fields() == {"data": []}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {}

    def test_create_custom_user_fields_posts_the_field(self, client, mocked, last_request):
        mocked.add(responses.POST, ORDERS_PLATFORM_CUSTOM_USER_FIELDS_V5, json={"data": {}}, status=200)

        client.orders_v5.create_custom_user_fields(**CUSTOM_USER_FIELD)

        assert last_request().method == "POST"
        assert body_of(last_request()) == CUSTOM_USER_FIELD

    def test_create_custom_user_fields_names_the_missing_fields(self, client, mocked):
        with pytest.raises(ParamValueException) as error:
            client.orders_v5.create_custom_user_fields(order_custom_field_name="cf_gate")

        assert error.value.param == "order_custom_field_type, order_custom_field_label, order_custom_field_type_info"
        assert not mocked.calls

    def test_update_custom_user_fields_puts_to_the_field_uuid(self, client, mocked, last_request):
        url = f"{ORDERS_PLATFORM_CUSTOM_USER_FIELDS_V5}/{FIELD_UUID}"
        mocked.add(responses.PUT, url, json={"data": {}}, status=200)
        update = {key: value for key, value in CUSTOM_USER_FIELD.items() if key != "order_custom_field_name"}

        client.orders_v5.update_custom_user_fields(FIELD_UUID, **update)

        assert last_request().method == "PUT"
        assert last_request().url == url
        assert body_of(last_request()) == update

    def test_update_custom_user_fields_requires_the_spec_fields(self, client, mocked):
        with pytest.raises(ParamValueException):
            client.orders_v5.update_custom_user_fields(FIELD_UUID, order_custom_field_label="Gate")

        assert not mocked.calls

    def test_delete_custom_user_fields(self, client, mocked, last_request):
        url = f"{ORDERS_PLATFORM_CUSTOM_USER_FIELDS_V5}/{FIELD_UUID}"
        mocked.add(responses.DELETE, url, json={"data": {}}, status=200)

        assert client.orders_v5.delete_custom_user_fields(FIELD_UUID) == {"data": {}}
        assert last_request().method == "DELETE"
        assert last_request().url == url
        assert last_request().body is None

    def test_a_field_uuid_cannot_escape_its_path_segment(self, client, mocked, last_request):
        url = f"{ORDERS_PLATFORM_CUSTOM_USER_FIELDS_V5}/a%2Fb"
        mocked.add(responses.DELETE, url, json={"data": {}}, status=200)

        client.orders_v5.delete_custom_user_fields("a/b")

        assert last_request().url == url

    @pytest.mark.parametrize("method", ["update_custom_user_fields", "delete_custom_user_fields"])
    def test_an_empty_field_uuid_is_rejected_before_any_request(self, client, mocked, method):
        with pytest.raises(ParamValueException):
            getattr(client.orders_v5, method)("")

        assert not mocked.calls


class TestOrderCustomFields:
    def test_get_order_custom_fields(self, client, mocked, last_request):
        reply = {"status": True, "code": 200, "data": []}
        mocked.add(responses.GET, ORDERS_CUSTOM_FIELDS_V5, json=reply, status=200)

        assert client.orders_v5.get_order_custom_fields() == reply
        assert last_request().method == "GET"

    def test_create_order_custom_field_posts_the_field(self, client, mocked, last_request):
        mocked.add(responses.POST, ORDERS_CUSTOM_FIELDS_V5, json={"status": True, "data": {}}, status=200)
        field = {
            "order_custom_field_name": "cf_gate",
            "order_custom_field_label": "Gate code",
            "order_custom_field_type": "text",
        }

        client.orders_v5.create_order_custom_field(**field)

        assert last_request().method == "POST"
        assert body_of(last_request()) == field

    def test_create_order_custom_field_names_the_missing_fields(self, client, mocked):
        with pytest.raises(ParamValueException) as error:
            client.orders_v5.create_order_custom_field(order_custom_field_type="text")

        assert error.value.param == "order_custom_field_name, order_custom_field_label"
        assert not mocked.calls

    def test_update_order_custom_field_puts_to_the_field_id(self, client, mocked, last_request):
        url = f"{ORDERS_CUSTOM_FIELDS_V5}/{FIELD_ID}"
        mocked.add(responses.PUT, url, json={"status": True, "data": {}}, status=200)

        client.orders_v5.update_order_custom_field(FIELD_ID, order_custom_field_label="Gate")

        assert last_request().method == "PUT"
        assert last_request().url == url
        assert body_of(last_request()) == {"order_custom_field_label": "Gate"}

    def test_delete_order_custom_field_sends_the_id_in_the_path(self, client, mocked, last_request):
        url = f"{ORDERS_CUSTOM_FIELDS_V5}/{FIELD_ID}"
        mocked.add(responses.DELETE, url, json={"status": True, "code": 200}, status=200)

        assert client.orders_v5.delete_order_custom_field(str(FIELD_ID)) == {"status": True, "code": 200}
        assert last_request().method == "DELETE"
        assert last_request().url == url

    @pytest.mark.parametrize("field_id", ["", "a/b", None, -1])
    @pytest.mark.parametrize("method", ["update_order_custom_field", "delete_order_custom_field"])
    def test_a_bad_field_id_is_rejected_before_any_request(self, client, mocked, method, field_id):
        with pytest.raises(ParamValueException):
            getattr(client.orders_v5, method)(field_id)

        assert not mocked.calls


class TestErrors:
    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.POST,
            ORDERS_PLATFORM_BATCH_DELETE_V5,
            json={"status": False, "code": 403, "messages": {"order_ids": ["Forbidden"]}},
            status=403,
        )

        assert client.orders_v5.batch_delete(order_ids=[ORDER_UUID]) == {"errors": ["Forbidden"]}
