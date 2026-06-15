#!/usr/bin/env python3
"""Skill ↔ Framework derivation lint (FN-004).

The `Skills/agentic-coding/` skill is a hand-maintained condensed derivation of
the canonical `Framework/` docs. Each skill reference file declares what it was
derived from via a provenance line, e.g.:

    > Derived from: Framework v0.22, Lifecycle v0.12, Protocol v0.17, Templates v0.15 (2026-06-13)

This lint compares each declared version against the *actual* latest version in
that Framework doc's changelog (the highest `| vX.Y |` row). If a Framework doc
has advanced past what the skill claims to be derived from, the skill is stale
and must be re-derived.

This is a deterministic, zero-false-positive check: it only flags when a
declared provenance version is behind the real changelog tail. It does NOT try
to judge content equivalence.

Usage:
    python3 scripts/check-skill-derivation.py          # check, exit 1 if stale
    python3 scripts/check-skill-derivation.py --quiet   # only print on drift

Exit codes: 0 = in sync, 1 = drift detected, 2 = lint error (missing files etc.)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Repo root = parent of this script's directory (scripts/..).
REPO = Path(__file__).resolve().parent.parent
FRAMEWORK_DIR = REPO / "Framework"

# Skill reference files that carry a "Derived from:" provenance line.
SKILL_FILES = [
    REPO / "Skills" / "agentic-coding" / "references" / "workflow.md",
    REPO / "Skills" / "agentic-coding" / "references" / "templates.md",
]

# Provenance doc name -> Framework file that owns the changelog.
DOC_FILES = {
    "Framework": FRAMEWORK_DIR / "Framework.md",
    "Lifecycle": FRAMEWORK_DIR / "Lifecycle.md",
    "Protocol": FRAMEWORK_DIR / "Protocol.md",
    "Templates": FRAMEWORK_DIR / "Templates.md",
}

PROVENANCE_RE = re.compile(r"Derived from:\s*(.+)")
PAIR_RE = re.compile(r"([A-Za-z][A-Za-z-]*)\s+v(\d+)\.(\d+)")
CHANGELOG_ROW_RE = re.compile(r"^\|\s*v(\d+)\.(\d+)\s*\|")


def latest_changelog_version(doc_path: Path) -> tuple[int, int] | None:
    """Return the highest (major, minor) found in `| vX.Y |` changelog rows."""
    if not doc_path.exists():
        return None
    versions = []
    for line in doc_path.read_text(encoding="utf-8").splitlines():
        m = CHANGELOG_ROW_RE.match(line.strip())
        if m:
            versions.append((int(m.group(1)), int(m.group(2))))
    return max(versions) if versions else None


def parse_provenance(skill_path: Path) -> list[tuple[str, int, int]]:
    """Extract (doc, major, minor) pairs from the skill file's provenance line."""
    text = skill_path.read_text(encoding="utf-8")
    m = PROVENANCE_RE.search(text)
    if not m:
        return []
    return [
        (doc, int(maj), int(minr))
        for doc, maj, minr in PAIR_RE.findall(m.group(1))
    ]


def fmt(v: tuple[int, int]) -> str:
    return f"v{v[0]}.{v[1]}"


def main(argv: list[str]) -> int:
    quiet = "--quiet" in argv
    drift: list[str] = []
    errors: list[str] = []
    checked = 0

    for skill_path in SKILL_FILES:
        if not skill_path.exists():
            errors.append(f"missing skill file: {skill_path.relative_to(REPO)}")
            continue
        pairs = parse_provenance(skill_path)
        if not pairs:
            errors.append(
                f"no 'Derived from:' provenance line in "
                f"{skill_path.relative_to(REPO)}"
            )
            continue
        for doc, maj, minr in pairs:
            declared = (maj, minr)
            doc_path = DOC_FILES.get(doc)
            if doc_path is None:
                errors.append(
                    f"{skill_path.name}: unknown doc '{doc}' in provenance "
                    f"(no changelog mapping)"
                )
                continue
            actual = latest_changelog_version(doc_path)
            if actual is None:
                errors.append(f"no changelog rows found in {doc}.md")
                continue
            checked += 1
            if actual > declared:
                drift.append(
                    f"  {skill_path.name}: declares {doc} {fmt(declared)} "
                    f"but {doc}.md is at {fmt(actual)} — re-derive the skill"
                )
            elif declared > actual:
                # Skill claims a newer version than the doc has — also a mistake.
                drift.append(
                    f"  {skill_path.name}: declares {doc} {fmt(declared)} "
                    f"which is AHEAD of {doc}.md ({fmt(actual)}) — fix provenance"
                )

    if errors:
        print("skill-derivation lint: ERROR", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 2

    if drift:
        print("skill-derivation lint: DRIFT — the skill is out of sync with Framework/")
        for d in drift:
            print(d)
        print(
            "\nFix: re-derive the affected Skills/agentic-coding/ files and "
            "update their 'Derived from:' line. (FN-004)"
        )
        return 1

    if not quiet:
        print(f"skill-derivation lint: OK — {checked} provenance versions in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
