"""
record_segmentation.detectors.predicate
===============================================================================

Predicate-based segment-start detection.

Overview
--------
`PredicateDetector` delegates segment-start detection to a user-supplied
callable.

This is the most flexible detector and is useful when boundary logic cannot be
expressed cleanly as a simple keyword or regular expression.

Examples
--------
    PredicateDetector(lambda line: line.startswith("BEGIN "))
    PredicateDetector(lambda line: line.count("|") >= 5)

Design notes
------------
- This detector intentionally does not impose semantics beyond "call the
  predicate and interpret its return value as truthy/falsey".
- Use this for advanced/custom detection rules.
"""

from __future__ import annotations

from collections.abc import Callable

# External package boundaries
from ..errors import InvalidConfigError

# Local detector implementation
from .base import BaseDetector


class PredicateDetector(BaseDetector):
    """
    Detect segment starts using a user-provided callable predicate.
    """

    __slots__ = ("predicate",)

    def __init__(self, predicate: Callable[[str], bool]):
        """
        Initialize the detector.

        Args:
            predicate:
                Callable receiving a single line and returning True when the
                line starts a new segment.

        Raises:
            InvalidConfigError:
                If `predicate` is not callable.
        """
        if not callable(predicate):
            raise InvalidConfigError(
                "'predicate' must be callable for PredicateDetector."
            )

        self.predicate = predicate

    def is_segment_start(self, line: str) -> bool:
        """
        Return True if the configured predicate evaluates truthy for `line`.
        """
        return bool(self.predicate(line))
