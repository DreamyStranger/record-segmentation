"""
record_segmentation.models.segment
===============================================================================

Runtime segment model.

Overview
--------
`Segment` represents one logical record extracted from a line stream.

This object is intentionally lightweight and can be used by higher-level code
that wants more structure than a raw `list[str]`.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Segment:
    """
    A logical segment consisting of one or more lines.

    Attributes:
        lines:
            The lines contained in the segment, in original order.
        index:
            Zero-based segment index in the emitted stream, if known.
        start_line_number:
            One-based input line number for the first line in the segment, if
            tracked by the caller/splitter.
        end_line_number:
            One-based input line number for the last line in the segment, if
            tracked by the caller/splitter.
    """

    lines: list[str] = field(default_factory=list)
    index: int | None = None
    start_line_number: int | None = None
    end_line_number: int | None = None

    @property
    def is_empty(self) -> bool:
        """Return True if the segment contains no lines."""
        return not self.lines

    @property
    def first_line(self) -> str | None:
        """Return the first line in the segment, or None if empty."""
        return self.lines[0] if self.lines else None

    @property
    def last_line(self) -> str | None:
        """Return the last line in the segment, or None if empty."""
        return self.lines[-1] if self.lines else None

    def __len__(self) -> int:
        """Return the number of lines in the segment."""
        return len(self.lines)
