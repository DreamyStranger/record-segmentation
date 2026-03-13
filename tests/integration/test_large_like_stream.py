"""
tests.integration.test_large_like_stream
===============================================================================

Integration tests for large-like streamed input.

Overview
--------
These tests do not attempt true performance benchmarking. Instead, they validate
correctness over larger synthetic inputs that resemble long-running streaming
workloads.

Scope
-----
- many records in a generator-driven stream
- consistent segment counts
- correct first/last segment content
"""

from __future__ import annotations

from collections.abc import Iterator

from record_segmentation import SegmentConfig, build_detector, split_segments


def _large_like_stream(
    record_count: int, payload_lines_per_record: int
) -> Iterator[str]:
    """
    Generate a long, deterministic stream of synthetic records.
    """
    for idx in range(record_count):
        yield f"START record-{idx}\n"
        for payload_idx in range(payload_lines_per_record):
            yield f"payload {idx}:{payload_idx}\n"


def test_split_segments_handles_many_streamed_records() -> None:
    """
    The splitter should produce the correct number of segments for a larger
    synthetic stream.
    """
    detector = build_detector(SegmentConfig(start_keyword="START"))

    segments = list(split_segments(_large_like_stream(100, 3), detector))

    assert len(segments) == 100
    assert segments[0] == [
        "START record-0\n",
        "payload 0:0\n",
        "payload 0:1\n",
        "payload 0:2\n",
    ]
    assert segments[-1] == [
        "START record-99\n",
        "payload 99:0\n",
        "payload 99:1\n",
        "payload 99:2\n",
    ]


def test_split_segments_preserves_expected_segment_size_across_large_like_stream() -> (
    None
):
    """
    Each emitted segment should preserve the expected number of lines across a
    long synthetic stream.
    """
    detector = build_detector(SegmentConfig(start_keyword="START"))

    segments = list(split_segments(_large_like_stream(25, 5), detector))

    assert len(segments) == 25
    assert all(len(segment) == 6 for segment in segments)


def test_large_like_stream_with_zero_payload_lines_still_emits_header_only_segments(
) -> None:
    """
    Records with no payload lines should still yield valid one-line segments.
    """
    detector = build_detector(SegmentConfig(start_keyword="START"))

    segments = list(split_segments(_large_like_stream(10, 0), detector))

    assert len(segments) == 10
    assert segments[0] == ["START record-0\n"]
    assert segments[-1] == ["START record-9\n"]
