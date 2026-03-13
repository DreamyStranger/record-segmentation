"""
tests.unit.test_types
===============================================================================

Unit tests for `record_segmentation.types`.

Overview
--------
This module lightly validates the runtime-facing aspects of shared typing
contracts.

Notes
-----
Most content in `record_segmentation.types` is static typing metadata and does
not require extensive runtime testing. These tests focus on the small detector
protocol contract used by the splitter layer.
"""

from __future__ import annotations

from record_segmentation.types import SupportsIsSegmentStart


class DetectorLike:
    """
    Minimal detector-like object satisfying the protocol contract at runtime.
    """

    def is_segment_start(self, line: str) -> bool:
        return line.startswith("START")


def test_detector_like_object_exposes_expected_protocol_method() -> None:
    """
    A detector-like object should expose a callable `is_segment_start` method.
    """
    detector = DetectorLike()

    assert hasattr(detector, "is_segment_start")
    assert callable(detector.is_segment_start)
    assert detector.is_segment_start("START alpha\n") is True
    assert detector.is_segment_start("noise\n") is False


def test_supports_is_segment_start_can_be_used_as_annotation_symbol() -> None:
    """
    The protocol symbol should be importable and usable in annotations.

    This is a light smoke test for the shared typing contract.
    """

    def accepts_detector(detector: SupportsIsSegmentStart) -> bool:
        return detector.is_segment_start("START alpha\n")

    assert accepts_detector(DetectorLike()) is True
