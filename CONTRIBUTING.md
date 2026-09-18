# Contributing

Contributions are welcome. This staging repository accepts focused, reviewable changes that improve data-free methods, synthetic tests, documentation, or release-boundary controls.

## Public boundary

Do not add research data, derived tables, figures, downloads, archives, external source material, access logs, notebooks, or cached artifacts. Do not add numerical results, source-specific outcome claims, release-status assertions, personal contact details, or external metadata.

## Code and tests

Keep retained utilities deterministic where practical and independent of repository data or output paths. Public callables should use Google-style docstrings and concise comments where they clarify a non-obvious implementation choice. Add or update synthetic tests for behavior changes; tests must not read local data or write into repository data, result, figure, or output paths.

## Documentation and review

Keep documentation conservative and methods-focused. Describe current scope and limitations rather than empirical conclusions. Before proposing a change, review [Methods scope](docs/METHODS_SCOPE.md), [Release boundary](docs/RELEASE_BOUNDARY.md), and [Status and plan](docs/STATUS_AND_PLAN.md). Run the documented validation commands and report any limitations of the change.
