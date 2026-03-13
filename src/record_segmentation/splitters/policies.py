"""
record_segmentation.splitters.policies
===============================================================================

Splitter policy definitions.

Overview
--------
This module defines the small policy surface used by the v1 splitter.

Current scope
-------------
v1 supports a single user-visible policy dimension:

- how to handle lines that appear before the first detected segment start

The supported behaviors are intentionally minimal to keep streaming semantics
clear and predictable.
"""

from __future__ import annotations

from enum import Enum


class PreamblePolicy(str, Enum):
    """
    Policy for handling lines before the first detected segment start.

    Members:
        IGNORE:
            Drop all lines before the first segment start.
        INCLUDE:
            Emit those lines as an initial segment.
    """

    IGNORE = "ignore"
    INCLUDE = "include"


def resolve_preamble_policy(include_preamble: bool) -> PreamblePolicy:
    """
    Resolve the configured preamble behavior into a concrete policy enum.

    Args:
        include_preamble:
            User-facing boolean configuration.

    Returns:
        The corresponding `PreamblePolicy`.
    """
    return PreamblePolicy.INCLUDE if include_preamble else PreamblePolicy.IGNORE
