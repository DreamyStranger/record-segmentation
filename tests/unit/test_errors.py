"""
tests.unit.test_errors
===============================================================================

Unit tests for `record_segmentation.errors`.

Overview
--------
These tests validate the public exception hierarchy exposed by the library.

Scope
-----
- inheritance relationships
- catchability through the top-level library exception
"""

from __future__ import annotations

from record_segmentation.errors import (
    InvalidConfigError,
    RecordSegmentationError,
    SegmentSplitError,
)

# ============================================================================
# Inheritance
# ============================================================================


def test_invalid_config_error_inherits_expected_bases() -> None:
    """
    InvalidConfigError should be both a library error and a ValueError.
    """
    err = InvalidConfigError("bad config")

    assert isinstance(err, InvalidConfigError)
    assert isinstance(err, RecordSegmentationError)
    assert isinstance(err, ValueError)


def test_segment_split_error_inherits_library_base() -> None:
    """
    SegmentSplitError should inherit from the top-level library exception.
    """
    err = SegmentSplitError("split failed")

    assert isinstance(err, SegmentSplitError)
    assert isinstance(err, RecordSegmentationError)


# ============================================================================
# Catchability
# ============================================================================


def test_top_level_library_error_catches_invalid_config_error() -> None:
    """
    Consumers should be able to catch InvalidConfigError via the top-level
    library exception type.
    """
    caught = False

    try:
        raise InvalidConfigError("bad config")
    except RecordSegmentationError:
        caught = True

    assert caught is True


def test_top_level_library_error_catches_segment_split_error() -> None:
    """
    Consumers should be able to catch SegmentSplitError via the top-level
    library exception type.
    """
    caught = False

    try:
        raise SegmentSplitError("split failed")
    except RecordSegmentationError:
        caught = True

    assert caught is True
