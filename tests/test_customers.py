"""Request-level tests for :class:`route4me.customers.Customers`."""

import json

import pytest
import responses

from route4me.api_endpoints import CUSTOMERS_V5
from route4me.exceptions import ParamValueException

CUSTOMER_ID = "CUSTOMER-1"


class TestCustomers:
    def test_create_customer_posts_the_fields(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, CUSTOMERS_V5, json={"customer_id": CUSTOMER_ID}, status=201)

        result = client.customers.create_customer(name="Acme Inc.", accountable_person_id=7, currency="USD")

        assert result == {"customer_id": CUSTOMER_ID}
        assert last_request().method == "POST"
        assert query_of(last_request()) == {}
        assert json.loads(last_request().body) == {"name": "Acme Inc.", "accountable_person_id": 7, "currency": "USD"}

    def test_create_customer_names_the_missing_fields(self, client, mocked):
        with pytest.raises(ParamValueException) as excinfo:
            client.customers.create_customer(currency="USD")

        assert "name" in str(excinfo.value)
        assert "accountable_person_id" in str(excinfo.value)
        assert not mocked.calls

    def test_get_customer_by_id(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, f"{CUSTOMERS_V5}/{CUSTOMER_ID}", json={"name": "Acme Inc."}, status=200)

        assert client.customers.get_customer_by_id(CUSTOMER_ID) == {"name": "Acme Inc."}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {}
        assert last_request().body is None

    def test_update_customer_puts_the_fields(self, client, mocked, last_request):
        mocked.add(responses.PUT, f"{CUSTOMERS_V5}/{CUSTOMER_ID}", json={"name": "Acme LLC"}, status=200)

        client.customers.update_customer(CUSTOMER_ID, name="Acme LLC", status=0)

        assert last_request().method == "PUT"
        assert json.loads(last_request().body) == {"name": "Acme LLC", "status": 0}

    def test_delete_customer_returns_the_empty_body_of_a_204(self, client, mocked, last_request):
        mocked.add(responses.DELETE, f"{CUSTOMERS_V5}/{CUSTOMER_ID}", body=b"", status=204)

        assert client.customers.delete_customer(CUSTOMER_ID) == b""
        assert last_request().method == "DELETE"

    def test_a_customer_id_with_a_slash_is_encoded(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{CUSTOMERS_V5}/a%2Fb", json={}, status=200)

        client.customers.get_customer_by_id("a/b")

        assert last_request().path_url == "/modules/api/v5.0/customers/a%2Fb"

    @pytest.mark.parametrize("method", ["get_customer_by_id", "update_customer", "delete_customer"])
    def test_an_empty_customer_id_is_rejected_before_any_request(self, client, mocked, method):
        with pytest.raises(ParamValueException):
            getattr(client.customers, method)("")

        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.GET, f"{CUSTOMERS_V5}/{CUSTOMER_ID}", json={"errors": ["Not found"]}, status=404)

        assert client.customers.get_customer_by_id(CUSTOMER_ID) == {"errors": ["Not found"]}

    def test_a_delete_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.DELETE, f"{CUSTOMERS_V5}/{CUSTOMER_ID}", json={"errors": ["Not found"]}, status=404)

        assert client.customers.delete_customer(CUSTOMER_ID) == {"errors": ["Not found"]}
