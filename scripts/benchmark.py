"""
scripts.benchmark
===============================================================================

Benchmark utilities for record segmentation.

Overview
--------
This script benchmarks the core segmentation pipeline:

    detector -> split_segments

It generates synthetic line streams and measures how quickly the library can
detect record starts and emit segments.

Supported detector modes
------------------------
- keyword
- regex
- predicate
- all

Examples
--------
Run the default comparison benchmark:

    python scripts/benchmark.py

Run a larger stress-style benchmark for keyword detection only:

    python scripts/benchmark.py --segments 10000000 --payload-lines 0 --detector keyword

Run all detectors on a custom workload:

    python scripts/benchmark.py --segments 500000 --payload-lines 10 --detector all

Design notes
------------
- The benchmark is fully streaming and does not accumulate segments in memory.
- Results are intended for relative comparison, not rigorous scientific
  benchmarking.
- For serious benchmarking, run multiple times and compare medians.
"""

from __future__ import annotations

import argparse
import time
from collections.abc import Iterator
from typing import Any

from record_segmentation import (
    KeywordDetector,
    PredicateDetector,
    RegexDetector,
    split_segments,
)


# ============================================================================
# Synthetic stream generation
# ============================================================================


def generate_stream(
    segment_count: int,
    payload_lines_per_segment: int,
) -> Iterator[str]:
    """
    Generate a synthetic streaming log.

    Each segment begins with a START line followed by payload lines.

    Args:
        segment_count:
            Number of segments to generate.
        payload_lines_per_segment:
            Number of payload lines per segment.

    Yields:
        Synthetic log lines suitable for segmentation benchmarks.
    """
    for i in range(segment_count):
        yield f"START segment-{i}\n"

        for j in range(payload_lines_per_segment):
            yield f"payload {i}:{j}\n"


# ============================================================================
# Benchmark execution
# ============================================================================


def run_benchmark(
    name: str,
    detector: Any,
    segment_count: int,
    payload_lines: int,
) -> None:
    """
    Run a benchmark for one detector.

    Args:
        name:
            Human-readable detector name.
        detector:
            Detector instance used by `split_segments`.
        segment_count:
            Number of synthetic segments to generate.
        payload_lines:
            Number of payload lines per segment.
    """
    stream = generate_stream(segment_count, payload_lines)

    start = time.perf_counter()

    segments = 0
    for _ in split_segments(stream, detector):
        segments += 1

    elapsed = time.perf_counter() - start
    total_lines = segment_count * (payload_lines + 1)

    print(name)
    print("-" * len(name))
    print(f"Segments detected : {segments}")
    print(f"Total lines       : {total_lines}")
    print(f"Elapsed time      : {elapsed:.4f}s")
    print(f"Lines/sec         : {total_lines / elapsed:,.0f}")
    print(f"Segments/sec      : {segments / elapsed:,.0f}")
    print()


def get_detectors(detector_name: str) -> list[tuple[str, Any]]:
    """
    Return the configured detector set for benchmarking.

    Args:
        detector_name:
            One of: keyword, regex, predicate, all

    Returns:
        A list of `(display_name, detector_instance)` pairs.
    """
    detectors: dict[str, tuple[str, Any]] = {
        "keyword": ("KeywordDetector", KeywordDetector("START")),
        "regex": ("RegexDetector", RegexDetector(r"^START")),
        "predicate": (
            "PredicateDetector",
            PredicateDetector(lambda line: line.startswith("START")),
        ),
    }

    if detector_name == "all":
        return [
            detectors["keyword"],
            detectors["regex"],
            detectors["predicate"],
        ]

    return [detectors[detector_name]]


# ============================================================================
# CLI
# ============================================================================


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the benchmark script.
    """
    parser = argparse.ArgumentParser(
        description="Benchmark record segmentation detectors."
    )

    parser.add_argument(
        "--segments",
        type=int,
        default=100_000,
        help="Number of segments to generate (default: 100000).",
    )

    parser.add_argument(
        "--payload-lines",
        type=int,
        default=5,
        help="Number of payload lines per segment (default: 5).",
    )

    parser.add_argument(
        "--detector",
        choices=["keyword", "regex", "predicate", "all"],
        default="all",
        help="Detector to benchmark (default: all).",
    )

    return parser.parse_args()


# ============================================================================
# Main entrypoint
# ============================================================================


def main() -> None:
    """
    Run the requested segmentation benchmark workload.
    """
    args = parse_args()

    print("\nRecord Segmentation Benchmark")
    print("=" * 40)
    print(f"Segments       : {args.segments:,}")
    print(f"Payload/segment: {args.payload_lines}")
    print(f"Detector mode  : {args.detector}")
    print()

    for name, detector in get_detectors(args.detector):
        run_benchmark(
            name=name,
            detector=detector,
            segment_count=args.segments,
            payload_lines=args.payload_lines,
        )


if __name__ == "__main__":
    main()