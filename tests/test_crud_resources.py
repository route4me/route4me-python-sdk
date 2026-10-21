"""Coverage for the simple CRUD resources.

``avoidance_zones``, ``address_book``, ``activity_feed`` and ``orders`` are all
thin wrappers over ``make_request`` with required-param checks, and all four
were effectively untested (19-47%).

These are deliberately written as a table so that Phase 7's manifest engine can
absorb them: the shape here is one row per method, which is what that engine
generalises.
"""

import json

import pytest
import responses

from route4me.api_endpoints import ACTIVITY_FEED, ADDRESSBOOK, AVOIDANCE, ORDERS_HOST
from route4me.avoidance_zones import AvoidanceZones, AvoindanceZones
from route4me.exceptions import ParamValueException

TERRITORY_ID = "0F3B8C2D5E7A419B6C8D0E2F4A6B8C1D"
ADDRESS_ID = 12345
ORDER_ID = 67890

ZONE = {
    "territory_name": "No-go zone",
    "territory_color": "ff0000",
    "territory": {"type": "circle", "data": ["40.7636197,-73.9744388", "500"]},
}
CONTACT = {"address_1": "754 5th Ave New York, NY 10019", "cached_lat": 40.7636197, "cached_lng": -73.9744388}


class TestAvoidanceZones:
    def test_get_all(self, client, mocked, last_request):
        mocked.add(responses.GET, AVOIDANCE, json=[{"territory_id": TERRITORY_ID}], status=200)

        result = client.avoidance_zones.get_avoidance_zones()

        assert result[0]["territory_id"] == TERRITORY_ID
        assert last_request().method == "GET"

    def test_get_one(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, AVOIDANCE, json={"territory_id": TERRITORY_ID}, status=200)

        client.avoidance_zones.get_avoidance_zone(territory_id=TERRITORY_ID)

        assert query_of(last_request())["territory_id"] == TERRITORY_ID

    def test_get_one_requires_the_territory_id(self, client):
        with pytest.raises(ParamValueException):
            client.avoidance_zones.get_avoidance_zone()

    def test_add_posts_a_json_body(self, client, mocked, last_request):
        mocked.add(responses.POST, AVOIDANCE, json={"territory_id": TERRITORY_ID}, status=200)

        client.avoidance_zones.add_avoidance_zone(**ZONE)

        assert last_request().method == "POST"
        assert json.loads(last_request().body) == ZONE

    @pytest.mark.parametrize("missing", sorted(ZONE))
    def test_add_enforces_each_required_field(self, client, missing):
        with pytest.raises(ParamValueException):
            client.avoidance_zones.add_avoidance_zone(**{k: v for k, v in ZONE.items() if k != missing})

    def test_update_sends_a_put_with_the_id_in_the_query(self, client, mocked, query_of, last_request):
        mocked.add(responses.PUT, AVOIDANCE, json={"territory_id": TERRITORY_ID}, status=200)

        client.avoidance_zones.update_avoidance_zone(TERRITORY_ID, **ZONE)

        assert last_request().method == "PUT"
        assert query_of(last_request())["territory_id"] == TERRITORY_ID

    def test_update_enforces_the_payload(self, client):
        with pytest.raises(ParamValueException):
            client.avoidance_zones.update_avoidance_zone(TERRITORY_ID, territory_name="only a name")

    def test_delete(self, client, mocked, query_of, last_request):
        mocked.add(responses.DELETE, AVOIDANCE, json={"status": True}, status=200)

        result = client.avoidance_zones.delete_avoidance_zone(territory_id=TERRITORY_ID)

        assert result == {"status": True}
        assert last_request().method == "DELETE"
        assert query_of(last_request())["territory_id"] == TERRITORY_ID

    def test_delete_requires_the_territory_id(self, client):
        with pytest.raises(ParamValueException):
            client.avoidance_zones.delete_avoidance_zone()

    def test_the_misspelled_alias_is_the_same_class(self):
        """`AvoindanceZones` shipped in a release and must never be removed."""
        assert AvoindanceZones is AvoidanceZones

    def test_an_api_error_is_returned_not_raised(self, client, mocked):
        mocked.add(responses.GET, AVOIDANCE, json={"errors": ["nope"]}, status=400)

        assert client.avoidance_zones.get_avoidance_zones() == {"errors": ["nope"]}


