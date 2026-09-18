# Release Boundary

## Purpose

This public repository preserves data-free methods and a concise, qualitative research-status record. The status record reports the completed re-analysis direction and its limitations without distributing research artifacts or numerical outputs.

## Included material

The public tree may contain data-free source code, synthetic tests, plain-language methods documentation, contribution guidance, release-boundary tooling, and a qualitative account of completed research work. Any public outcome statement must be pre-specified in scope, free of numerical values and source-specific operational details, and paired with its material limitations.

## Excluded material

The public tree must exclude raw or derived data, numerical results, pair-level or participant-level results, figures and figure specifications, downloads, archives, external source material and metadata, internal indexes, access logs, notebooks, and caches. It also excludes unsupported causal, mechanistic, exact-replication, or readiness assertions and personal contact details.

## Automated check

`tools/check_release_boundary.py` obtains the Git-tracked file list, then evaluates only those paths and text files. It does not traverse untracked directories, load data, download material, or write files. The check is intended as a conservative guard, not as a substitute for human review.
