"""Tests for the small data models: ``Slowdowns``, ``Bundling``,
``ServiceTimeRules`` and ``AdvancedConstraint``.

All four are part of the public API (three are re-exported from
``route4me/__init__.py``) and none had any test coverage.
"""

import pytest

from route4me import AdvancedConstraint, Bundling
from route4me.bundling import (
    BUNDLING_ADDITIONAL_ITEM_MODE,
    BUNDLING_FIRST_ITEM_MODE,
    BUNDLING_MERGE_MODE,
    BUNDLING_MODE,
    ServiceTimeRules,
)
from route4me.slowdowns import Slowdowns


class TestSlowdowns:
    @pytest.mark.parametrize(("service", "travel"), [(0, 0), (25, 25), (50, 50), (0, 50)])
    def test_accepts_the_inclusive_range(self, service, travel):
        s = Slowdowns(service, travel)
        assert s.to_dict() == {"service_time": service, "travel_time": travel}

    @pytest.mark.parametrize("bad", [-1, 51, 1.5, "10", None])
    def test_rejects_an_out_of_range_service_time(self, bad):
        with pytest.raises(ValueError, match="Service time"):
            Slowdowns(bad, 10)

    @pytest.mark.parametrize("bad", [-1, 51, 1.5, "10", None])
    def test_rejects_an_out_of_range_travel_time(self, bad):
        with pytest.raises(ValueError, match="Travel time"):
            Slowdowns(10, bad)

    def test_validation_runs_before_assignment(self):
        """A rejected value must not leave a half-built object behind."""
        with pytest.raises(ValueError, match="Service time"):
            Slowdowns(99, 10)


class TestBundlingEnums:
    def test_mode_members(self):
        assert BUNDLING_MODE.BY_ADDRESS == 1
        assert BUNDLING_MODE.BY_COORDINATES == 2
        assert BUNDLING_MODE.BY_STATIC_FIELD == 3
        assert BUNDLING_MODE.BY_CUSTOM_DATA == 4

    def test_merge_mode_members(self):
        assert BUNDLING_MERGE_MODE.KEEP_SEPARATED == 1
        assert BUNDLING_MERGE_MODE.MERGE_INTO_SINGLE == 2

    def test_item_mode_members(self):
        assert BUNDLING_FIRST_ITEM_MODE.KEEP_ORIGINAL_SERVICE_TIME == 1
        assert BUNDLING_ADDITIONAL_ITEM_MODE.DO_NOT_ADD_SERVICE_TIME == 3

    def test_reverse_mapping_is_what_enum_validation_reads(self):
        """``ValidatedField``'s ``enum`` type checks membership against
        ``reverse_mapping`` keys, so it has to hold the *values*."""
        assert set(BUNDLING_MODE.reverse_mapping.keys()) == {1, 2, 3, 4}
        assert BUNDLING_MODE.reverse_mapping[1] == "BY_ADDRESS"


class TestBundling:
    def test_defaults(self):
        b = Bundling()
        assert b.mode == BUNDLING_MODE.BY_ADDRESS
        assert b.merge_mode == BUNDLING_MERGE_MODE.KEEP_SEPARATED
        assert b.mode_params == []

    def test_mutable_defaults_are_not_shared_between_instances(self):
        first, second = Bundling(), Bundling()
        first.mode_params.append("x")
        assert second.mode_params == []

    def test_to_dict_round_trips_the_fields(self):
        b = Bundling(mode=BUNDLING_MODE.BY_COORDINATES, mode_params=["a"])
        result = b.to_dict()
        assert result["mode"] == BUNDLING_MODE.BY_COORDINATES
        assert result["mode_params"] == ["a"]


class TestServiceTimeRules:
    def test_it_still_subclasses_dict(self):
        """Load-bearing: documented in CLAUDE.md as not to be changed."""
        assert isinstance(ServiceTimeRules(), dict)

    def test_defaults_are_class_attributes(self):
        rules = ServiceTimeRules()
        assert rules.first_item_mode is None
        assert rules.additional_items_mode is None


class TestAdvancedConstraint:
    def test_to_dict_strips_none_and_empty_values(self):
        """``to_dict`` runs ``clean_dict``, so unset fields never reach the
        wire -- the API rejects nulls in several of these slots."""
        result = AdvancedConstraint(max_capacity=10, tags=["fridge"]).to_dict()

        assert result["max_capacity"] == 10
        assert result["tags"] == ["fridge"]
        assert "max_cargo_weight" not in result
        assert "vehicles_id" not in result
        assert "depot_address" not in result

    def test_members_count_defaults_to_ten(self):
        assert AdvancedConstraint().to_dict()["members_count"] == 10

    def test_a_populated_depot_address_survives(self):
        constraint = AdvancedConstraint(
            depot_address={"alias": "Depot", "address": "754 5th Ave", "lat": 40.76, "lng": -73.97}
        )
        assert constraint.to_dict()["depot_address"]["alias"] == "Depot"

    def test_mutable_defaults_are_not_shared_between_instances(self):
        first, second = AdvancedConstraint(), AdvancedConstraint()
        first.tags.append("x")
        assert second.tags == []
