"""
tests.unit.splitters.test_split
===============================================================================

Unit tests for `record_segmentation.splitters.split`.

Overview
--------
These tests validate the v1 streaming segment splitting algorithm.

Scope
-----
- basic segmentation
- preamble handling
- empty input
- inputs with no segment starts
- consecutive segment starts
- final flush behavior
- detector contract validation
"""

from __future__ import annotations

import pytest

from record_segmentation.errors import SegmentSplitError
from record_segmentation.splitters.split import split_segments

# ============================================================================
# Basic segmentation
# ============================================================================


def test_split_segments_splits_basic_keyword_input(
    basic_lines: list[str],
    keyword_detector,
) -> None:
    """
    Basic keyword-based input should be split into distinct segments.
    """
    result = list(split_segments(basic_lines, keyword_detector))

    assert result == [
        [
            "START alpha\n",
            "alpha line 1\n",
            "alpha line 2\n",
        ],
        [
            "START beta\n",
            "beta line 1\n",
        ],
    ]


def test_split_segments_splits_basic_regex_input(
    timestamp_lines: list[str],
    regex_detector,
) -> None:
    """
    Regex-based input should be split into distinct segments.
    """
    result = list(split_segments(timestamp_lines, regex_detector))

    assert result == [
        [
            "2026-03-12 INFO startup\n",
            "payload line a\n",
        ],
        [
            "2026-03-12 ERROR failure\n",
            "trace line 1\n",
            "trace line 2\n",
        ],
    ]


# ============================================================================
# Preamble handling
# ============================================================================


def test_split_segments_ignores_preamble_by_default(
    preamble_lines: list[str],
    keyword_detector,
) -> None:
    """
    Lines before the first segment start should be ignored by default.
    """
    result = list(split_segments(preamble_lines, keyword_detector))

    assert result == [
        [
            "START alpha\n",
            "alpha line 1\n",
        ]
    ]


def test_split_segments_can_include_preamble_as_first_segment(
    preamble_lines: list[str],
    keyword_detector,
) -> None:
    """
    When configured, preamble lines should be emitted as the first segment.
    """
    result = list(
        split_segments(
            preamble_lines,
            keyword_detector,
            include_preamble=True,
        )
    )

    assert result == [
        [
            "noise line 1\n",
            "noise line 2\n",
        ],
        [
            "START alpha\n",
            "alpha line 1\n",
        ],
    ]


# ============================================================================
# Empty / no-start inputs
# ============================================================================


def test_split_segments_returns_nothing_for_empty_input(
    empty_lines: list[str],
    keyword_detector,
) -> None:
    """
    Empty input should yield no segments.
    """
    result = list(split_segments(empty_lines, keyword_detector))

    assert result == []


def test_split_segments_returns_nothing_when_no_start_found_and_preamble_ignored(
    no_start_lines: list[str],
    keyword_detector,
) -> None:
    """
    Input with no segment start should yield nothing when preamble is ignored.
    """
    result = list(split_segments(no_start_lines, keyword_detector))

    assert result == []


def test_split_segments_returns_preamble_when_no_start_found_and_included(
    no_start_lines: list[str],
    keyword_detector,
) -> None:
    """
    Input with no segment start should yield one segment when preamble
    inclusion is enabled.
    """
    result = list(
        split_segments(
            no_start_lines,
            keyword_detector,
            include_preamble=True,
        )
    )

    assert result == [
        [
            "noise line 1\n",
            "noise line 2\n",
            "noise line 3\n",
        ]
    ]


# ============================================================================
# Consecutive starts
# ============================================================================


def test_split_segments_emits_one_line_segments_for_consecutive_starts(
    consecutive_start_lines: list[str],
    keyword_detector,
) -> None:
    """
    Consecutive segment-start lines should produce distinct one-line segments.
    """
    result = list(split_segments(consecutive_start_lines, keyword_detector))

    assert result == [
        ["START alpha\n"],
        ["START beta\n"],
        ["START gamma\n"],
    ]


# ============================================================================
# Final flush behavior
# ============================================================================


def test_split_segments_flushes_final_open_segment_at_end_of_input(
    keyword_detector,
) -> None:
    """
    The final open segment should be emitted when input is exhausted.
    """
    lines = [
        "START alpha\n",
        "alpha line 1\n",
        "alpha line 2\n",
    ]

    result = list(split_segments(lines, keyword_detector))

    assert result == [
        [
            "START alpha\n",
            "alpha line 1\n",
            "alpha line 2\n",
        ]
    ]


# ============================================================================
# Streaming behavior
# ============================================================================


def test_split_segments_accepts_generator_input(
    basic_line_generator,
    keyword_detector,
) -> None:
    """
    The splitter should work with streaming generator input, not only lists.
    """
    result = list(split_segments(basic_line_generator, keyword_detector))

    assert result == [
        [
            "START alpha\n",
            "alpha line 1\n",
            "alpha line 2\n",
        ],
        [
            "START beta\n",
            "beta line 1\n",
        ],
    ]


# ============================================================================
# Detector validation
# ============================================================================


def test_split_segments_rejects_object_without_is_segment_start() -> None:
    """
    The splitter should reject detector-like inputs that do not implement the
    required method.
    """

    class InvalidDetector:
        """Intentionally invalid detector object."""

    with pytest.raises(SegmentSplitError):
        list(split_segments(["START alpha\n"], InvalidDetector()))


def test_split_segments_rejects_non_callable_is_segment_start() -> None:
    """
    The splitter should reject detector-like inputs whose
    `is_segment_start` attribute is not callable.
    """

    class InvalidDetector:
        """Invalid detector with non-callable contract member."""

        is_segment_start = True

    with pytest.raises(SegmentSplitError):
        list(split_segments(["START alpha\n"], InvalidDetector()))
