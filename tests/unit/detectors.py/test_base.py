"""
tests.unit.detectors.test_base
===============================================================================

Unit tests for `record_segmentation.detectors.base`.

Overview
--------
These tests validate the minimal abstract contract used by all concrete
segment-start detectors.

Scope
-----
- abstract base behavior
- subclass implementation expectations
"""

from __future__ import annotations

import pytest

from record_segmentation.detectors.base import BaseDetector

# ============================================================================
# Abstract contract
# ============================================================================


def test_base_detector_cannot_be_instantiated_directly() -> None:
    """
    BaseDetector should remain abstract and non-instantiable.
    """
    with pytest.raises(TypeError):
        BaseDetector()


def test_base_detector_subclass_must_implement_is_segment_start() -> None:
    """
    A subclass that does not implement the abstract method should remain
    non-instantiable.
    """

    class IncompleteDetector(BaseDetector):
        """Intentionally incomplete detector for abstract-base validation."""

    with pytest.raises(TypeError):
        IncompleteDetector()


# ============================================================================
# Subclass expectations
# ============================================================================


def test_base_detector_subclass_with_implementation_is_usable() -> None:
    """
    A concrete subclass implementing `is_segment_start` should behave like a
    valid detector.
    """

    class ConcreteDetector(BaseDetector):
        """Minimal concrete detector for contract validation."""

        def is_segment_start(self, line: str) -> bool:
            return line.startswith("START")

    detector = ConcreteDetector()

    assert detector.is_segment_start("START alpha\n") is True
    assert detector.is_segment_start("noise line\n") is False


# ============================================================================
# Base method fallback behavior
# ============================================================================


def test_base_detector_base_method_raises_not_implemented_error() -> None:
    """
    A concrete subclass that delegates to the abstract base implementation
    should surface the base class `NotImplementedError`.

    This test exists mainly to exercise the defensive fallback in the abstract
    method body and to keep coverage aligned with the declared base contract.
    """

    class DelegatingDetector(BaseDetector):
        """Concrete detector that intentionally delegates to the base method."""

        def is_segment_start(self, line: str) -> bool:
            return super().is_segment_start(line)

    detector = DelegatingDetector()

    with pytest.raises(NotImplementedError):
        detector.is_segment_start("START alpha\n")
