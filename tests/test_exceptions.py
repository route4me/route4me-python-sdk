"""Tests for ``route4me/exceptions.py``.

The two exception classes carry the SDK's entire error contract, and
``APIException.to_dict()`` is what almost every resource method returns on an
API error -- so its behaviour on malformed input matters more than its
behaviour on the happy path.
"""

import json

import pytest

from route4me.exceptions import DRIVER_VERSION, APIException, ParamValueException
from route4me.version import VERSION_STRING


class TestAPIException:
    def test_accessors(self):
        exc = APIException(404, '{"errors": ["not found"]}', "https://api.route4me.com/x")

        assert exc.get_status_code() == 404
        assert exc.get_response() == '{"errors": ["not found"]}'

    def test_args_carry_the_diagnostic_payload(self):
        exc = APIException(500, "boom", "https://api.route4me.com/x")

        (payload,) = exc.args
        assert payload["http_status_code"] == 500
        assert payload["response"] == "boom"
        assert payload["driver_version"] == DRIVER_VERSION

    def test_driver_version_tracks_the_package_version(self):
        assert DRIVER_VERSION == f"route4me-python-sdk-{VERSION_STRING}"

    def test_to_dict_extracts_the_errors_key(self):
        exc = APIException(400, json.dumps({"errors": ["a", "b"]}), "u")

        assert exc.to_dict() == {"errors": ["a", "b"]}

    def test_to_dict_on_valid_json_without_an_errors_key(self):
        exc = APIException(400, json.dumps({"status": False}), "u")

        assert exc.to_dict() == {"errors": None}

    def test_to_dict_on_non_json_returns_a_placeholder(self):
        exc = APIException(500, "<html>Gateway Error</html>", "u")

        assert exc.to_dict() == {"errors": "Unexpected server response"}

    def test_to_dict_on_an_empty_body(self):
        exc = APIException(502, "", "u")

        assert exc.to_dict() == {"errors": "Unexpected server response"}

    @pytest.mark.xfail(
        strict=True,
        reason="Phase 4: to_dict catches only JSONDecodeError, so a None body "
        "raises TypeError out of the error path. Remove this marker once the "
        "handler also catches TypeError.",
    )
    def test_to_dict_survives_a_none_body(self):
        """A response with no body should not turn into a second exception."""
        assert APIException(504, None, "u").to_dict() == {"errors": "Unexpected server response"}

    @pytest.mark.xfail(
        strict=True,
        reason="Phase 4: json.loads('[1,2]') returns a list, whose .get raises "
        "AttributeError out of to_dict. Remove this marker once non-dict "
        "payloads are handled.",
    )
    def test_to_dict_survives_a_json_array_body(self):
        """Some endpoints return a bare array even on an error status."""
        assert APIException(400, "[1, 2]", "u").to_dict() == {"errors": "Unexpected server response"}


class TestParamValueException:
    def test_accessors(self):
        exc = ParamValueException("route_id", "must be a string")

        assert exc.param == "route_id"
        assert exc.get_msg() == "must be a string"

    def test_args_carry_param_and_msg(self):
        (payload,) = ParamValueException("lat", "must be a float").args

        assert payload == {"param": "lat", "msg": "must be a float"}

    def test_it_is_catchable_as_a_plain_exception(self):
        with pytest.raises(Exception):  # noqa: B017 - the point is the base class
            raise ParamValueException("x", "y")
