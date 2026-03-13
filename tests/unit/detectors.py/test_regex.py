"""
tests.unit.detectors.test_regex
===============================================================================

Unit tests for `record_segmentation.detectors.regex`.

Overview
--------
These tests validate regex-based segment-start detection.

Scope
-----
- construction from pattern strings
- construction from compiled regex objects
- matching and non-matching behavior
- invalid regex validation
"""

from __future__ import annotations

import re

import pytest

from record_segmentation.detectors.regex_detector import RegexDetector
from record_segmentation.errors import InvalidConfigError

# ============================================================================
# Construction
# ============================================================================


def test_regex_detector_accepts_non_empty_pattern_string() -> None:
    """
    RegexDetector should compile and preserve a valid regex pattern string.
    """
    detector = RegexDetector(r"^\d{4}-\d{2}-\d{2}")

    assert detector.pattern.pattern == r"^\d{4}-\d{2}-\d{2}"


def test_regex_detector_accepts_compiled_pattern() -> None:
    """
    RegexDetector should accept a precompiled regex pattern unchanged.
    """
    compiled = re.compile(r"^START")
    detector = RegexDetector(compiled)

    assert detector.pattern is compiled


def test_regex_detector_applies_flags_when_pattern_is_string() -> None:
    """
    Regex flags should be applied when compiling a pattern string.
    """
    detector = RegexDetector(r"^start", flags=re.IGNORECASE)

    assert detector.is_segment_start("START alpha\n") is True
    assert detector.is_segment_start("start beta\n") is True


# ============================================================================
# Matching behavior
# ============================================================================


def test_regex_detector_matches_when_pattern_search_succeeds() -> None:
    """
    A line should be treated as a segment start when the regex search matches.
    """
    detector = RegexDetector(r"^\d{4}-\d{2}-\d{2}")

    assert detector.is_segment_start("2026-03-12 INFO start\n") is True
    assert detector.is_segment_start("2026-01-01 ERROR fail\n") is True


def test_regex_detector_does_not_match_when_pattern_search_fails() -> None:
    """
    A line should not be treated as a segment start when the regex search does
    not match.
    """
    detector = RegexDetector(r"^\d{4}-\d{2}-\d{2}")

    assert detector.is_segment_start("INFO 2026-03-12 start\n") is False
    assert detector.is_segment_start("plain text\n") is False


def test_regex_detector_uses_search_semantics() -> None:
    """
    RegexDetector should use Pattern.search semantics.

    This means non-anchored patterns may match anywhere in the line.
    """
    detector = RegexDetector(r"ERROR")

    assert detector.is_segment_start("ERROR first token\n") is True
    assert detector.is_segment_start("prefix ERROR suffix\n") is True
    assert detector.is_segment_start("all good\n") is False


# ============================================================================
# Validation
# ============================================================================


@pytest.mark.parametrize(
    "pattern",
    [
        "",
        None,
        123,
    ],
)
def test_regex_detector_rejects_invalid_pattern_input(pattern: object) -> None:
    """
    RegexDetector should reject empty or non-regex-compatible pattern inputs.
    """
    with pytest.raises(InvalidConfigError):
        RegexDetector(pattern)  # type: ignore[arg-type]


def test_regex_detector_rejects_invalid_regex_string() -> None:
    """
    RegexDetector should surface invalid regex syntax as InvalidConfigError.
    """
    with pytest.raises(InvalidConfigError):
        RegexDetector(r"([unclosed")
