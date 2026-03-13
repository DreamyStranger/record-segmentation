"""
record_segmentation.config.models
===============================================================================

User-facing configuration models.

Overview
--------
This module defines the stable configuration object used to construct record
boundary detectors and control splitting behavior.

Design principles
-----------------
- Small surface area
- Explicit defaults
- Streaming-friendly behavior
- Enough flexibility for common log and text-record use cases
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SegmentConfig:
    """
    Configuration for record-boundary detection and splitting.

    Detection strategy
    ------------------
    Provide one of:

    - `start_keyword`
    - `start_regex`

    If both are provided, `start_keyword` takes precedence.

    Attributes:
        start_keyword:
            Substring used to detect the start of a new segment.
        start_regex:
            Regular expression used to detect the start of a new segment.
        include_preamble:
            If False, lines before the first detected segment are ignored.
            If True, those lines are emitted as an initial segment.
        emit_empty_segments:
            If True, consecutive segment starts may emit empty segments under
            future richer splitting policies. The default False keeps output
            simpler and more intuitive for most users.
    """

    start_keyword: str | None = None
    start_regex: str | None = None
    include_preamble: bool = False
    emit_empty_segments: bool = False
