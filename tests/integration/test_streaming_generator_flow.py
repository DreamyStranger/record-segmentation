"""
tests.integration.test_streaming_generator_flow
===============================================================================

Integration tests for true streaming-style generator input.

Overview
--------
These tests validate that detector + splitter flows work correctly when lines
are yielded one by one from generators rather than materialized lists.

Scope
-----
- keyword-based streaming flow
- regex-based streaming flow
- preamble inclusion behavior with generator input
"""

from __future__ import annotations

from collections.abc import Iterator

from record_segmentation import SegmentConfig, build_detector, split_segments


def _yield_lines(lines: list[str]) -> Iterator[str]:
    """
    Yield lines one by one to simulate streaming input.
    """
    yield from lines


def test_keyword_detector_and_splitter_work_with_generator_input(
    basic_lines: list[str],
) -> None:
    """
    The public detector-builder + splitter flow should work correctly with a
    generator that yields lines incrementally.
    """
    detector = build_detector(SegmentConfig(start_keyword="START"))

    result = list(split_segments(_yield_lines(basic_lines), detector))

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


def test_regex_detector_and_splitter_work_with_generator_input(
    timestamp_lines: list[str],
) -> None:
    """
    Regex-based segmentation should also work correctly with generator input.
    """
    detector = build_detector(SegmentConfig(start_regex=r"^\d{4}-\d{2}-\d{2}"))

    result = list(split_segments(_yield_lines(timestamp_lines), detector))

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


def test_generator_input_respects_preamble_inclusion() -> None:
    """
    Preamble behavior should remain correct when input is streamed from a
    generator.
    """
    lines = [
        "noise line 1\n",
        "noise line 2\n",
        "START alpha\n",
        "alpha line 1\n",
    ]

    detector = build_detector(SegmentConfig(start_keyword="START"))

    result = list(
        split_segments(
            _yield_lines(lines),
            detector,
            include_preamble=True,
        )
    )

    assert result == [
        [
            "noise line 1\n",
            "noise line 2\n",
        ],
        [
            "START alpha\n",
            "alpha line 1\n",
        ],
    ]
