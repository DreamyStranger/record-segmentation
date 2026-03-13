"""
tests.unit.models.test_segment
===============================================================================

Unit tests for `record_segmentation.models.segment`.

Overview
--------
These tests validate the lightweight runtime `Segment` model used to represent
one emitted logical segment.

Scope
-----
- default construction
- convenience properties
- length behavior
- immutability guarantees
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from record_segmentation.models.segment import Segment

# ============================================================================
# Defaults
# ============================================================================


def test_segment_defaults_are_empty_and_unset() -> None:
    """
    A default Segment should start empty and without optional metadata.
    """
    segment = Segment()

    assert segment.lines == []
    assert segment.index is None
    assert segment.start_line_number is None
    assert segment.end_line_number is None


# ============================================================================
# Convenience properties
# ============================================================================


def test_segment_is_empty_true_for_default_segment() -> None:
    """
    `is_empty` should be True when the segment contains no lines.
    """
    segment = Segment()

    assert segment.is_empty is True


def test_segment_is_empty_false_when_lines_exist() -> None:
    """
    `is_empty` should be False when the segment contains one or more lines.
    """
    segment = Segment(lines=["line 1\n"])

    assert segment.is_empty is False


def test_segment_first_line_returns_none_for_empty_segment() -> None:
    """
    `first_line` should return None when the segment is empty.
    """
    segment = Segment()

    assert segment.first_line is None


def test_segment_last_line_returns_none_for_empty_segment() -> None:
    """
    `last_line` should return None when the segment is empty.
    """
    segment = Segment()

    assert segment.last_line is None


def test_segment_first_line_returns_first_entry() -> None:
    """
    `first_line` should return the first stored line.
    """
    segment = Segment(lines=["line 1\n", "line 2\n", "line 3\n"])

    assert segment.first_line == "line 1\n"


def test_segment_last_line_returns_last_entry() -> None:
    """
    `last_line` should return the last stored line.
    """
    segment = Segment(lines=["line 1\n", "line 2\n", "line 3\n"])

    assert segment.last_line == "line 3\n"


# ============================================================================
# Length behavior
# ============================================================================


def test_segment_len_is_zero_when_empty() -> None:
    """
    `len(segment)` should be zero for an empty segment.
    """
    segment = Segment()

    assert len(segment) == 0


def test_segment_len_matches_number_of_lines() -> None:
    """
    `len(segment)` should equal the number of stored lines.
    """
    segment = Segment(lines=["a\n", "b\n", "c\n"])

    assert len(segment) == 3


# ============================================================================
# Metadata
# ============================================================================


def test_segment_preserves_optional_metadata() -> None:
    """
    Segment should preserve caller-provided metadata fields.
    """
    segment = Segment(
        lines=["START alpha\n", "alpha-1\n"],
        index=2,
        start_line_number=10,
        end_line_number=11,
    )

    assert segment.lines == ["START alpha\n", "alpha-1\n"]
    assert segment.index == 2
    assert segment.start_line_number == 10
    assert segment.end_line_number == 11


# ============================================================================
# Immutability
# ============================================================================


def test_segment_is_frozen() -> None:
    """
    Segment should be immutable once created.
    """
    segment = Segment(lines=["line 1\n"])

    with pytest.raises(FrozenInstanceError):
        segment.index = 99  # type: ignore[misc]


def test_segment_uses_slots() -> None:
    """
    Segment should not allow arbitrary dynamic attributes.
    """
    segment = Segment(lines=["line 1\n"])

    with pytest.raises((AttributeError, TypeError)):
        segment.some_new_attribute = "value"  # type: ignore[attr-defined]
