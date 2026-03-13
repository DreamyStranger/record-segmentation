"""
tests.unit.config.test_models
===============================================================================

Unit tests for `record_segmentation.config.models`.

Overview
--------
These tests validate the behavior of the user-facing configuration model used
to construct detectors and control splitting behavior.

Scope
-----
- default values
- field assignment
- coexistence of keyword and regex inputs
- immutability guarantees
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from record_segmentation.config.models import SegmentConfig

# ============================================================================
# Defaults
# ============================================================================


def test_segment_config_defaults_are_v1_safe() -> None:
    """
    SegmentConfig should expose the expected conservative v1 defaults.
    """
    cfg = SegmentConfig()

    assert cfg.start_keyword is None
    assert cfg.start_regex is None
    assert cfg.include_preamble is False
    assert cfg.emit_empty_segments is False


# ============================================================================
# Field assignment
# ============================================================================


def test_segment_config_accepts_keyword_configuration() -> None:
    """
    SegmentConfig should preserve a provided start keyword exactly as given.
    """
    cfg = SegmentConfig(start_keyword="START")

    assert cfg.start_keyword == "START"
    assert cfg.start_regex is None


def test_segment_config_accepts_regex_configuration() -> None:
    """
    SegmentConfig should preserve a provided start regex exactly as given.
    """
    cfg = SegmentConfig(start_regex=r"^\d{4}-\d{2}-\d{2}")

    assert cfg.start_keyword is None
    assert cfg.start_regex == r"^\d{4}-\d{2}-\d{2}"


def test_segment_config_accepts_behavior_flags() -> None:
    """
    SegmentConfig should store splitter-related behavior flags.
    """
    cfg = SegmentConfig(
        start_keyword="START",
        include_preamble=True,
        emit_empty_segments=True,
    )

    assert cfg.start_keyword == "START"
    assert cfg.include_preamble is True
    assert cfg.emit_empty_segments is True


# ============================================================================
# Coexisting inputs
# ============================================================================


def test_segment_config_allows_both_keyword_and_regex_to_be_present() -> None:
    """
    SegmentConfig may contain both keyword and regex inputs.

    Precedence is resolved later by detector-construction logic, not by the
    dataclass itself.
    """
    cfg = SegmentConfig(
        start_keyword="START",
        start_regex=r"^\d{4}-\d{2}-\d{2}",
    )

    assert cfg.start_keyword == "START"
    assert cfg.start_regex == r"^\d{4}-\d{2}-\d{2}"


# ============================================================================
# Immutability
# ============================================================================


def test_segment_config_is_frozen() -> None:
    """
    SegmentConfig should be immutable once created.
    """
    cfg = SegmentConfig(start_keyword="START")

    with pytest.raises(FrozenInstanceError):
        cfg.start_keyword = "OTHER"  # type: ignore[misc]


def test_segment_config_uses_slots() -> None:
    """
    SegmentConfig should not allow arbitrary dynamic attributes.
    """
    cfg = SegmentConfig(start_keyword="START")

    with pytest.raises((AttributeError, TypeError)):
        cfg.some_new_attribute = "value"  # type: ignore[attr-defined]
