# Release Boundary

## Purpose

This repository is a public-safe, data-free methods staging tree. Its boundary is designed to make the retained code and documentation understandable without providing research records, downloaded material, or empirical outputs.

## Included material

The public tree may contain data-free source code, synthetic tests, plain-language methods documentation, contribution guidance, and release-boundary tooling. Retained code must operate on caller-provided arrays and must not assume repository-local data or output paths.

## Excluded material

The public tree must exclude raw or derived data, numerical results, figures and figure specifications, downloads, archives, external source material and metadata, internal indexes, access logs, notebooks, and caches. It also excludes source-specific outcome assertions, readiness assertions, and personal contact details.

## Automated check

`tools/check_release_boundary.py` obtains the Git-tracked file list, then evaluates only those paths and text files. It does not traverse untracked directories, load data, download material, or write files. The check is intended as a conservative guard, not as a substitute for human review.
