#!/usr/bin/env python3
"""Check Git-tracked paths and text against the public release boundary.

The checker intentionally obtains its candidate list from Git and reads only tracked
text files. It never searches untracked directories, loads research data, downloads
resources, or writes files.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

PATH_SEGMENTS = {
    "data",
    "results",
    "outputs",
    "figures",
    "downloads",
    "archive",
    "archives",
    "external",
    "external_docs",
    "source_material",
    "notebooks",
    "logs",
}
TEXT_SUFFIXES = {".cfg", ".ini", ".json", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}
TEXT_RULES = (
    ("direct web reference", re.compile(r"https?:" + r"//", re.IGNORECASE)),
    ("identifier-style source reference", re.compile(r"\bd" + r"oi\s*:", re.IGNORECASE)),
    ("email address", re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")),
    (
        "known external-source identifier",
        re.compile(r"\b(?:Cos" + "ta|Dry" + "ad|Zen" + "odo)\b", re.IGNORECASE),
    ),
)


def tracked_paths(root: Path) -> list[PurePosixPath]:
    """Return Git-tracked relative paths for the supplied repository root.

    Args:
        root: Directory in which Git should enumerate tracked paths.

    Returns:
        Git-tracked paths expressed with POSIX separators.

    Raises:
        RuntimeError: If Git cannot enumerate tracked paths for ``root``.
    """
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(detail or "Git could not enumerate tracked paths")
    return [
        PurePosixPath(item.decode("utf-8", errors="surrogateescape"))
        for item in completed.stdout.split(b"\0")
        if item
    ]


def path_violations(path: PurePosixPath) -> list[str]:
    """Return release-boundary violations detectable from one tracked path.

    Args:
        path: Git-tracked relative path to evaluate.

    Returns:
        Human-readable violation messages, or an empty list when the path is allowed.
    """
    violations: list[str] = []
    if path.is_absolute() or ".." in path.parts:
        violations.append("path is not a safe relative path")
    if any(part.lower() in PATH_SEGMENTS for part in path.parts):
        violations.append("path is in an excluded material directory")
    if path.suffix.lower() == ".ipynb":
        violations.append("notebook file is excluded")
    if path.suffix.lower() == ".log" or path.name.lower() == "access.log":
        violations.append("log or access record is excluded")
    return violations


def text_violations(path: PurePosixPath, root: Path) -> list[str]:
    """Return prohibited-text violations for one tracked text file.

    Args:
        path: Git-tracked relative path to inspect.
        root: Repository root containing ``path``.

    Returns:
        Human-readable violation messages, or an empty list for allowed text.
    """
    if path == PurePosixPath("docs/INTRODUCTION.md"):
        return []
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return []
    content = (root / path).read_text(encoding="utf-8", errors="replace")
    return [label for label, pattern in TEXT_RULES if pattern.search(content)]


def main() -> int:
    """Run the tracked-file release-boundary check.

    Returns:
        Process exit status: zero when no violations are found, otherwise nonzero.
    """
    root = Path(__file__).resolve().parents[1]
    try:
        paths = tracked_paths(root)
    except RuntimeError as error:
        print(f"Cannot perform a tracked-file-only check: {error}", file=sys.stderr)
        return 2

    violations: list[str] = []
    for path in paths:
        for message in path_violations(path):
            violations.append(f"{path}: {message}")
        for message in text_violations(path, root):
            violations.append(f"{path}: {message}")
    if violations:
        print("Release-boundary violations:", file=sys.stderr)
        print("\n".join(f"- {item}" for item in violations), file=sys.stderr)
        return 1
    print(f"Release boundary passed for {len(paths)} tracked paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
