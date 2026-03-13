"""
record_segmentation.detectors.keyword
===============================================================================

Keyword-based segment-start detection.

Overview
--------
`KeywordDetector` treats a line as the start of a new segment when a configured
keyword is present in the line.

This detector is intentionally simple and fast. It is often appropriate when
record boundaries are introduced by stable markers such as:

- timestamps
- level labels
- header tokens
- domain-specific record prefixes

Examples
--------
    KeywordDetector("ERROR")
    KeywordDetector("[SESSION_START]")

Design notes
------------
- The hot path is a single preselected check stored at initialization.
- Empty keywords are rejected.
"""

from __future__ import annotations

from collections.abc import Callable

# External package boundaries
from ..errors import InvalidConfigError

# Local detector implementation
from .base import BaseDetector


class KeywordDetector(BaseDetector):
    """
    Detect segment starts using substring containment.

    A line is considered a segment start if `keyword in line` evaluates True.

    Attributes:
        keyword:
            The configured non-empty keyword.
    """

    __slots__ = ("keyword", "_check")

    def __init__(self, keyword: str):
        """
        Initialize the detector.

        Args:
            keyword:
                Non-empty substring used to identify segment starts.

        Raises:
            InvalidConfigError:
                If `keyword` is not a non-empty string.
        """
        if not isinstance(keyword, str) or not keyword:
            raise InvalidConfigError(
                "'keyword' must be a non-empty string for KeywordDetector."
            )

        self.keyword = keyword

        def _check(line: str, *, _kw: str = keyword) -> bool:
            return _kw in line

        self._check: Callable[[str], bool] = _check

    def is_segment_start(self, line: str) -> bool:
        """
        Return True if the configured keyword is present in `line`.
        """
        return self._check(line)
