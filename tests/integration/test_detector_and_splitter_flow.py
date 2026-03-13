"""
tests.integration.test_detector_and_splitter_flow
===============================================================================

Integration tests for detector construction and segment splitting.

Overview
--------
These tests validate the normal end-to-end flow:

    SegmentConfig -> build_detector(...) -> split_segments(...)

Scope
-----
- keyword-based flow
- regex-based flow
- configuration precedence through the public builder
"""

from __future__ import annotations

from record_segmentation import SegmentConfig, build_detector, split_segments
from record_segmentation.detectors.keyword import KeywordDetector
from record_segmentation.detectors.regex_detector import RegexDetector


def test_keyword_config_builds_detector_and_splits_basic_input(
    basic_lines: list[str],
) -> None:
    """
    A keyword-based config should build a working detector that splits input
    into the expected segments.
    """
    detector = build_detector(SegmentConfig(start_keyword="START"))

    assert isinstance(detector, KeywordDetector)

    result = list(split_segments(basic_lines, detector))

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


def test_regex_config_builds_detector_and_splits_timestamp_input(
    timestamp_lines: list[str],
) -> None:
    """
    A regex-based config should build a working detector that splits
    timestamp-prefixed input into the expected segments.
    """
    detector = build_detector(SegmentConfig(start_regex=r"^\d{4}-\d{2}-\d{2}"))

    assert isinstance(detector, RegexDetector)

    result = list(split_segments(timestamp_lines, detector))

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


def test_builder_keyword_precedence_flows_through_splitter() -> None:
    """
    When both keyword and regex are configured, the public builder should
    honor keyword precedence and the resulting detector should drive splitting
    accordingly.
    """
    lines = [
        "noise line\n",
        "START alpha\n",
        "alpha line\n",
        "2026-03-12 not a start for this config\n",
        "START beta\n",
        "beta line\n",
    ]

    detector = build_detector(
        SegmentConfig(
            start_keyword="START",
            start_regex=r"^\d{4}-\d{2}-\d{2}",
        )
    )

    assert isinstance(detector, KeywordDetector)

    result = list(split_segments(lines, detector))

    assert result == [
        [
            "START alpha\n",
            "alpha line\n",
            "2026-03-12 not a start for this config\n",
        ],
        [
            "START beta\n",
            "beta line\n",
        ],
    ]
