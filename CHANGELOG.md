# Changelog

All notable changes to this project will be documented in this file.

The format is based on **Keep a Changelog**:
https://keepachangelog.com/en/1.0.0/

This project adheres to **Semantic Versioning**:
https://semver.org/

---

## [0.1.0] - 2026-03-13

### Added

- Initial release of `record-segmentation`
- Streaming record segmentation for line-oriented text
- `KeywordDetector` for fast substring boundary detection
- `RegexDetector` for pattern-based detection
- `PredicateDetector` for custom detection logic
- `split_segments()` streaming segmentation utility
- `SegmentConfig` configuration model
- `build_detector()` configuration builder

### Infrastructure

- Full unit and integration test suite
- test coverage
- Strict `mypy` typing
- `ruff` linting
- GitHub CI workflow
- Benchmark script for segmentation performance