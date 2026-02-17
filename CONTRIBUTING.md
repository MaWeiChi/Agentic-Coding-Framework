# Contributing to Agentic Coding Framework

Thank you for your interest in contributing! This document explains how to participate.

## Reporting Issues

Open a GitHub Issue with:

- **What happened** — describe the problem or unexpected behavior
- **What you expected** — the behavior you anticipated
- **Context** — which document(s) are involved, your tool (Claude Code, Cursor, Windsurf, etc.), and whether you were using Full or Lite mode

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-change`)
3. Make your changes following the conventions below
4. Open a Pull Request with a clear description of what changed and why

## Writing Conventions

- **RFC 2119 keywords**: Use MUST, SHOULD, MAY (uppercase) with their standard meanings when writing normative statements in framework documents
- **Changelog entries**: Every Framework document has a Changelog section at the bottom. Add a new row when making substantive changes
- **Version bumping**: Increment the minor version (e.g., v0.9 → v0.10) for each release-worthy change. The README version table should match
- **Language**: All framework documents and commit messages are in English
- **Formatting**: Use Markdown. Keep lines under 120 characters where practical. Use tables for structured comparisons

## Document Structure

- `Framework/` — Core framework documents (concepts, lifecycle, templates, protocol)
- `Skills/` — Tool-specific skill packages that agents load directly
- `Skills/agentic-coding/references/` — Condensed versions of framework docs optimized for agent token budgets. These include a `Derived from:` header indicating which framework version they were generated from

## Skill Reference Sync

The files in `Skills/agentic-coding/references/` are condensed copies of framework content. When updating framework documents, check if the corresponding reference file also needs updating. The `Derived from:` header in each reference file indicates the source version.

## Field Feedback

If you have used the framework on a real project and want to share observations, open an Issue tagged `field-feedback`. Include:

- Project type and approximate size (number of stories completed)
- Mode used (Full / Lite)
- What worked well and what didn't
- Specific suggestions with rationale

Field feedback is tracked in `Framework/Refinement.md` and may be incorporated into future versions.

## Code of Conduct

Be respectful and constructive. This is a documentation-heavy project — clarity and precision matter more than volume.
