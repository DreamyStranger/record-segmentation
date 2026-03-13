"""
tests.unit.detectors.test_predicate
===============================================================================

Unit tests for `record_segmentation.detectors.predicate`.

Overview
--------
These tests validate predicate-based segment-start detection.

Scope
-----
- detector construction
- predicate-based matching behavior
- truthy/falsey coercion semantics
- validation of predicate input
"""

from __future__ import annotations

import pytest

from record_segmentation.detectors.predicate import PredicateDetector
from record_segmentation.errors import InvalidConfigError

# ============================================================================
# Construction
# ============================================================================


def test_predicate_detector_accepts_callable() -> None:
    """
    PredicateDetector should accept and store a callable predicate.
    """

    def predicate(line: str) -> bool:
        return line.startswith("START")

    detector = PredicateDetector(predicate)

    assert detector.predicate is predicate


# ============================================================================
# Matching behavior
# ============================================================================


def test_predicate_detector_returns_true_when_predicate_true() -> None:
    """
    A line should be treated as a segment start when the predicate returns True.
    """
    detector = PredicateDetector(lambda line: line.startswith("START"))

    assert detector.is_segment_start("START alpha\n") is True
    assert detector.is_segment_start("START beta\n") is True


def test_predicate_detector_returns_false_when_predicate_false() -> None:
    """
    A line should not be treated as a segment start when the predicate returns
    False.
    """
    detector = PredicateDetector(lambda line: line.startswith("START"))

    assert detector.is_segment_start("alpha line\n") is False
    assert detector.is_segment_start("beta line\n") is False


# ============================================================================
# Truthy / falsey coercion
# ============================================================================


def test_predicate_detector_coerces_truthy_values() -> None:
    """
    The detector should interpret truthy predicate results as True.
    """
    detector = PredicateDetector(
        lambda line: "START" if line.startswith("START") else ""
    )

    assert detector.is_segment_start("START alpha\n") is True
    assert detector.is_segment_start("alpha\n") is False


def test_predicate_detector_coerces_falsy_non_bool_values() -> None:
    """
    The detector should interpret falsy non-bool values as False and truthy
    non-bool values as True.
    """
    detector = PredicateDetector(lambda line: [] if line.startswith("START") else [1])

    assert detector.is_segment_start("START alpha\n") is False
    assert detector.is_segment_start("alpha\n") is True


# ============================================================================
# Validation
# ============================================================================


def test_predicate_detector_rejects_none_predicate() -> None:
    """
    PredicateDetector should reject None as a predicate input.
    """
    with pytest.raises(InvalidConfigError):
        PredicateDetector(None)  # type: ignore[arg-type]


def test_predicate_detector_rejects_integer_predicate() -> None:
    """
    PredicateDetector should reject integer predicate inputs.
    """
    with pytest.raises(InvalidConfigError):
        PredicateDetector(123)  # type: ignore[arg-type]


def test_predicate_detector_rejects_string_predicate() -> None:
    """
    PredicateDetector should reject string predicate inputs.
    """
    with pytest.raises(InvalidConfigError):
        PredicateDetector("not callable")  # type: ignore[arg-type]
