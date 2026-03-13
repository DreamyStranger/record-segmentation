"""
Streaming splitters for record segmentation.
"""

from .policies import PreamblePolicy
from .split import split_segments

__all__ = ["PreamblePolicy", "split_segments"]
