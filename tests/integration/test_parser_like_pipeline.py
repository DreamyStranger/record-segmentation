"""
tests.integration.test_parser_like_pipeline
===============================================================================

Integration tests for a parser-like consumer pipeline.

Overview
--------
These tests validate that `record_segmentation` integrates naturally into a
higher-level parsing flow where:

- a detector identifies record boundaries
- a splitter groups lines into segments
- a consumer builds one structured record per segment

This mirrors the intended real-world usage pattern of the library.
"""

from __future__ import annotations

from record_segmentation import SegmentConfig, build_detector, split_segments


def _extract_fields_from_segment(segment: list[str]) -> dict[str, str | int | None]:
    """
    Simulate a tiny parser/extractor that derives a structured record from a
    segment.

    The implementation is intentionally simple and deterministic for testing.
    """
    header = segment[0].rstrip("\n")
    payload_line_count = max(len(segment) - 1, 0)

    return {
        "header": header,
        "line_count": len(segment),
        "payload_line_count": payload_line_count,
        "contains_error": int(any("ERROR" in line for line in segment)),
    }


def test_parser_like_pipeline_builds_one_record_per_segment() -> None:
    """
    A parser-style consumer should be able to build one structured record from
    each emitted segment.
    """
    lines = [
        "START alpha\n",
        "payload a1\n",
        "payload a2\n",
        "START beta\n",
        "payload b1\n",
    ]

    detector = build_detector(SegmentConfig(start_keyword="START"))

    records = [
        _extract_fields_from_segment(segment)
        for segment in split_segments(lines, detector)
    ]

    assert records == [
        {
            "header": "START alpha",
            "line_count": 3,
            "payload_line_count": 2,
            "contains_error": 0,
        },
        {
            "header": "START beta",
            "line_count": 2,
            "payload_line_count": 1,
            "contains_error": 0,
        },
    ]


def test_parser_like_pipeline_handles_multiline_error_segment() -> None:
    """
    A parser-style consumer should be able to process multiline segments,
    including stack-trace-like bodies.
    """
    lines = [
        "2026-03-12 INFO startup\n",
        "init ok\n",
        "2026-03-12 ERROR failure\n",
        "Traceback line 1\n",
        "Traceback line 2\n",
    ]

    detector = build_detector(SegmentConfig(start_regex=r"^\d{4}-\d{2}-\d{2}"))

    records = [
        _extract_fields_from_segment(segment)
        for segment in split_segments(lines, detector)
    ]

    assert records == [
        {
            "header": "2026-03-12 INFO startup",
            "line_count": 2,
            "payload_line_count": 1,
            "contains_error": 0,
        },
        {
            "header": "2026-03-12 ERROR failure",
            "line_count": 3,
            "payload_line_count": 2,
            "contains_error": 1,
        },
    ]


def test_parser_like_pipeline_can_ignore_preamble_like_real_parser() -> None:
    """
    A parser-like consumer should be able to ignore non-record lines before the
    first detected segment start.
    """
    lines = [
        "banner line\n",
        "metadata line\n",
        "START alpha\n",
        "payload a1\n",
    ]

    detector = build_detector(SegmentConfig(start_keyword="START"))

    records = [
        _extract_fields_from_segment(segment)
        for segment in split_segments(lines, detector, include_preamble=False)
    ]

    assert records == [
        {
            "header": "START alpha",
            "line_count": 2,
            "payload_line_count": 1,
            "contains_error": 0,
        }
    ]