class TestAddressBook:
    def test_create_contact(self, client, mocked, last_request):
        mocked.add(responses.POST, ADDRESSBOOK, json={"address_id": ADDRESS_ID}, status=200)

        result = client.address_book.create_contact(**CONTACT)

        assert result["address_id"] == ADDRESS_ID
        assert json.loads(last_request().body) == CONTACT

    @pytest.mark.parametrize("missing", sorted(CONTACT))
    def test_create_enforces_each_required_field(self, client, missing):
        with pytest.raises(ParamValueException):
            client.address_book.create_contact(**{k: v for k, v in CONTACT.items() if k != missing})

    def test_get_contacts(self, client, mocked, query_of, last_request, api_key):
        mocked.add(responses.GET, ADDRESSBOOK, json={"results": []}, status=200)

        client.address_book.get_addressbook_contacts(limit=10, offset=0)

        query = query_of(last_request())
        assert query["api_key"] == api_key
        assert query["limit"] == "10"

    def test_get_one_contact(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, ADDRESSBOOK, json={"address_id": ADDRESS_ID}, status=200)

        client.address_book.get_addressbook_contact(address_id=ADDRESS_ID)

        assert query_of(last_request())["address_id"] == str(ADDRESS_ID)

    def test_get_one_requires_the_address_id(self, client):
        with pytest.raises(ParamValueException):
            client.address_book.get_addressbook_contact()

    def test_update_contact(self, client, mocked, last_request):
        mocked.add(responses.PUT, ADDRESSBOOK, json={"address_id": ADDRESS_ID}, status=200)

        client.address_book.update_contact(address_id=ADDRESS_ID, first_name="Ada")

        assert last_request().method == "PUT"
        assert json.loads(last_request().body)["first_name"] == "Ada"

    def test_update_requires_the_address_id(self, client):
        with pytest.raises(ParamValueException):
            client.address_book.update_contact(first_name="Ada")

    def test_delete_contacts(self, client, mocked, last_request):
        mocked.add(responses.DELETE, ADDRESSBOOK, json={"status": True}, status=200)

        result = client.address_book.delete_addressbook_contact(address_ids=[ADDRESS_ID])

        assert result == {"status": True}
        assert last_request().method == "DELETE"

    def test_delete_requires_address_ids(self, client):
        with pytest.raises(ParamValueException):
            client.address_book.delete_addressbook_contact()


class TestOrders:
    def test_create_order(self, client, mocked, last_request):
        mocked.add(responses.POST, ORDERS_HOST, json={"order_id": ORDER_ID}, status=200)

        result = client.order.create_order(address_1="754 5th Ave")

        assert result["order_id"] == ORDER_ID
        assert last_request().method == "POST"

    def test_create_requires_address_1(self, client):
        with pytest.raises(ParamValueException):
            client.order.create_order()

    def test_get_order(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, ORDERS_HOST, json={"order_id": ORDER_ID}, status=200)

        result = client.order.get_order(order_id=ORDER_ID)

        assert result["order_id"] == ORDER_ID
        assert query_of(last_request())["order_id"] == str(ORDER_ID)

    def test_get_requires_the_order_id(self, client):
        with pytest.raises(ParamValueException):
            client.order.get_order()

    def test_update_order(self, client, mocked, last_request):
        mocked.add(responses.PUT, ORDERS_HOST, json={"order_id": ORDER_ID}, status=200)

        client.order.update_order(address_1="754 5th Ave", order_id=ORDER_ID)

        assert last_request().method == "PUT"

    def test_update_requires_address_1(self, client):
        with pytest.raises(ParamValueException):
            client.order.update_order(order_id=ORDER_ID)

    def test_delete_order(self, client, mocked, last_request):
        mocked.add(responses.DELETE, ORDERS_HOST, json={"status": True}, status=200)

        result = client.order.delete_order(order_ids=[ORDER_ID])

        assert result == {"status": True}
        assert last_request().method == "DELETE"

    def test_delete_requires_order_ids(self, client):
        with pytest.raises(ParamValueException):
            client.order.delete_order()

    def test_a_non_json_body_returns_raw_content(self, client, mocked):
        mocked.add(responses.GET, ORDERS_HOST, body="not json", status=200)

        assert client.order.get_order(order_id=ORDER_ID) == b"not json"

    def test_an_api_error_is_returned_not_raised(self, client, mocked):
        mocked.add(responses.GET, ORDERS_HOST, json={"errors": ["nope"]}, status=404)

        assert client.order.get_order(order_id=ORDER_ID) == {"errors": ["nope"]}


