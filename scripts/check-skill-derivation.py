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

# --- FB-019 extensions ---------------------------------------------------

# README "Versions" table rows: `| Framework | v0.23 | 2026-06-13 |`
README_PATH_DEFAULT = "README.md"
README_ROW_RE = re.compile(r"^\|\s*([A-Za-z][A-Za-z-]*)\s*\|\s*v(\d+)\.(\d+)\s*\|")
# Docs the README table tracks that carry their own changelog.
README_TRACKED = {"Framework", "Lifecycle", "Templates", "Protocol", "Refinement"}

# Stale-phrase tripwire: phrases that were removed by contract repairs and
# must never reappear in normative text. Refinement.md (history ledger) and
# changelog rows (`| vX.Y |`) are excluded from the scan.
STALE_PHRASES = [
    "## Delta:",          # pre-FB-012 delta heading (breaks section-name merge)
    "docs/sdd/sdd.md",    # pre-FB-019 SDD path (canonical is docs/sdd.md)
    "Triple verification",
    "triple check",
    "triple-check",
]
SCAN_GLOBS = ["Framework/*.md", "Skills/**/*.md", "README.md", "CONTRIBUTING.md"]


def check_readme_versions(drift: list[str], errors: list[str]) -> int:
    """Compare README's Versions table against each doc's changelog tail."""
    readme = REPO / README_PATH_DEFAULT
    if not readme.exists():
        errors.append("README.md not found")
        return 0
    checked = 0
    for line in readme.read_text(encoding="utf-8").splitlines():
        m = README_ROW_RE.match(line.strip())
        if not m:
            continue
        doc, maj, minr = m.group(1), int(m.group(2)), int(m.group(3))
        if doc not in README_TRACKED:
            continue
        doc_path = REPO / "Framework" / f"{doc}.md"
        actual = latest_changelog_version(doc_path)
        if actual is None:
            errors.append(f"no changelog rows found in Framework/{doc}.md")
            continue
        checked += 1
        declared = (maj, minr)
        if actual != declared:
            drift.append(
                f"  README.md Versions table: {doc} listed as {fmt(declared)} "
                f"but Framework/{doc}.md changelog is at {fmt(actual)}"
            )
    return checked


def check_stale_phrases(drift: list[str]) -> int:
    """Grep normative docs for phrases retired by contract repairs (FB-019)."""
    checked = 0
    seen: set[Path] = set()
    for pattern in SCAN_GLOBS:
        for path in sorted(REPO.glob(pattern)):
            if path in seen or path.name == "Refinement.md":
                continue
            seen.add(path)
            checked += 1
            for lineno, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if CHANGELOG_ROW_RE.match(line.strip()):
                    continue  # changelog rows may quote history
                for phrase in STALE_PHRASES:
                    if phrase.lower() in line.lower():
                        drift.append(
                            f"  {path.relative_to(REPO)}:{lineno}: stale phrase "
                            f"'{phrase}' — retired by FB-019"
                        )
    return checked


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

    readme_checked = check_readme_versions(drift, errors)
    files_scanned = check_stale_phrases(drift)

    if errors:
        print("skill-derivation lint: ERROR", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 2

    if drift:
        print("skill-derivation lint: DRIFT detected")
        for d in drift:
            print(d)
        print(
            "\nFix: re-derive/re-sync the flagged files. Provenance drift → "
            "update the skill + its 'Derived from:' line (FN-004); README "
            "table / stale phrases → align with the current contracts (FB-019)."
        )
        return 1

    if not quiet:
        print(
            f"skill-derivation lint: OK — {checked} provenance versions, "
            f"{readme_checked} README table rows in sync; "
            f"{files_scanned} files free of stale phrases"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
