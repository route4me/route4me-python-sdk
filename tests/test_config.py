"""Tests for ``route4me/config.py``.

Config resolution is layered:

    per-call  >  constructor  >  Route4MeConfig  >  shipped default

The ``UNSET`` sentinel is what makes that work: an explicit ``timeout=None``
means "wait forever", which is a different thing from "the caller didn't say".
A plain ``None`` default could not express both.
"""

import pytest

from route4me.config import (
    DEFAULT_TIMEOUT,
    UNSET,
    Route4MeConfig,
    normalize_timeout,
    resolve_timeout,
)


class TestUnsetSentinel:
    def test_it_is_falsy(self):
        assert not UNSET

    def test_it_reprs_readably(self):
        assert repr(UNSET) == "UNSET"

    def test_it_is_distinct_from_none_and_false(self):
        assert UNSET is not None
        assert UNSET is not False
        assert UNSET != None  # noqa: E711 - identity vs equality is the point


class TestDefaults:
    def test_the_default_timeout_is_a_connect_read_pair(self):
        assert DEFAULT_TIMEOUT == (6.05, 30.0)

    def test_the_read_timeout_matches_the_csharp_sdk(self):
        """C# ``Route4MeConfig.HttpTimeout`` is 30s; the two clients agree."""
        assert DEFAULT_TIMEOUT[1] == 30.0

    def test_the_connect_timeout_clears_two_syn_retransmits(self):
        """1s + 2s + 3s = 6s, plus the offset the requests docs recommend so the
        deadline never lands exactly on a retransmit boundary."""
        assert 6.0 < DEFAULT_TIMEOUT[0] < 7.0

    def test_redaction_is_on_by_default(self):
        assert Route4MeConfig.redact_urls is True


class TestNormalizeTimeout:
    def test_none_means_no_timeout(self):
        assert normalize_timeout(None) is None

    @pytest.mark.parametrize(("value", "expected"), [(30, 30.0), (1.5, 1.5), (0.001, 0.001)])
    def test_a_number_applies_to_both_phases(self, value, expected):
        assert normalize_timeout(value) == expected

    @pytest.mark.parametrize("value", [(1, 2), [1, 2], (1.5, 30.0)])
    def test_a_two_sequence_becomes_a_float_pair(self, value):
        assert normalize_timeout(value) == (float(value[0]), float(value[1]))

    @pytest.mark.parametrize("bad", [0, -1, -0.5])
    def test_non_positive_numbers_are_rejected(self, bad):
        with pytest.raises(ValueError, match="positive"):
            normalize_timeout(bad)

    @pytest.mark.parametrize("bad", [(1,), (1, 2, 3), ()])
    def test_wrong_length_sequences_are_rejected(self, bad):
        with pytest.raises(ValueError, match="connect, read"):
            normalize_timeout(bad)

    @pytest.mark.parametrize("bad", [(0, 5), (5, 0), (-1, 5), ("a", 5), (None, 5)])
    def test_bad_sequence_components_are_rejected(self, bad):
        with pytest.raises(ValueError, match="components"):
            normalize_timeout(bad)

    @pytest.mark.parametrize("bad", ["30", object(), {}, set()])
    def test_wrong_types_are_rejected(self, bad):
        with pytest.raises(ValueError):
            normalize_timeout(bad)

    @pytest.mark.parametrize("bad", [True, False])
    def test_booleans_are_rejected(self, bad):
        """``bool`` subclasses ``int``; ``timeout=True`` is never intended."""
        with pytest.raises(ValueError):
            normalize_timeout(bad)


class TestResolveTimeout:
    def test_the_first_supplied_candidate_wins(self):
        assert resolve_timeout(5, 10) == 5.0

    def test_unset_candidates_are_skipped(self):
        assert resolve_timeout(UNSET, 10) == 10.0
        assert resolve_timeout(UNSET, UNSET, 15) == 15.0

    def test_an_explicit_none_wins_over_a_later_candidate(self):
        """This is exactly why UNSET exists rather than using None."""
        assert resolve_timeout(None, 10) is None

    def test_it_falls_back_to_the_global_config(self, monkeypatch):
        monkeypatch.setattr(Route4MeConfig, "timeout", 42)

        assert resolve_timeout(UNSET, UNSET) == 42.0

    def test_it_falls_back_to_the_shipped_default(self):
        assert resolve_timeout(UNSET, UNSET) == DEFAULT_TIMEOUT

    def test_an_unset_global_falls_through_to_the_default(self, monkeypatch):
        monkeypatch.setattr(Route4MeConfig, "timeout", UNSET)

        assert resolve_timeout(UNSET) == DEFAULT_TIMEOUT

    def test_no_candidates_yields_the_default(self):
        assert resolve_timeout() == DEFAULT_TIMEOUT


class TestGlobalMutationIsIsolatedByMonkeypatch:
    """Guard against a test leaking global state into its neighbours."""

    def test_setting_the_global(self, monkeypatch):
        monkeypatch.setattr(Route4MeConfig, "redact_urls", False)
        assert Route4MeConfig.redact_urls is False

    def test_the_global_is_restored(self):
        assert Route4MeConfig.redact_urls is True
