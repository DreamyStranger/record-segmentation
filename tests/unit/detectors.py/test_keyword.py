"""
tests.unit.detectors.test_keyword
===============================================================================

Unit tests for `record_segmentation.detectors.keyword`.

Overview
--------
These tests validate keyword-based segment-start detection.

Scope
-----
- successful construction
- substring matching behavior
- non-matching behavior
- invalid keyword validation
"""

from __future__ import annotations

import pytest

from record_segmentation.detectors.keyword import KeywordDetector
from record_segmentation.errors import InvalidConfigError

# ============================================================================
# Construction
# ============================================================================


def test_keyword_detector_accepts_non_empty_keyword() -> None:
    """
    KeywordDetector should preserve the configured keyword.
    """
    detector = KeywordDetector("START")

    assert detector.keyword == "START"


# ============================================================================
# Matching behavior
# ============================================================================


def test_keyword_detector_matches_when_keyword_is_present() -> None:
    """
    A line should be treated as a segment start when it contains the keyword.
    """
    detector = KeywordDetector("START")

    assert detector.is_segment_start("START alpha\n") is True
    assert detector.is_segment_start("prefix START suffix\n") is True


def test_keyword_detector_does_not_match_when_keyword_is_absent() -> None:
    """
    A line should not be treated as a segment start when the keyword is absent.
    """
    detector = KeywordDetector("START")

    assert detector.is_segment_start("alpha line 1\n") is False
    assert detector.is_segment_start("begin alpha\n") is False


def test_keyword_detector_is_case_sensitive_by_default() -> None:
    """
    Keyword matching should remain case-sensitive in v1.
    """
    detector = KeywordDetector("START")

    assert detector.is_segment_start("START alpha\n") is True
    assert detector.is_segment_start("start alpha\n") is False


def test_keyword_detector_matches_single_character_keyword() -> None:
    """
    Even a single-character keyword should behave as a standard containment
    match.
    """
    detector = KeywordDetector("#")

    assert detector.is_segment_start("# header\n") is True
    assert detector.is_segment_start("value # marker\n") is True
    assert detector.is_segment_start("plain text\n") is False


# ============================================================================
# Validation
# ============================================================================


@pytest.mark.parametrize(
    "keyword",
    [
        "",
        None,
        123,
    ],
)
def test_keyword_detector_rejects_invalid_keyword(keyword: object) -> None:
    """
    KeywordDetector should reject invalid keyword inputs.
    """
    with pytest.raises(InvalidConfigError):
        KeywordDetector(keyword)  # type: ignore[arg-type]
