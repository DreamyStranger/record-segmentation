"""
tests.unit.splitters.test_policies
===============================================================================

Unit tests for `record_segmentation.splitters.policies`.

Overview
--------
These tests validate the small policy surface used by the v1 splitter.

Scope
-----
- enum values
- boolean-to-policy resolution
"""

from __future__ import annotations

from record_segmentation.splitters.policies import (
    PreamblePolicy,
    resolve_preamble_policy,
)

# ============================================================================
# Enum behavior
# ============================================================================


def test_preamble_policy_enum_values_are_stable() -> None:
    """
    PreamblePolicy should expose stable string values for public/internal use.
    """
    assert PreamblePolicy.IGNORE.value == "ignore"
    assert PreamblePolicy.INCLUDE.value == "include"


# ============================================================================
# Resolution
# ============================================================================


def test_resolve_preamble_policy_returns_ignore_for_false() -> None:
    """
    False should resolve to the IGNORE preamble policy.
    """
    assert resolve_preamble_policy(False) is PreamblePolicy.IGNORE


def test_resolve_preamble_policy_returns_include_for_true() -> None:
    """
    True should resolve to the INCLUDE preamble policy.
    """
    assert resolve_preamble_policy(True) is PreamblePolicy.INCLUDE
