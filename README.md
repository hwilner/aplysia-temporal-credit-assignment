# Aplysia Temporal Credit Assignment

This independent research repository records a completed deterministic Python re-analysis of temporal credit assignment in *Aplysia* together with the data-free utilities used to make the analysis testable and reviewable.

## Research status

| Completed work | Outcome |
|---|---|
| Deterministic Python non-negative matrix factorization re-analysis | The planned contingent-minus-yoked contrast was directionally negative in most matched pairs and retained that direction in leave-one-pair-out summaries. |
| Planned component-count and smoothing checks | The timing contrast was not precise or stable enough across these choices to support a robust conclusion. |
| Descriptive comparison with an archived reference | Preparation-level directional correspondence was broad, but pair-level correspondence was incomplete and the methods were not identical. |
| Exact reference-workflow execution | Not performed. The project uses a Python route and does not claim an exact rerun or replication. |

**Current conclusion:** the completed re-analysis is **directionally suggestive but inconclusive**. It does not support a strong confirmatory, causal, mechanistic, or exact-replication claim.

## What is included

| Path | Contents |
|---|---|
| `src/preprocessing.py` | Array-based spike-time conversion and Gaussian smoothing utilities. |
| `src/factorization.py` | Deterministic matrix preprocessing and component-timing helper functions. |
| `tests/` | Synthetic tests for retained utilities. |
| `tools/check_release_boundary.py` | Tracked-text and tracked-path release-boundary scanner. |
| `docs/` | Research status, methods scope, deferred directions, and contribution guidance. |

## Use and validation

Install the Python requirements in an isolated environment, then run:

```bash
python -m pytest -q
python tools/check_release_boundary.py
```

The scanner reads tracked files and their text only. It does not inspect, load, download, create, or modify research data or output directories.

## Keywords

*Aplysia*, temporal credit assignment, neural time series, non-negative matrix factorization, reproducible re-analysis, synthetic testing.

## Contributing

Contributions are welcome, especially focused improvements to data-free methods, synthetic tests, documentation, and release-boundary safeguards. Please read [Contributing](CONTRIBUTING.md) and the [research status](docs/STATUS_AND_PLAN.md) before opening a change.

## Documentation

- [Introduction for new readers](docs/INTRODUCTION.md)
- [Research status and plan](docs/STATUS_AND_PLAN.md)
- [Methods scope](docs/METHODS_SCOPE.md)
- [Release boundary](docs/RELEASE_BOUNDARY.md)
- [Deferred and dropped directions](docs/DEFERRED_AND_DROPPED_DIRECTIONS.md)
