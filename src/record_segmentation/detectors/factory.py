"""
record_segmentation.detectors.factory
===============================================================================

Detector construction helpers.

Overview
--------
This module resolves user-facing configuration into a concrete detector
instance.

Resolution rules
----------------
- If `start_keyword` is a non-empty string, a `KeywordDetector` is created.
- Otherwise, if `start_regex` is a non-empty string, a `RegexDetector` is
  created.
- If neither is available, configuration is invalid.

Precedence
----------
If both `start_keyword` and `start_regex` are provided, `start_keyword`
takes precedence.

Design notes
------------
- Centralizing detector construction keeps precedence and validation rules
  consistent across the package.
"""

from __future__ import annotations

# External package boundaries
from ..config import SegmentConfig
from ..errors import InvalidConfigError

# Local detector implementations
from .base import BaseDetector
from .keyword import KeywordDetector
from .regex_detector import RegexDetector


def build_detector_from_config(cfg: SegmentConfig) -> BaseDetector:
    """
    Build a concrete detector from `SegmentConfig`.

    Args:
        cfg:
            User-facing segment configuration.

    Returns:
        A concrete detector instance selected according to configuration
        precedence rules.

    Raises:
        InvalidConfigError:
            If no usable detection strategy is configured.
    """
    if not isinstance(cfg, SegmentConfig):
        raise InvalidConfigError(
            "'cfg' must be a SegmentConfig instance in build_detector_from_config()."
        )

    if isinstance(cfg.start_keyword, str) and cfg.start_keyword:
        return KeywordDetector(cfg.start_keyword)

    if isinstance(cfg.start_regex, str) and cfg.start_regex:
        return RegexDetector(cfg.start_regex)

    raise InvalidConfigError(
        "SegmentConfig must define a non-empty 'start_keyword' or 'start_regex'."
    )
