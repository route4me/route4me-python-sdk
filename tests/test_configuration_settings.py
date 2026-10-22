"""Request-level tests for :class:`route4me.configuration_settings.ConfigurationSettings`."""

import json

import pytest
import responses

from route4me.api_endpoints import CONFIGURATION_SETTINGS


class TestConfigurationSettings:
    @pytest.mark.parametrize(
        ("method", "http_method"),
        [("create_new_configuration_key", "POST"), ("update_configuration_key", "PUT")],
    )
    def test_writes_send_the_key_and_value_as_json(self, client, mocked, last_request, query_of, method, http_method):
        mocked.add(http_method, CONFIGURATION_SETTINGS, json={"result": "OK", "affected": 1}, status=200)

        result = getattr(client.configuration_settings, method)("hide_sharing_menu", "true")

        assert result == {"result": "OK", "affected": 1}
        request = last_request()
        assert request.method == http_method
        assert request.url.split("?")[0] == CONFIGURATION_SETTINGS
        assert query_of(request) == {"api_key": client.key}
        assert json.loads(request.body) == {"config_key": "hide_sharing_menu", "config_value": "true"}

    def test_get_configuration_data_sends_the_key_in_the_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, CONFIGURATION_SETTINGS, json={"result": "OK", "data": []}, status=200)

        assert client.configuration_settings.get_configuration_data("hide_sharing_menu") == {"result": "OK", "data": []}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {"api_key": client.key, "config_key": "hide_sharing_menu"}
        assert last_request().body is None

    def test_get_configuration_data_without_a_key_lists_them_all(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, CONFIGURATION_SETTINGS, json={"result": "OK", "data": []}, status=200)

        client.configuration_settings.get_configuration_data()

        assert query_of(last_request()) == {"api_key": client.key}

    def test_remove_configuration_key_sends_the_key_as_json(self, client, mocked, last_request, query_of):
        mocked.add(responses.DELETE, CONFIGURATION_SETTINGS, json={"result": "OK", "affected": 1}, status=200)

        client.configuration_settings.remove_configuration_key("hide_sharing_menu")

        assert last_request().method == "DELETE"
        assert query_of(last_request()) == {"api_key": client.key}
        assert json.loads(last_request().body) == {"config_key": "hide_sharing_menu"}

    def test_calls_do_not_leak_into_each_other(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, CONFIGURATION_SETTINGS, json={"data": []}, status=200)

        client.configuration_settings.get_configuration_data("first_key")
        client.configuration_settings.get_configuration_data()

        assert query_of(last_request()) == {"api_key": client.key}

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked, load_fixture):
        mocked.add(responses.GET, CONFIGURATION_SETTINGS, json=load_fixture("error_v4"), status=401)

        assert client.configuration_settings.get_configuration_data() == {"errors": ["The API key is invalid."]}
