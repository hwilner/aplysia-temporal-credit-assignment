# Contributing

Contributions are welcome. This staging repository accepts focused, reviewable changes that improve data-free methods, synthetic tests, documentation, or release-boundary controls.

## Public boundary

Do not add research data, derived tables, figures, downloads, archives, external source material, access logs, notebooks, or cached artifacts. Do not add numerical results, source-specific outcome claims, release-status assertions, personal contact details, or external metadata.

## Code and tests

Keep retained utilities deterministic where practical and independent of repository data or output paths. Public callables should use Google-style docstrings and concise comments where they clarify a non-obvious implementation choice. Add or update synthetic tests for behavior changes; tests must not read local data or write into repository data, result, figure, or output paths.

## Documentation and review

Keep documentation conservative and methods-focused. Describe current scope and limitations rather than empirical conclusions. Before proposing a change, review [Methods scope](docs/METHODS_SCOPE.md), [Release boundary](docs/RELEASE_BOUNDARY.md), and [Status and plan](docs/STATUS_AND_PLAN.md). Run the documented validation commands and report any limitations of the change.

## Future Testing Opportunities

The opportunities below preserve the public boundary. They do not authorize the addition of research data, derived outputs, external material, infrastructure, runtime code, a test suite, or release-control changes in this staging repository.

### Data-free software or documentation tests contributors can work on now

- **Interface-to-documentation check:** Review the retained array utilities against their docstrings and methods documentation. Report an ambiguity about inputs, indexing, shapes, or deterministic behavior, or propose a prose-only clarification; do not change runtime code or tests.
- **Scope-language check:** Read the status, methods, and release-boundary documents together and flag wording that could blur the distinction between synthetic behavior checks and empirical evidence. A documentation-only correction is welcome when it keeps that distinction clear.
- **Synthetic edge-case test design review:** Describe, in an issue or pull-request discussion, a small in-memory edge case that a future approved synthetic test should cover, along with its expected behavior. Keep the proposal data-free and do not add a test, output, or new testing tool in this staging change.
- **Boundary tabletop review:** Evaluate a hypothetical documentation or utility change against the public-boundary rules and identify which wording or artifact would create a release risk. Submit the recommendation as review feedback without adding source material or modifying the scanner.

### Research-facing tests requiring maintainer approval and an appropriate data boundary

- **Pre-specified timing evaluation:** With maintainer approval and appropriately governed data outside this public tree, test whether the matched timing contrast retains its direction under analysis choices fixed before outcomes are reviewed.
- **Robustness evaluation:** Under the same approved boundary, test whether planned component-complexity and smoothing choices lead to a stable interpretation, while reporting every planned check rather than selecting a favorable setting afterward.
- **Reference-workflow comparison:** If maintainers approve the required access and method documentation, assess whether an independently documented run of the reference MATLAB/seqNMF workflow gives a compatible qualitative result. This is a prospective comparison, not a claim that it has already occurred.
- **Component-correspondence evaluation:** With an approved research plan and data boundary, test whether components fitted separately can be matched using a rule defined before review, rather than assuming that selected components are identical.

Research-facing proposals must state the question, authorized data boundary, analysis plan, selection rules, planned checks, reporting plan, and release treatment before any research work begins. Maintainer approval is required before proceeding.
