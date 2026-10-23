"""Tests for the ``ValidatedField`` descriptor system in ``route4me/_fields.py``.

This module replaced 46 hand-written setter methods on ``Base`` and had no
direct tests, despite every resource's parameter validation now flowing
through it.

The descriptor is unusual: ``__get__`` returns a *closure*, so the API is call
syntax (``obj.route_id("ABC")``) rather than assignment. ``self.name`` is the
wire key, which may differ from the attribute name.
"""

import pytest

from route4me._fields import ValidatedField
from route4me.constants import DISTANCE_UNIT, TRAVEL_MODE
from route4me.exceptions import ParamValueException


class Target:
    """Minimal stand-in for ``Base``: just the two copy sinks."""

    str_param = ValidatedField("str_param", str, "param", "must be a string")
    int_data = ValidatedField("int_data", int, "data", "must be an int")
    numeric = ValidatedField("numeric", "numeric", "data", "must be numeric")
    number = ValidatedField("number", "number", "param", "must be a number")
    flag = ValidatedField("flag", "boolish", "data", "must be 0 or 1")
    unit = ValidatedField("unit", "enum", "data", "bad unit", enum_cls=DISTANCE_UNIT)
    algo = ValidatedField("algo", "oneof", "data", "bad algo", valid_values=[1, 2, 3])
    metric = ValidatedField("metric", "range", "data", "out of range", valid_range=(1, 7))
    #: Aliased field: the attribute is `cached`, the wire key is `lat`.
    cached = ValidatedField("lat", "number", "param", "must be a number")

    def __init__(self):
        self.params = {}
        self.data = {"parameters": {}}

    def _copy_param(self, values):
        self.params.update(values)

    def _copy_data(self, values):
        self.data["parameters"].update(values)


@pytest.fixture
def target():
    return Target()


class TestDescriptorProtocol:
    def test_class_access_returns_the_descriptor_itself(self):
        assert isinstance(Target.str_param, ValidatedField)

    def test_instance_access_returns_a_callable(self, target):
        assert callable(target.str_param)

    def test_set_name_records_the_attribute_name(self):
        assert Target.str_param.attr_name == "str_param"

    def test_the_wire_key_can_differ_from_the_attribute_name(self, target):
        """`cached` writes `lat`: the wire key is the descriptor's name."""
        target.cached(40.7)
        assert target.params == {"lat": 40.7}
        assert "cached" not in target.params


class TestRouting:
    def test_param_target_writes_to_params(self, target):
        target.str_param("abc")
        assert target.params == {"str_param": "abc"}
        assert target.data["parameters"] == {}

    def test_data_target_writes_to_data_parameters(self, target):
        target.int_data(5)
        assert target.data["parameters"] == {"int_data": 5}
        assert target.params == {}


class TestValidation:
    @pytest.mark.parametrize("value", ["", "abc", "754 5th Ave"])
    def test_str_accepts_strings(self, target, value):
        target.str_param(value)
        assert target.params["str_param"] == value

    @pytest.mark.parametrize("value", [1, 1.5, None, [], {}, b"bytes"])
    def test_str_rejects_non_strings(self, target, value):
        with pytest.raises(ParamValueException):
            target.str_param(value)

    @pytest.mark.parametrize("value", [0, 1, -5, 10000])
    def test_int_accepts_ints(self, target, value):
        target.int_data(value)
        assert target.data["parameters"]["int_data"] == value

    @pytest.mark.parametrize("value", [1.5, "1", None, []])
    def test_int_rejects_non_ints(self, target, value):
        with pytest.raises(ParamValueException):
            target.int_data(value)

    def test_int_accepts_bool_because_bool_subclasses_int(self, target):
        """Documents current behaviour rather than endorsing it: ``isinstance``
        is used, and in Python ``bool`` is a subclass of ``int``."""
        target.int_data(True)
        assert target.data["parameters"]["int_data"] is True

    @pytest.mark.parametrize("value", [1, 1.5, 0, -2.75])
    def test_numeric_accepts_ints_and_floats(self, target, value):
        target.numeric(value)
        assert target.data["parameters"]["numeric"] == value

    @pytest.mark.parametrize("value", ["1", None, []])
    def test_numeric_rejects_everything_else(self, target, value):
        with pytest.raises(ParamValueException):
            target.numeric(value)

    @pytest.mark.parametrize("value", [40.7636197, 10, 0, -73])
    def test_number_accepts_ints_and_floats(self, target, value):
        """#126: a whole-number coordinate or altitude is valid."""
        target.number(value)
        assert target.params["number"] == value

    @pytest.mark.parametrize("value", [True, False, "1.5", None])
    def test_number_rejects_booleans_and_strings(self, target, value):
        with pytest.raises(ParamValueException):
            target.number(value)

    @pytest.mark.parametrize("value", [0, 1])
    def test_boolish_accepts_zero_and_one(self, target, value):
        target.flag(value)
        assert target.data["parameters"]["flag"] == value

    @pytest.mark.parametrize("value", [-1, 2, 1.0, "1", None])
    def test_boolish_rejects_anything_else(self, target, value):
        with pytest.raises(ParamValueException):
            target.flag(value)

    @pytest.mark.parametrize("value", [DISTANCE_UNIT.MI, DISTANCE_UNIT.KM])
    def test_enum_accepts_declared_members(self, target, value):
        target.unit(value)
        assert target.data["parameters"]["unit"] == value

    @pytest.mark.parametrize("value", ["furlongs", TRAVEL_MODE.DRIVING, 1])
    def test_enum_rejects_values_outside_the_enum(self, target, value):
        with pytest.raises(ParamValueException):
            target.unit(value)

    @pytest.mark.parametrize("value", [1, 2, 3])
    def test_oneof_accepts_listed_values(self, target, value):
        target.algo(value)
        assert target.data["parameters"]["algo"] == value

    @pytest.mark.parametrize("value", [0, 4, "1", None])
    def test_oneof_rejects_unlisted_values(self, target, value):
        with pytest.raises(ParamValueException):
            target.algo(value)

    @pytest.mark.parametrize("value", [1, 4, 7])
    def test_range_accepts_inclusive_bounds(self, target, value):
        target.metric(value)
        assert target.data["parameters"]["metric"] == value

    @pytest.mark.parametrize("value", [0, 8, -1])
    def test_range_rejects_values_outside_the_bounds(self, target, value):
        with pytest.raises(ParamValueException):
            target.metric(value)


class TestExceptionContents:
    def test_exception_carries_the_wire_name_and_message(self, target):
        with pytest.raises(ParamValueException) as excinfo:
            target.str_param(123)

        assert excinfo.value.param == "str_param"
        assert excinfo.value.get_msg() == "must be a string"

    def test_a_rejected_value_is_not_written(self, target):
        with pytest.raises(ParamValueException):
            target.str_param(123)

        assert target.params == {}
