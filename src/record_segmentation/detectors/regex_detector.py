"""
record_segmentation.detectors.regex_detector
===============================================================================

Regex-based segment-start detection.

Overview
--------
`RegexDetector` treats a line as the start of a new segment when a compiled
regular expression matches the line via `Pattern.search()`.

This detector is suitable for cases where boundaries are described by patterns
such as:

- anchored timestamps
- structured headers
- line prefixes with variable content
- domain-specific record formats

Design notes
------------
- Regex patterns are compiled exactly once at initialization unless a compiled
  pattern is supplied directly.
- The hot path is a single stored predicate calling `Pattern.search()`.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from re import Pattern

# External package boundaries
from ..errors import InvalidConfigError

# Local detector implementation
from .base import BaseDetector


class RegexDetector(BaseDetector):
    """
    Detect segment starts using a compiled regular expression.

    A line is considered a segment start if `pattern.search(line)` succeeds.
    """

    __slots__ = ("pattern", "_check")

    def __init__(
        self,
        pattern: str | Pattern[str],
        *,
        flags: int = 0,
    ):
        """
        Initialize the detector.

        Args:
            pattern:
                A non-empty regex pattern string or a precompiled regex object.
            flags:
                Regex flags used only when `pattern` is provided as a string.

        Raises:
            InvalidConfigError:
                If `pattern` is invalid or empty.
        """
        compiled: Pattern[str]

        if isinstance(pattern, re.Pattern):
            compiled = pattern
        elif isinstance(pattern, str) and pattern:
            try:
                compiled = re.compile(pattern, flags)
            except re.error as exc:
                raise InvalidConfigError(
                    f"Invalid regular expression for RegexDetector: {exc}"
                ) from exc
        else:
            raise InvalidConfigError(
                "'pattern' must be a non-empty regex string or compiled pattern."
            )

        self.pattern = compiled

        def _check(line: str, *, _pattern: Pattern[str] = compiled) -> bool:
            return _pattern.search(line) is not None

        self._check: Callable[[str], bool] = _check

    def is_segment_start(self, line: str) -> bool:
        """
        Return True if the regex pattern matches `line`.
        """
        return self._check(line)
