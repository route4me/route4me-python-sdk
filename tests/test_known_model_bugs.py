"""Known defects in the optimization payload models and helpers.

Each test states the correct behaviour under ``xfail(strict=True)`` and names
the GitHub issue that tracks it. A fix makes the test pass, strict xfail turns
that into a failure, and the marker has to be removed with the fix.
"""

import dataclasses
import json

import pytest
import responses

from route4me.advanced_constraint import AdvancedConstraint
from route4me.api import Route4Me
from route4me.api_endpoints import API_HOST
from route4me.bundling import BUNDLING_FIRST_ITEM_MODE, Bundling, ServiceTimeRules
from route4me.exceptions import ParamValueException
from route4me.utils import clean_dict


class TestServiceTimeRules:
    def test_instances_do_not_share_their_param_lists(self):
        first = ServiceTimeRules()
        second = ServiceTimeRules()

        first.first_item_mode_params.append(30)

        assert second.first_item_mode_params == []

    def test_the_rules_reach_the_request_body(self):
        rules = ServiceTimeRules()
        rules.first_item_mode = BUNDLING_FIRST_ITEM_MODE.USE_CUSTOM_SERVICE_TIME
        rules.first_item_mode_params = [300]

        payload = json.loads(json.dumps({"rules": rules}))

        assert payload["rules"]["first_item_mode"] == BUNDLING_FIRST_ITEM_MODE.USE_CUSTOM_SERVICE_TIME
        assert payload["rules"]["first_item_mode_params"] == [300]

    def test_to_dict_sends_the_first_item_mode_and_any_rule_that_is_set(self):
        rules = ServiceTimeRules()
        assert rules.to_dict() == {"first_item_mode": None}

        rules.additional_items_mode = 3
        rules.additional_items_mode_params = [60]

        assert rules.to_dict() == {
            "first_item_mode": None,
            "additional_items_mode": 3,
            "additional_items_mode_params": [60],
        }

    def test_it_round_trips_through_dataclasses_asdict(self):
        assert dataclasses.asdict(Bundling())["service_time_rules"]["first_item_mode_params"] == []


class TestBundling:
    def test_to_dict_is_a_snapshot(self):
        bundling = Bundling()
        snapshot = bundling.to_dict()

        bundling.mode_params.append("later")

        assert snapshot["mode_params"] == []

    def test_a_bundling_object_is_accepted(self):
        Route4Me("1" * 32).optimization.bundling(Bundling())

    def test_a_bundling_object_is_sent_as_its_dict(self):
        client = Route4Me("1" * 32)

        client.optimization.bundling(Bundling(mode_params=["zip"]))

        assert client.optimization.data["parameters"]["bundling"]["mode_params"] == ["zip"]

    def test_advanced_constraint_objects_are_converted(self):
        client = Route4Me("1" * 32)

        client.optimization.advanced_constraints([AdvancedConstraint(max_cargo_weight=1000, members_count=2)])

        constraint = client.optimization.data["parameters"]["advanced_constraints"][0]
        assert (constraint["max_cargo_weight"], constraint["members_count"]) == (1000, 2)

    def test_a_plain_dict_is_accepted(self):
        client = Route4Me("1" * 32)

        client.optimization.bundling({"mode": 1})

        assert client.optimization.data["parameters"]["bundling"] == {"mode": 1}

    def test_anything_else_is_rejected(self):
        with pytest.raises(ParamValueException):
            Route4Me("1" * 32).optimization.bundling("by address")


class TestCleanDict:
    @pytest.mark.xfail(strict=True, raises=AssertionError, reason="#41: clean_dict drops 0, corrupting time windows")
    def test_a_time_window_starting_at_zero_survives(self):
        assert clean_dict({"available_time_windows": [[0, 3600]]}) == {"available_time_windows": [[0, 3600]]}

    @pytest.mark.xfail(strict=True, raises=AssertionError, reason="#41: clean_dict drops 0.0 coordinates")
    def test_zero_coordinates_survive(self):
        assert clean_dict({"lat": 0.0, "lng": 0.0}) == {"lat": 0.0, "lng": 0.0}

    @pytest.mark.xfail(strict=True, raises=AssertionError, reason="#41: clean_dict drops False")
    def test_false_survives(self):
        assert clean_dict({"is_depot": False}) == {"is_depot": False}

    def test_none_and_empty_containers_are_dropped(self):
        assert clean_dict({"a": None, "b": {}, "c": [], "d": 1}) == {"d": 1}

    def test_empty_strings_inside_lists_are_kept(self):
        assert clean_dict({"tags": ["", "x"]}) == {"tags": ["", "x"]}


class TestAdvancedConstraintSerialisation:
    @pytest.mark.xfail(strict=True, raises=KeyError, reason="#41: a constraint with capacity 0 loses the field")
    def test_a_zero_capacity_is_sent(self):
        constraint = AdvancedConstraint(max_capacity=0, members_count=1)

        assert constraint.to_dict()["max_capacity"] == 0


class TestClientState:
    """Issue #26 and the leftover from #30: one client reused for two optimizations."""

    def test_a_second_optimization_starts_without_the_first_ones_addresses(self, mocked):
        mocked.add(responses.POST, API_HOST, json={"optimization_problem_id": "A"}, status=200)
        client = Route4Me("1" * 32)
        client.address.add_address(address="first", lat=1.0, lng=1.0)
        client.run_optimization()

        client.optimization.reset()
        client.address.add_address(address="second", lat=2.0, lng=2.0)

        assert [a["address"] for a in client.optimization.data["addresses"]] == ["second"]
