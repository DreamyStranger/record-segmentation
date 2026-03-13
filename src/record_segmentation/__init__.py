"""
record_segmentation
===============================================================================

Streaming record-boundary detection and splitting for line-oriented text.

Overview
--------
`record_segmentation` provides small, composable primitives for:

- detecting the start of logical records in a stream of lines
- splitting an input line stream into record segments
- supporting keyword-, regex-, and predicate-based boundary detection

Design goals
------------
- Streaming-first
- Small, stable public API
- Minimal hot-path overhead
- Easy integration into parsers and ETL pipelines
- Strong typing and predictable behavior

Typical usage
-------------
    from record_segmentation import SegmentConfig, build_detector, split_segments

    detector = build_detector(SegmentConfig(start_regex=r"^\\d{4}-\\d{2}-\\d{2}"))

    for segment in split_segments(lines, detector):
        ...

Public API
----------
The symbols re-exported here form the intended stable import surface for users.
"""

from .builders import build_detector
from .config.models import SegmentConfig
from .detectors.base import BaseDetector
from .detectors.keyword import KeywordDetector
from .detectors.predicate import PredicateDetector
from .detectors.regex_detector import RegexDetector
from .errors import InvalidConfigError, RecordSegmentationError, SegmentSplitError
from .models.segment import Segment
from .splitters import split_segments

__all__ = [
    "BaseDetector",
    "InvalidConfigError",
    "KeywordDetector",
    "PredicateDetector",
    "RecordSegmentationError",
    "RegexDetector",
    "Segment",
    "SegmentConfig",
    "SegmentSplitError",
    "build_detector",
    "split_segments",
]

__version__ = "0.1.0"
