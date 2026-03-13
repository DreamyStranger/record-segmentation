"""
record_segmentation.detectors.base
===============================================================================

Base detector protocol and shared detector contracts.

Overview
--------
A detector is any object that can answer a single question for a given line:

    "Does this line start a new segment?"

This module defines the small common base used by concrete detector
implementations.

Design notes
------------
- Keep the runtime contract minimal.
- Favor composition over inheritance where possible.
- Concrete detectors should preselect their hot-path predicate during
  initialization when practical.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseDetector(ABC):
    """
    Abstract base class for segment-start detectors.

    Concrete subclasses must implement `is_segment_start(line)`.
    """

    __slots__ = ()

    @abstractmethod
    def is_segment_start(self, line: str) -> bool:
        """
        Return True if `line` marks the start of a new segment.

        Args:
            line:
                A single input line. The line may or may not include a trailing
                newline depending on the upstream source.

        Returns:
            True if the line should be treated as a segment boundary/start.
        """
        raise NotImplementedError
