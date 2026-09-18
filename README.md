# Aplysia Temporal Credit Assignment

This independent research repository contains **data-free Python utilities** for exploring temporal credit-assignment methods in an *Aplysia*-inspired setting. It is a scoped methods workspace, not a record of empirical outcomes. It contains no research data, generated outputs, figures, external source material, or claims about biological or experimental findings.

## Current status

**Public staging:** the repository currently provides a small, deterministic utility layer and synthetic tests. The retained code is suitable for method development and review with synthetic inputs only. No dataset-specific workflow, numerical result, or external-source claim is included. This status note supersedes any earlier outcome-oriented descriptions that may remain in historical version control.

## Contents

| Path | Contents |
|---|---|
| `src/preprocessing.py` | Array-based spike-time conversion and Gaussian smoothing utilities. |
| `src/factorization.py` | Deterministic matrix preprocessing and component-timing helper functions. |
| `tests/` | Synthetic, data-free tests for retained utilities. |
| `tools/check_release_boundary.py` | Tracked-text and tracked-path release-boundary scanner. |
| `docs/` | Scope, release-boundary, status, and contribution guidance. |

## Use and validation

Install the Python requirements in an isolated environment, then run:

```bash
python -m pytest -q
python tools/check_release_boundary.py
```

The scanner reads tracked files and their text only. It does not inspect, load, download, create, or modify research data or output directories.

## Keywords

*Aplysia*, temporal credit assignment, neural time series, non-negative matrix factorization, preprocessing, reproducible methods, synthetic testing.

## Contributing

Contributions are welcome, especially focused improvements to data-free methods, synthetic tests, documentation, and release-boundary safeguards. Please read [Contributing](CONTRIBUTING.md) and the [public documentation](docs/STATUS_AND_PLAN.md) before opening a change.

## Documentation

- [Status and plan](docs/STATUS_AND_PLAN.md)
- [Methods scope](docs/METHODS_SCOPE.md)
- [Release boundary](docs/RELEASE_BOUNDARY.md)
- [Deferred and dropped directions](docs/DEFERRED_AND_DROPPED_DIRECTIONS.md)