class TestActivityFeed:
    def test_get_activities_feed(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, ACTIVITY_FEED, json={"results": []}, status=200)

        client.activity_feed.get_activities_feed(limit=10, offset=0)

        assert query_of(last_request())["limit"] == "10"

    def test_get_activities_feed_by_type(self, client, mocked, query_of, last_request):
        mocked.add(responses.GET, ACTIVITY_FEED, json={"results": []}, status=200)

        client.activity_feed.get_activities_feed_by_type(limit=10, offset=0, activity_type="area-added")

        assert query_of(last_request())["activity_type"] == "area-added"

    @pytest.mark.parametrize(
        ("method", "activity_type"),
        [
            ("get_activity_feed_inserted", "insert-destination"),
            ("get_activity_feed_deleted", "delete-destination"),
            ("get_activity_feed_route_owner_changed", "route-owner-changed"),
        ],
    )
    def test_the_typed_feed_helpers_pin_their_activity_type(
        self, client, mocked, query_of, last_request, method, activity_type
    ):
        """Each helper is a fixed-``activity_type`` shorthand and requires a
        ``route_id``."""
        mocked.add(responses.GET, ACTIVITY_FEED, json={"results": []}, status=200)

        result = getattr(client.activity_feed, method)(route_id="R1", limit=10, offset=0)

        assert result == {"results": []}
        assert query_of(last_request())["activity_type"] == activity_type

    @pytest.mark.parametrize(
        "method",
        ["get_activity_feed_inserted", "get_activity_feed_deleted", "get_activity_feed_route_owner_changed"],
    )
    def test_the_typed_feed_helpers_require_a_route_id(self, client, method):
        with pytest.raises(ParamValueException):
            getattr(client.activity_feed, method)(limit=10, offset=0)

    def test_log_specific_message(self, client, mocked, last_request):
        mocked.add(responses.POST, ACTIVITY_FEED, json={"status": True}, status=200)

        result = client.activity_feed.log_specific_message(route_id="R1", activity_message="hello")

        assert result == {"status": True}
        assert last_request().method == "POST"
        assert json.loads(last_request().body) == {
            "route_id": "R1",
            "activity_message": "hello",
            "activity_type": "user_message",
        }

    def test_log_specific_message_keeps_the_key_out_of_the_body(self, client, mocked, last_request, api_key):
        mocked.add(responses.POST, ACTIVITY_FEED, json={"status": True}, status=200)

        client.activity_feed.log_specific_message(route_id="R1", activity_message="hello")

        assert api_key not in last_request().body.decode()

    def test_log_specific_message_enforces_its_required_fields(self, client):
        with pytest.raises(ParamValueException):
            client.activity_feed.log_specific_message(route_id="R1")

    def test_an_api_error_is_returned_not_raised(self, client, mocked):
        mocked.add(responses.GET, ACTIVITY_FEED, json={"errors": ["nope"]}, status=400)

        assert client.activity_feed.get_activities_feed(limit=1, offset=0) == {"errors": ["nope"]}
