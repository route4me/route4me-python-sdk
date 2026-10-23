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
        """This used to return ``{"errors": None}``, which satisfied an
        ``"errors" in result`` check while carrying no information."""
        exc = APIException(400, json.dumps({"status": False}), "u")

        assert exc.to_dict() == {"errors": ["Unexpected server response"]}

    def test_to_dict_treats_a_null_errors_key_as_absent(self):
        """``{"errors": null}`` used to come back unchanged, and
        ``". ".join(None)`` raised in every caller."""
        exc = APIException(400, json.dumps({"errors": None, "message": "Bad route"}), "u")

        assert exc.to_dict() == {"errors": ["Bad route"]}

    def test_to_dict_wraps_a_scalar_v4_error(self):
        exc = APIException(400, json.dumps({"errors": "Route not found"}), "u")

        assert exc.to_dict() == {"errors": ["Route not found"]}

    def test_to_dict_falls_back_when_the_errors_list_is_empty(self):
        exc = APIException(400, json.dumps({"errors": []}), "u")

        assert exc.to_dict() == {"errors": ["Unexpected server response"]}

    def test_to_dict_errors_always_join(self):
        """Every example prints ``". ".join(result["errors"])``. A string value
        printed letter by letter; a non-string list item raised ``TypeError``."""
        bodies = [None, "", "<html>", "[1, 2]", '{"errors": [404, "x"]}', '{"messages": {"a": ["b", 7]}}']

        for body in bodies:
            errors = APIException(400, body, "u").to_dict()["errors"]

            assert errors and all(isinstance(message, str) for message in errors)
            assert ". ".join(errors)

    def test_to_dict_flattens_the_v5_messages_envelope(self):
        """A V5 error has no ``errors`` key at all (see
        ``DataTypes/V5/ResultResponse.cs``), so every V5 failure previously
        came back as ``{"errors": None}`` with the message discarded."""
        body = json.dumps(
            {
                "status": False,
                "code": 422,
                "messages": {
                    "route_id": ["The route id field is required."],
                    "lat": ["The lat must be a number.", "The lat is required."],
                },
            }
        )

        result = APIException(422, body, "u").to_dict()

        assert result == {
            "errors": [
                "The route id field is required.",
                "The lat must be a number.",
                "The lat is required.",
            ]
        }

    def test_to_dict_handles_a_scalar_v5_message(self):
        exc = APIException(422, json.dumps({"status": False, "messages": "Nope"}), "u")

        assert exc.to_dict() == {"errors": ["Nope"]}

    def test_to_dict_falls_back_to_a_message_key(self):
        exc = APIException(500, json.dumps({"message": "Server exploded"}), "u")

        assert exc.to_dict() == {"errors": ["Server exploded"]}

    def test_to_dict_on_non_json_returns_a_placeholder(self):
        exc = APIException(500, "<html>Gateway Error</html>", "u")

        assert exc.to_dict() == {"errors": ["Unexpected server response"]}

    def test_to_dict_on_an_empty_body(self):
        exc = APIException(502, "", "u")

        assert exc.to_dict() == {"errors": ["Unexpected server response"]}

    def test_to_dict_survives_a_none_body(self):
        """A response with no body should not turn into a second exception."""
        assert APIException(504, None, "u").to_dict() == {"errors": ["Unexpected server response"]}

    def test_to_dict_survives_a_json_array_body(self):
        """Some endpoints return a bare array even on an error status."""
        assert APIException(400, "[1, 2]", "u").to_dict() == {"errors": ["Unexpected server response"]}


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
