"""
record_segmentation.builders
===============================================================================

High-level package construction helpers.

Overview
--------
This module exposes ergonomic builder functions that translate user-facing
configuration into concrete runtime objects.

At present this mainly means turning `SegmentConfig` into a detector instance.
Keeping this entrypoint stable lets the library evolve internally without
forcing users to import lower-level factory modules directly.
"""

from __future__ import annotations

# External package boundaries
from .config import SegmentConfig

# Configuration
# Detector subsystem
from .detectors.base import BaseDetector
from .detectors.factory import build_detector_from_config

# Core errors
from .errors import InvalidConfigError


def build_detector(cfg: SegmentConfig | dict[str, object]) -> BaseDetector:
    """
    Build a concrete detector from configuration.

    Args:
        cfg:
            Either a `SegmentConfig` instance or a mapping containing compatible
            constructor fields for `SegmentConfig`.

    Returns:
        A concrete detector chosen according to library precedence rules.

    Raises:
        InvalidConfigError:
            If `cfg` cannot be normalized or does not define a valid detection
            strategy.
    """
    if isinstance(cfg, dict):
        start_keyword = cfg.get("start_keyword")
        start_regex = cfg.get("start_regex")
        include_preamble = cfg.get("include_preamble", False)
        emit_empty_segments = cfg.get("emit_empty_segments", False)

        if start_keyword is not None and not isinstance(start_keyword, str):
            raise InvalidConfigError("'start_keyword' must be a string or None.")

        if start_regex is not None and not isinstance(start_regex, str):
            raise InvalidConfigError("'start_regex' must be a string or None.")

        if not isinstance(include_preamble, bool):
            raise InvalidConfigError("'include_preamble' must be a bool.")

        if not isinstance(emit_empty_segments, bool):
            raise InvalidConfigError("'emit_empty_segments' must be a bool.")

        cfg = SegmentConfig(
            start_keyword=start_keyword,
            start_regex=start_regex,
            include_preamble=include_preamble,
            emit_empty_segments=emit_empty_segments,
        )

    if not isinstance(cfg, SegmentConfig):
        raise InvalidConfigError(
            "'cfg' must be a SegmentConfig or compatible dict in build_detector()."
        )

    return build_detector_from_config(cfg)
