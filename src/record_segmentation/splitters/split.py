"""
record_segmentation.splitters.split
===============================================================================

Streaming segment splitting.

Overview
--------
This module provides the core v1 splitting primitive:

    `split_segments(lines, detector, ...)`

The function consumes a line-oriented iterable and groups lines into logical
segments using a start-boundary detector. A new segment begins whenever the
detector reports that a line is a segment start.

Behavior summary
----------------
- Streaming only: input is consumed one line at a time.
- Start-boundary driven: a matching line begins a new segment.
- Final flush: the last open segment is emitted at end-of-input.
- Preamble policy:
    - ignore lines before first segment start, or
    - emit them as an initial segment

Non-goals (v1)
--------------
- Explicit end-boundary support
- Nested segment structures
- Segment validation
- Partial/incremental resume state across separate calls
"""

from __future__ import annotations

from collections.abc import Iterator

# External package boundaries
from ..errors import SegmentSplitError
from ..types import LineIterable, SupportsIsSegmentStart

# Local splitter implementation
from .policies import PreamblePolicy, resolve_preamble_policy


def split_segments(
    lines: LineIterable,
    detector: SupportsIsSegmentStart,
    *,
    include_preamble: bool = False,
) -> Iterator[list[str]]:
    """
    Split a line stream into logical segments.

    A new segment begins whenever `detector.is_segment_start(line)` returns
    True. The previous segment, if any, is emitted immediately before the new
    one is opened. The final open segment is emitted when the input is
    exhausted.

    Args:
        lines:
            Any iterable yielding text lines one by one. This may be a list,
            generator, file handle, or any streaming line source.
        detector:
            Any object implementing `is_segment_start(line: str) -> bool`.
        include_preamble:
            Controls handling of lines appearing before the first detected
            segment start.

            - False:
                ignore all preamble lines
            - True:
                emit preamble lines as the first segment

    Yields:
        Lists of lines, where each list represents one logical segment.

    Raises:
        SegmentSplitError:
            If the provided detector does not expose a usable
            `is_segment_start` method.

    Notes
    -----
    - The splitter does not strip newlines or otherwise normalize line content.
      It preserves exactly what the upstream iterable yields.
    - Empty input yields no segments.
    - Consecutive segment-start lines produce distinct one-line segments.
    """
    if not hasattr(detector, "is_segment_start") or not callable(
        detector.is_segment_start
    ):
        raise SegmentSplitError(
            "'detector' must define a callable is_segment_start(line) method."
        )

    policy = resolve_preamble_policy(include_preamble)

    current: list[str] = []
    seen_first_start = False

    for line in lines:
        is_start = detector.is_segment_start(line)

        if is_start:
            if seen_first_start:
                if current:
                    yield current
            else:
                seen_first_start = True
                if policy is PreamblePolicy.INCLUDE and current:
                    yield current

            current = [line]
            continue

        if seen_first_start:
            current.append(line)
            continue

        if policy is PreamblePolicy.INCLUDE:
            current.append(line)

    if current:
        if seen_first_start:
            yield current
        elif policy is PreamblePolicy.INCLUDE:
            yield current
