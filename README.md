# Record Segmentation

[![CI](https://github.com/DreamyStranger/record-segmentation/actions/workflows/ci.yml/badge.svg)](https://github.com/DreamyStranger/record-segmentation/actions/workflows/ci.yml)
[![Python Versions](https://img.shields.io/pypi/pyversions/record-segmentation.svg)](https://pypi.org/project/record-segmentation/)
[![License](https://img.shields.io/github/license/DreamyStranger/record-segmentation.svg)](LICENSE)
![Tests](https://img.shields.io/badge/tests-pytest-blue)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)]()

**Streaming record-boundary detection and segmentation for line-oriented text.**

`record-segmentation` is a small, fast Python library for splitting line-oriented streams such as logs, dumps, and event feeds into logical records based on configurable boundary detection.

It is designed for:

- streaming workloads
- large log processing
- record-oriented parsing pipelines
- constant-memory segmentation

---

## Features

- Streaming segmentation for any iterable of lines
- Multiple boundary detection strategies
- Constant memory usage
- Pure Python with no runtime dependencies
- Fully typed (`mypy --strict`)
- Comprehensive unit and integration tests
- Simple API focused on composability

---

## Installation

```bash
pip install record-segmentation
```

For development:

```bash
pip install -e .[dev]
```

---

## Quick Example

Suppose you have a log where each record begins with `START`:

```
START request
line a
line b
START request
line c
line d
```

You can segment it like this:

```python
from record_segmentation import KeywordDetector, split_segments

detector = KeywordDetector("START")

with open("log.txt") as f:
    for segment in split_segments(f, detector):
        print(segment)
```

Output:

```
["START request\n", "line a\n", "line b\n"]
["START request\n", "line c\n", "line d\n"]
```

Segments are emitted as soon as they are detected, allowing the library to operate efficiently on very large inputs.

---

## Core API

The main public entrypoints are:

- `KeywordDetector`
- `RegexDetector`
- `PredicateDetector`
- `SegmentConfig`
- `build_detector`
- `split_segments`

---

## Detectors

### KeywordDetector

Fast substring-based detection.

```python
from record_segmentation import KeywordDetector

detector = KeywordDetector("START")
```

### RegexDetector

Pattern-based detection for more flexible boundaries.

```python
from record_segmentation import RegexDetector

detector = RegexDetector(r"^\d{4}-\d{2}-\d{2}")
```

### PredicateDetector

Custom detection logic for advanced use cases.

```python
from record_segmentation import PredicateDetector

detector = PredicateDetector(lambda line: line.startswith("BEGIN"))
```

---

## Streaming Design

`split_segments()` accepts any iterable of lines:

- file objects
- generators
- iterators
- sockets
- streaming pipelines

Example with a generator:

```python
from record_segmentation import KeywordDetector, split_segments

def stream():
    yield "START a\n"
    yield "x\n"
    yield "START b\n"
    yield "y\n"

for segment in split_segments(stream(), KeywordDetector("START")):
    process(segment)
```

Memory usage stays bounded because the library only keeps the current segment in memory.

---

## Configuration Builder

You can also construct detectors from configuration mappings:

```python
from record_segmentation import build_detector

detector = build_detector({
    "start_keyword": "START",
})
```

Or from a `SegmentConfig`:

```python
from record_segmentation import SegmentConfig, build_detector

cfg = SegmentConfig(start_regex=r"^\d{4}-\d{2}-\d{2}")
detector = build_detector(cfg)
```

---

## Typical Usage in a Real Project

A common usage pattern is:

```python
from record_segmentation import RegexDetector, split_segments

detector = RegexDetector(r"^\d{4}-\d{2}-\d{2}")

with open("application.log") as f:
    for segment in split_segments(f, detector):
        record = parse_segment(segment)
        handle_record(record)
```

This keeps segmentation logic separate from parsing logic, which makes larger pipelines easier to test and maintain.

---

## Performance

The library is designed to keep the hot path small and predictable.

Run the benchmark locally:

```bash
python scripts/benchmark.py
```

Run a stress-style benchmark:

```bash
python scripts/benchmark.py --segments 10000000 --payload-lines 0 --detector keyword
```

Example synthetic benchmark results:

| Detector | Lines/sec |
|----------|-----------|
| PredicateDetector (`startswith`) | ~2.0M |
| KeywordDetector | ~1.9M |
| RegexDetector | ~1.3M |

Actual performance depends on:

- Python version
- hardware
- detector strategy
- input shape
- match frequency

---

## Development

Create a virtual environment and install development dependencies.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

Run checks:

```bash
ruff check .
mypy src
pytest --cov=record_segmentation --cov-report=term-missing
```

---

## Project Structure

```
record-segmentation/
├── src/record_segmentation/
│   ├── config/
│   ├── detectors/
│   ├── models/
│   ├── splitters/
│   ├── builders.py
│   ├── errors.py
│   └── types.py
├── tests/
│   ├── unit/
│   └── integration/
├── scripts/
│   └── benchmark.py
├── CHANGELOG.md
├── LICENSE
├── MANIFEST.in
└── pyproject.toml
```

---

## Use Cases

This library is useful in projects that need to segment line-oriented input into logical records, including:

- log processing pipelines
- ETL ingestion flows
- streaming event processing
- parser front-ends
- preprocessing semi-structured text dumps

---

## Status

The project currently focuses on **start-boundary segmentation**:

- a new segment begins when a line matches the configured detector
- the previous segment ends immediately before that line
- the final segment is emitted at end-of-input

This keeps the model simple, streaming-friendly, and well-suited to many real log and record-processing tasks.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

---

## License

MIT License. See [LICENSE](LICENSE).