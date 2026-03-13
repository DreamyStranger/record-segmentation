"""
Shared pytest fixtures for the `record_segmentation` test suite.

Overview
--------
This module provides reusable fixtures for:

- common line streams
- detector instances
- configuration objects
- generator-based streaming inputs

Notes
-----
- Fixtures should stay generic and broadly reusable.
- Module-specific edge cases should usually remain close to the tests that use
  them rather than being promoted here too early.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from record_segmentation import KeywordDetector, RegexDetector, SegmentConfig

# ============================================================================
# Common line inputs
# ============================================================================


@pytest.fixture
def basic_lines() -> list[str]:
    """
    Return a simple multi-segment input with keyword-based starts.
    """
    return [
        "START alpha\n",
        "alpha line 1\n",
        "alpha line 2\n",
        "START beta\n",
        "beta line 1\n",
    ]


@pytest.fixture
def preamble_lines() -> list[str]:
    """
    Return input containing lines before the first detected segment start.
    """
    return [
        "noise line 1\n",
        "noise line 2\n",
        "START alpha\n",
        "alpha line 1\n",
    ]


@pytest.fixture
def consecutive_start_lines() -> list[str]:
    """
    Return input where each line starts a new segment.
    """
    return [
        "START alpha\n",
        "START beta\n",
        "START gamma\n",
    ]


@pytest.fixture
def empty_lines() -> list[str]:
    """
    Return an empty input stream.
    """
    return []


@pytest.fixture
def no_start_lines() -> list[str]:
    """
    Return input with no valid segment start lines.
    """
    return [
        "noise line 1\n",
        "noise line 2\n",
        "noise line 3\n",
    ]


@pytest.fixture
def timestamp_lines() -> list[str]:
    """
    Return input segmented by timestamp-like regex matches.
    """
    return [
        "2026-03-12 INFO startup\n",
        "payload line a\n",
        "2026-03-12 ERROR failure\n",
        "trace line 1\n",
        "trace line 2\n",
    ]


# ============================================================================
# Common detectors
# ============================================================================


@pytest.fixture
def keyword_detector() -> KeywordDetector:
    """
    Return a keyword detector matching 'START'.
    """
    return KeywordDetector("START")


@pytest.fixture
def regex_detector() -> RegexDetector:
    """
    Return a regex detector matching YYYY-MM-DD-prefixed lines.
    """
    return RegexDetector(r"^\d{4}-\d{2}-\d{2}")


# ============================================================================
# Common configs
# ============================================================================


@pytest.fixture
def keyword_config() -> SegmentConfig:
    """
    Return a keyword-based SegmentConfig.
    """
    return SegmentConfig(start_keyword="START")


@pytest.fixture
def regex_config() -> SegmentConfig:
    """
    Return a regex-based SegmentConfig.
    """
    return SegmentConfig(start_regex=r"^\d{4}-\d{2}-\d{2}")


@pytest.fixture
def dual_config() -> SegmentConfig:
    """
    Return a config containing both keyword and regex inputs.

    This is useful for verifying precedence behavior during detector building.
    """
    return SegmentConfig(
        start_keyword="START",
        start_regex=r"^\d{4}-\d{2}-\d{2}",
    )


# ============================================================================
# Streaming inputs
# ============================================================================


@pytest.fixture
def basic_line_generator(basic_lines: list[str]) -> Iterator[str]:
    """
    Return a generator yielding `basic_lines` one by one.

    This simulates true streaming input.
    """
    return (line for line in basic_lines)


@pytest.fixture
def timestamp_line_generator(timestamp_lines: list[str]) -> Iterator[str]:
    """
    Return a generator yielding `timestamp_lines` one by one.

    This simulates regex-based streaming segmentation input.
    """
    return (line for line in timestamp_lines)
