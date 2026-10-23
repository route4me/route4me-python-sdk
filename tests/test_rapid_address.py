"""Tests for ``route4me/rapid_address.py``.

The street-data endpoints are gone from ``rapid.route4me.com``, so every
method warns, checks its arguments and returns an error dict without sending a
request: the SDK never sends the API key to an endpoint that no longer exists.
"""

import pytest

from route4me.exceptions import ParamValueException

CALLS = [
    ("get_street_data", {}),
    ("get_street_data", {"pk": "PK1"}),
    ("get_street_data", {"offset": 10, "limit": 20}),
    ("get_street_data_zip", {"zipcode": "00602"}),
    ("get_street_data_zip", {"zipcode": "00602", "offset": 1, "limit": 5}),
    ("get_street_data_service", {"zipcode": "00602", "housenumber": "17"}),
]


@pytest.mark.filterwarnings("default::DeprecationWarning")
@pytest.mark.parametrize(("method", "kwargs"), CALLS)
def test_every_street_data_method_warns_and_sends_nothing(client, mocked, method, kwargs):
    with pytest.warns(DeprecationWarning, match="no replacement"):
        result = getattr(client.rapid_address, method)(**kwargs)

    assert result == {"errors": ["rapid.route4me.com no longer serves /street_data, so no request was sent."]}
    assert not mocked.calls


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
class TestArgumentsAreStillChecked:
    def test_a_missing_zipcode_raises(self, client):
        with pytest.raises(ParamValueException):
            client.rapid_address.get_street_data_zip()

    def test_a_non_integer_offset_raises(self, client):
        with pytest.raises(ParamValueException):
            client.rapid_address.get_street_data_zip(zipcode="00602", offset="abc", limit=5)

    @pytest.mark.parametrize("missing", ["zipcode", "housenumber"])
    def test_each_required_field_of_the_service_lookup_is_enforced(self, client, missing):
        payload = {"zipcode": "00602", "housenumber": "17"}
        del payload[missing]

        with pytest.raises(ParamValueException):
            client.rapid_address.get_street_data_service(**payload)

    def test_an_empty_pk_raises(self, client):
        with pytest.raises(ParamValueException):
            client.rapid_address.get_street_data(pk="")
