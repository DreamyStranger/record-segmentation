"""
tests.unit.detectors.test_factory
===============================================================================

Unit tests for `record_segmentation.detectors.factory`.

Overview
--------
These tests validate construction of detectors from `SegmentConfig`.

Scope
-----
- keyword detector construction
- regex detector construction
- precedence rules when both inputs exist
- invalid configuration handling
"""

from __future__ import annotations

import pytest

from record_segmentation.config.models import SegmentConfig
from record_segmentation.detectors.factory import build_detector_from_config
from record_segmentation.detectors.keyword import KeywordDetector
from record_segmentation.detectors.regex_detector import RegexDetector
from record_segmentation.errors import InvalidConfigError

# ============================================================================
# Keyword construction
# ============================================================================


def test_factory_returns_keyword_detector_when_keyword_configured() -> None:
    """
    When start_keyword is defined, the factory should return a KeywordDetector.
    """
    cfg = SegmentConfig(start_keyword="START")

    detector = build_detector_from_config(cfg)

    assert isinstance(detector, KeywordDetector)
    assert detector.keyword == "START"


# ============================================================================
# Regex construction
# ============================================================================


def test_factory_returns_regex_detector_when_only_regex_configured() -> None:
    """
    When start_regex is defined and no keyword is present, a RegexDetector
    should be returned.
    """
    cfg = SegmentConfig(start_regex=r"^\d{4}-\d{2}-\d{2}")

    detector = build_detector_from_config(cfg)

    assert isinstance(detector, RegexDetector)
    assert detector.pattern.pattern == r"^\d{4}-\d{2}-\d{2}"


# ============================================================================
# Precedence
# ============================================================================


def test_factory_keyword_takes_precedence_over_regex() -> None:
    """
    When both keyword and regex are provided, keyword should take precedence.
    """
    cfg = SegmentConfig(
        start_keyword="START",
        start_regex=r"^\d{4}-\d{2}-\d{2}",
    )

    detector = build_detector_from_config(cfg)

    assert isinstance(detector, KeywordDetector)
    assert detector.keyword == "START"


# ============================================================================
# Validation
# ============================================================================


def test_factory_rejects_config_without_detection_strategy() -> None:
    """
    The factory should reject configurations without keyword or regex.
    """
    cfg = SegmentConfig()

    with pytest.raises(InvalidConfigError):
        build_detector_from_config(cfg)


def test_factory_rejects_non_segment_config_input() -> None:
    """
    The factory should reject inputs that are not SegmentConfig instances.
    """
    with pytest.raises(InvalidConfigError):
        build_detector_from_config("invalid")  # type: ignore[arg-type]
