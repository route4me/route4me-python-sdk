"""Request-level tests for :class:`route4me.configuration_settings_v5.ConfigurationSettingsV5`."""

import responses

from route4me.api_endpoints import MEMBER_CONFIGURATION_SETTINGS_V5


class TestConfigurationSettingsV5:
    def test_get_member_configuration_settings_sends_the_filters(self, client, mocked, last_request, query_of):
        reply = {"status": "success", "data": [{"config_key": "hide_sharing_menu", "config_value": "true"}]}
        mocked.add(responses.GET, MEMBER_CONFIGURATION_SETTINGS_V5, json=reply, status=200)

        result = client.configuration_settings_v5.get_member_configuration_settings(
            mcs="MCS-1", config_key="hide_sharing_menu"
        )

        assert result == reply
        request = last_request()
        assert request.method == "GET"
        assert request.url.split("?")[0] == MEMBER_CONFIGURATION_SETTINGS_V5
        assert query_of(request) == {"mcs": "MCS-1", "config_key": "hide_sharing_menu"}
        assert request.body is None

    def test_without_filters_sends_no_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, MEMBER_CONFIGURATION_SETTINGS_V5, json={"status": "success", "data": []}, status=200)

        client.configuration_settings_v5.get_member_configuration_settings()

        assert query_of(last_request()) == {}

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        error = {"status": False, "code": 401, "exit_code": 1, "messages": ["Unauthenticated"]}
        mocked.add(responses.GET, MEMBER_CONFIGURATION_SETTINGS_V5, json=error, status=401)

        assert client.configuration_settings_v5.get_member_configuration_settings() == {"errors": ["Unauthenticated"]}
