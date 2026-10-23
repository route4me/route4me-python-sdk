"""Tests for ``route4me/_url.py``.

These helpers are the defence against path injection. API V5 is REST-style
with IDs in the path (``/route-status/{route_id}``), so all ~200 of its
endpoints share the surface that ``rapid_address`` had -- which makes these
the most-reused security-relevant functions in the package.
"""

import pytest

from route4me._url import join_path, path_int, path_segment
from route4me.exceptions import ParamValueException


class TestPathSegment:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("00602", "00602"),
            ("17", "17"),
            (17, "17"),
            ("ABC123", "ABC123"),
            ("a-b_c.d~e", "a-b_c.d~e"),  # RFC 3986 unreserved characters
        ],
    )
    def test_safe_values_pass_through(self, value, expected):
        assert path_segment(value) == expected

    @pytest.mark.parametrize(
        ("hostile", "must_not_contain"),
        [
            ("../../admin", "/"),
            ("a/b", "/"),
            ("x?y=1", "?"),
            ("x#frag", "#"),
            ("x&y=2", "&"),
            ("100%", "%2"),  # the '%' itself must be encoded, not passed raw
        ],
    )
    def test_path_traversal_and_delimiters_are_encoded(self, hostile, must_not_contain):
        result = path_segment(hostile, "zipcode")

        if must_not_contain != "%2":
            assert must_not_contain not in result
        assert result != hostile

    def test_a_slash_cannot_escape_the_segment(self):
        """The core guarantee. ``quote`` alone leaves '/' untouched by default,
        which is exactly the character that breaks out of a path segment."""
        assert path_segment("../../admin", "zipcode") == "..%2F..%2Fadmin"

    def test_spaces_and_non_ascii_are_encoded(self):
        assert path_segment("a b") == "a%20b"
        assert path_segment("Yigal Azrouël") == "Yigal%20Azrou%C3%ABl"

    def test_none_is_rejected(self):
        with pytest.raises(ParamValueException) as excinfo:
            path_segment(None, "zipcode")

        assert excinfo.value.param == "zipcode"

    @pytest.mark.parametrize("empty", ["", "   ", "\t"])
    def test_empty_is_rejected(self, empty):
        """An empty segment would collapse the path and silently hit a
        different endpoint."""
        with pytest.raises(ParamValueException):
            path_segment(empty, "zipcode")


class TestPathInt:
    @pytest.mark.parametrize(("value", "expected"), [(0, "0"), (10, "10"), ("25", "25"), (999999, "999999")])
    def test_valid_integers(self, value, expected):
        assert path_int(value) == expected

    @pytest.mark.parametrize("bad", ["abc", "1.5", None, [], "../../etc", "1;DROP"])
    def test_non_integers_are_rejected(self, bad):
        """Rejecting beats escaping here: a non-numeric offset is a caller bug,
        and encoding it would surface as a confusing 404."""
        with pytest.raises(ParamValueException):
            path_int(bad, "offset")

    @pytest.mark.parametrize("bad", [-1, -100, "-5"])
    def test_negatives_are_rejected(self, bad):
        with pytest.raises(ParamValueException):
            path_int(bad, "offset")

    def test_booleans_are_coerced_through_the_string_path(self):
        """``bool`` subclasses ``int``, so it is routed through ``int(str(...))``
        and rejected -- ``True`` is never a meaningful offset."""
        with pytest.raises(ParamValueException):
            path_int(True, "offset")

    def test_the_minimum_is_configurable(self):
        assert path_int(1, "limit", minimum=1) == "1"
        with pytest.raises(ParamValueException):
            path_int(0, "limit", minimum=1)

    def test_the_error_names_the_parameter(self):
        with pytest.raises(ParamValueException) as excinfo:
            path_int("nope", "limit")

        assert excinfo.value.param == "limit"


class TestJoinPath:
    def test_appends_segments_with_a_trailing_slash(self):
        result = join_path("https://rapid.route4me.com/street_data/", "00602", "17")

        assert result == "https://rapid.route4me.com/street_data/00602/17/"

    def test_a_base_without_a_trailing_slash(self):
        assert join_path("https://h/x", "1") == "https://h/x/1/"

    def test_no_segments_normalises_to_a_single_trailing_slash(self):
        assert join_path("https://h/x/") == "https://h/x/"

    def test_duplicate_slashes_are_not_produced(self):
        assert "//" not in join_path("https://h/x/", "/1/", "/2/").replace("https://", "")

    def test_it_does_not_encode(self):
        """Encoding is ``path_segment``'s job. Keeping them separate makes an
        accidental double-encoding bug impossible to introduce here."""
        assert join_path("https://h/x", "a b") == "https://h/x/a b/"
