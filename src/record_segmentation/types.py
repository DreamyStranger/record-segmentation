"""
record_segmentation.types
===============================================================================

Shared type aliases and lightweight protocols.

Overview
--------
This module centralizes common typing primitives used across detectors,
splitters, and configuration helpers.

Notes
-----
- Keep this module dependency-light.
- Prefer aliases and protocols that clarify public contracts.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Protocol, TypeAlias

Line: TypeAlias = str
LineIterable: TypeAlias = Iterable[Line]
LineIterator: TypeAlias = Iterator[Line]
LinePredicate: TypeAlias = Callable[[Line], bool]


class SupportsIsSegmentStart(Protocol):
    """Protocol for detector-like objects accepted by splitters."""

    def is_segment_start(self, line: str) -> bool:
        """
        Return True if `line` marks the start of a new segment.

        Args:
            line:
                A single input line. The line may or may not include a trailing
                newline depending on the upstream source.

        Returns:
            True if the line begins a new logical record/segment.
        """
        ...
