"""
record_segmentation.errors
===============================================================================

Library exception hierarchy.

Overview
--------
This module defines the public exception types raised by `record_segmentation`.

Design notes
------------
- Exceptions are intentionally small and stable.
- Users should be able to catch a single top-level library exception when
  desired, or handle narrower failures such as invalid configuration.
"""


class RecordSegmentationError(Exception):
    """Base exception for all library-specific errors."""


class InvalidConfigError(RecordSegmentationError, ValueError):
    """Raised when configuration is missing, invalid, or internally inconsistent."""


class SegmentSplitError(RecordSegmentationError):
    """Raised when segment splitting cannot proceed under the configured policy."""
