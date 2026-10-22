"""Request-level tests for the API V4 :class:`route4me.orders.Order` methods added in 1.0.0.

Covers the order filter, the order updates feed and the order custom user
fields. Each test pins the HTTP method, URL, query and JSON body.
"""

import json

import pytest
import responses

from route4me.api_endpoints import ORDER_CUSTOM_USER_FIELDS, ORDERS_HOST, ORDERS_UPDATES

FIELD_ID = 7


def body_of(request):
    """Decode a JSON request body."""
    return json.loads(request.body)


class TestGetOrders:
    def test_get_orders_sends_the_page_and_filters_in_the_query(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.GET, ORDERS_HOST, json={"results": [], "total": 0}, status=200)

        result = client.order.get_orders(limit=10, offset=0, day_added_YYMMDD="2026-10-22")

        assert result == {"results": [], "total": 0}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {
            "api_key": api_key,
            "limit": "10",
            "offset": "0",
            "day_added_YYMMDD": "2026-10-22",
        }
        assert last_request().body is None

    def test_get_orders_keeps_no_state_between_calls(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.GET, ORDERS_HOST, json={"results": []}, status=200)
        client.order.get_orders(query="Example")

        client.order.get_orders()

        assert query_of(last_request()) == {"api_key": api_key}


class TestFilterAndUpdates:
    def test_filter_orders_sends_the_filter_as_the_body_and_the_page_as_the_query(
        self, client, mocked, query_of, last_request, api_key
    ):
        mocked.add(responses.POST, ORDERS_HOST, json={"results": [], "total": 0}, status=200)
        body = {"filter": {"display": "all", "statuses": [1]}}

        result = client.order.filter_orders(body, limit=10, offset=0)

        assert result == {"results": [], "total": 0}
        assert last_request().method == "POST"
        assert query_of(last_request()) == {"api_key": api_key, "limit": "10", "offset": "0"}
        assert body_of(last_request()) == body

    def test_filter_orders_keeps_no_state_between_calls(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.POST, ORDERS_HOST, json={"results": []}, status=200)
        client.order.filter_orders({"filter": {}}, limit=10)

        client.order.filter_orders({"filter": {}})

        assert query_of(last_request()) == {"api_key": api_key}

    def test_get_orders_updates_sends_the_timestamp(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.GET, ORDERS_UPDATES, json={"orders": []}, status=200)

        client.order.get_orders_updates(last_known_ts=1792600000)

        assert last_request().method == "GET"
        assert query_of(last_request()) == {"api_key": api_key, "last_known_ts": "1792600000"}


class TestOrderCustomUserFields:
    def test_get_order_custom_user_fields(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.GET, ORDER_CUSTOM_USER_FIELDS, json={"data": []}, status=200)

        assert client.order.get_order_custom_user_fields() == {"data": []}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {"api_key": api_key}

    @pytest.mark.parametrize(
        ("method", "http", "kwargs"),
        [
            (
                "create_order_custom_user_field",
                "POST",
                {
                    "order_custom_field_name": "cf_gate",
                    "order_custom_field_label": "Gate code",
                    "order_custom_field_type": "text",
                    "order_custom_field_type_info": {"short_label": "Gate"},
                },
            ),
            (
                "update_order_custom_user_field",
                "PUT",
                {"order_custom_field_id": FIELD_ID, "order_custom_field_label": "Gate"},
            ),
        ],
    )
    def test_writes_send_the_field_as_json(self, client, mocked, query_of, last_request, api_key, method, http, kwargs):
        mocked.add(http, ORDER_CUSTOM_USER_FIELDS, json={"result": "OK", "affected": 1}, status=200)

        assert getattr(client.order, method)(**kwargs) == {"result": "OK", "affected": 1}
        assert last_request().method == http
        assert query_of(last_request()) == {"api_key": api_key}
        assert body_of(last_request()) == kwargs

    def test_remove_order_custom_user_field_sends_the_id_as_json(self, client, mocked, last_request, api_key):
        mocked.add(responses.DELETE, ORDER_CUSTOM_USER_FIELDS, json={"result": "OK", "affected": 1}, status=200)

        client.order.remove_order_custom_user_field(FIELD_ID)

        assert last_request().method == "DELETE"
        assert body_of(last_request()) == {"order_custom_field_id": FIELD_ID}
        assert api_key not in last_request().body.decode()

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.GET, ORDER_CUSTOM_USER_FIELDS, json={"errors": ["Access denied"]}, status=403)

        assert client.order.get_order_custom_user_fields() == {"errors": ["Access denied"]}

    def test_a_non_json_reply_is_returned_raw(self, client, mocked):
        mocked.add(responses.GET, ORDERS_UPDATES, body=b"maintenance", status=200)

        assert client.order.get_orders_updates(last_known_ts=0) == b"maintenance"
