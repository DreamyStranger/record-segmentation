"""
tests.unit.test_builders
===============================================================================

Unit tests for `record_segmentation.builders`.

Overview
--------
These tests validate the public builder helpers that normalize user-facing
configuration into concrete runtime objects.

Scope
-----
- building from SegmentConfig
- building from dict input
- precedence behavior via builder entrypoint
- invalid input handling
"""

from __future__ import annotations

import pytest

from record_segmentation.builders import build_detector
from record_segmentation.config.models import SegmentConfig
from record_segmentation.detectors.keyword import KeywordDetector
from record_segmentation.detectors.regex_detector import RegexDetector
from record_segmentation.errors import InvalidConfigError

# ============================================================================
# SegmentConfig input
# ============================================================================


def test_build_detector_accepts_segment_config_keyword() -> None:
    """
    build_detector should construct a KeywordDetector from keyword config.
    """
    cfg = SegmentConfig(start_keyword="START")

    detector = build_detector(cfg)

    assert isinstance(detector, KeywordDetector)
    assert detector.keyword == "START"


def test_build_detector_accepts_segment_config_regex() -> None:
    """
    build_detector should construct a RegexDetector from regex config.
    """
    cfg = SegmentConfig(start_regex=r"^\d{4}-\d{2}-\d{2}")

    detector = build_detector(cfg)

    assert isinstance(detector, RegexDetector)
    assert detector.pattern.pattern == r"^\d{4}-\d{2}-\d{2}"


# ============================================================================
# Mapping input
# ============================================================================


def test_build_detector_accepts_mapping_keyword_config() -> None:
    """
    build_detector should normalize a compatible dict into SegmentConfig.
    """
    detector = build_detector({"start_keyword": "START"})

    assert isinstance(detector, KeywordDetector)
    assert detector.keyword == "START"


def test_build_detector_accepts_mapping_regex_config() -> None:
    """
    build_detector should normalize a compatible dict containing regex config.
    """
    detector = build_detector({"start_regex": r"^\d{4}-\d{2}-\d{2}"})

    assert isinstance(detector, RegexDetector)
    assert detector.pattern.pattern == r"^\d{4}-\d{2}-\d{2}"


# ============================================================================
# Precedence
# ============================================================================


def test_build_detector_keyword_takes_precedence_over_regex_from_mapping() -> None:
    """
    When both keyword and regex are present in mapping input, keyword should
    take precedence.
    """
    detector = build_detector(
        {
            "start_keyword": "START",
            "start_regex": r"^\d{4}-\d{2}-\d{2}",
        }
    )

    assert isinstance(detector, KeywordDetector)
    assert detector.keyword == "START"


# ============================================================================
# Validation
# ============================================================================


def test_build_detector_rejects_config_without_strategy() -> None:
    """
    build_detector should reject configs that define no usable strategy.
    """
    with pytest.raises(InvalidConfigError):
        build_detector(SegmentConfig())


def test_build_detector_rejects_invalid_mapping_fields() -> None:
    """
    build_detector should reject mappings that cannot be normalized into
    SegmentConfig.
    """
    with pytest.raises(InvalidConfigError):
        build_detector({"unknown_field": "value"})  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "value",
    [
        None,
        123,
        "invalid",
        3.14,
        object(),
    ],
)
def test_build_detector_rejects_non_config_non_mapping(value: object) -> None:
    """
    build_detector should reject unsupported input types.
    """
    with pytest.raises(InvalidConfigError):
        build_detector(value)  # type: ignore[arg-type]

# ============================================================================
# Mapping field validation
# ============================================================================


def test_build_detector_rejects_non_string_start_keyword_in_mapping() -> None:
    """
    build_detector should reject mapping input whose `start_keyword` value is
    neither a string nor None.
    """
    with pytest.raises(
        InvalidConfigError,
        match="'start_keyword' must be a string or None.",
    ):
        build_detector({"start_keyword": 123})  # type: ignore[arg-type]


def test_build_detector_rejects_non_string_start_regex_in_mapping() -> None:
    """
    build_detector should reject mapping input whose `start_regex` value is
    neither a string nor None.
    """
    with pytest.raises(
        InvalidConfigError,
        match="'start_regex' must be a string or None.",
    ):
        build_detector({"start_regex": 123})  # type: ignore[arg-type]


def test_build_detector_rejects_non_bool_include_preamble_in_mapping() -> None:
    """
    build_detector should reject mapping input whose `include_preamble` value is
    not a boolean.
    """
    with pytest.raises(
        InvalidConfigError,
        match="'include_preamble' must be a bool.",
    ):
        build_detector(
            {
                "start_keyword": "START",
                "include_preamble": "yes",
            }
        )


def test_build_detector_rejects_non_bool_emit_empty_segments_in_mapping() -> None:
    """
    build_detector should reject mapping input whose `emit_empty_segments` value
    is not a boolean.
    """
    with pytest.raises(
        InvalidConfigError,
        match="'emit_empty_segments' must be a bool.",
    ):
        build_detector(
            {
                "start_keyword": "START",
                "emit_empty_segments": "no",
            }
        )