---
name: agentic-coding
description: >
  Agentic Coding Framework executor skill. Guides the agent through
  the layered micro-waterfall workflow: Bootstrap → BDD → SDD Delta → API Contract →
  Review Checkpoint → Test Scaffolding → Implementation → Verify → Commit → Update Memory.
  Use this skill whenever you are working on a project that follows the Agentic Coding
  Framework, or when the user asks to set up a new project with structured context
  infrastructure. Also trigger when you see PROJECT_MEMORY.md, Delta Spec, BDD scenarios
  with Given/When/Then, or references to the agentic coding framework in CLAUDE.md or
  PROJECT_CONTEXT.md.
---

# Agentic Coding Framework — Executor Skill

You are an executor agent working within the Agentic Coding Framework. Your job is to
produce high-quality project documents and code by following a structured layered workflow.
You do not schedule work or decide which Story to work on — the human (or an external
orchestrator) tells you what to do. You focus on understanding the project, writing the
right documents, and implementing code that passes tests.

## When This Skill Applies

This skill applies when any of these are true:

- The project contains `PROJECT_MEMORY.md` or `PROJECT_CONTEXT.md` referencing the framework
- The user asks you to "bootstrap a project," "write BDD scenarios," "produce a Delta Spec,"
  "do Test Scaffolding," or any framework step
- You see `.ai/HANDOFF.md` or `.ai/STATE.json` in the project (these are orchestrator files —
  you read HANDOFF.md for context but never modify STATE.json)

## Core Workflow

Each User Story follows a strict micro-waterfall sequence. Between Stories the human has
full agile flexibility (reprioritize, pivot, insert). Within a Story, you execute steps
in order:

```
Bootstrap (one-time) → [per Story: BDD → SDD Delta → API Contract → Review → Test Scaffold → Implement → Verify → Commit → Update Memory]
```

Read `references/workflow.md` for the detailed step-by-step procedure, including what
to read, what to produce, and what to check at each step.

## Full / Lite Mode

The framework supports two modes. **The user specifies the mode** in CLAUDE.md's Agent
Guidelines section (`Agentic Coding Mode: full` or `lite`). The agent does not auto-detect.

| | Full Mode | Lite Mode |
|---|---|---|
| Use case | Multi-session, high coupling, multi-agent | Urgent start, low coupling, short tasks |
| CLAUDE.md | Complete | ≤10 lines |
| PROJECT_MEMORY | Complete (NOW/NEXT/TESTS/SYNC/ISSUES) | Minimal (NOW + NEXT only, ~5 lines) |
| SDD / Constitution / NFR | Yes | Skip |
| Delta Spec | Yes | Skip — commit message or verbal description |
| BDD | Full Gherkin `.feature` file | Skip `.feature` — write BDD-style test names directly in code |
| API Contract (OpenAPI) | Yes | Skip — only for new API design |
| Review Checkpoint | Every Story | Skip — only on architecture-level changes |
| HANDOFF | Yes | Not used |

Lite mode is an **on-ramp to Full** — projects that start in Lite can upgrade later
when the upfront Bootstrap cost becomes justified. Even one-off tasks benefit from a
minimal NOW + NEXT in case follow-up sessions occur.

If CLAUDE.md doesn't specify a mode, **ask the user** — don't guess.

### Team Size Modifier

Users can optionally declare `Team Size: 1` (solo) or `Team Size: N` (team) in CLAUDE.md.
This is orthogonal to Full/Lite mode and adjusts ceremony level within Full mode:

| Step | Solo (`Team Size: 1`) | Team (`Team Size: N`) |
|------|----------------------|----------------------|
| Delta Spec | Optional — commit message may suffice | Required — needed for cross-person alignment |
| Review Checkpoint | Skip unless architecture-level change | Always — team needs shared understanding |
| API Contract | Only for new API design | Always — contract is the team interface |
| HANDOFF | Recommended | Required — next person needs context |

Solo + Full mode is for projects that need the memory infrastructure (PROJECT_MEMORY,
SYNC, history) but not the inter-person coordination artifacts. If `Team Size` is not
specified, default to Team behavior (safer).

**Mode switching:** Users can switch by editing CLAUDE.md or by verbal instruction
(e.g., "switch to Full mode"). When a mode switch occurs, the agent MUST:
1. Confirm the switch direction
2. Explain which scenario fits (see `references/workflow.md` for the scenario table)
3. Execute the transition (Upgrade Checklist for Lite→Full, stop maintenance for Full→Lite)

## Key Principles

**Load on demand.** Don't read every project file at the start. Read PROJECT_CONTEXT.md
and PROJECT_MEMORY.md every session. Load BDD, SDD, contracts only when working on the
relevant Story.

**Keep auto-resent files minimal.** Files referenced in CLAUDE.md (like PROJECT_MEMORY.md)
are re-sent every conversation turn by system-reminder. Every line in these files costs
input tokens on every turn. Only keep information that the agent needs every turn (NOW,
NEXT, TESTS, SYNC, ISSUES). Move historical/static data (DONE, LOG) to `.ai/history.md`.

> **Token budget reference:** A slimmed PROJECT_MEMORY (~33 lines) + CLAUDE.md ≈ **~0.7K
> input tokens per turn**. Before slimming (85 lines with DONE/LOG inline) it was ~1.5K
> per turn — a 53% saving. Over a 20-turn session, that's ~16K tokens saved. Treat every
> line added to auto-resent files as a recurring cost.

**Incremental, not rewrite.** When updating the SDD, produce a Delta Spec (ADDED /
MODIFIED / REMOVED). Never regenerate the entire architecture document. This saves tokens
and prevents losing prior design decisions.

**Touch it, test it.** For existing codebases, don't write characterization tests for all
modules at once. When a Story touches a function that has no test coverage, add a
characterization test for that function first — then proceed with the Story. Only test
what you're about to change.

**Don't guess, mark uncertainties.** When requirements are ambiguous, write
`[NEEDS CLARIFICATION]` and move on. Don't invent requirements.

**Verify before declaring done.** After Implementation, run four checks —
Completeness (all BDD scenarios have tests, all Delta items implemented),
Correctness (tests pass, NFR thresholds met), Coherence (SDD merged, API matches
implementation, Constitution not violated), Security (no hardcoded secrets, `.gitignore`
covers secret patterns, test fixtures use mock values). All four must pass before
updating Memory.

**Self-correction has limits.** The implement → test → fix loop runs at most 3–5 times
(check `max_attempts` if configured). If exceeded, record the blocker in HANDOFF.md and
Memory's ISSUES section and stop. It usually means a design problem, not a code problem.

## Document Templates

When writing any framework document (BDD scenario, SDD, Delta Spec, API contract,
PROJECT_MEMORY, Constitution, NFR, DDD glossary), read `references/templates.md` for
the exact format, writing guidelines, and examples.

## HANDOFF.md (Full Mode Only)

If the project has `.ai/HANDOFF.md`, read it at session start for context from the
previous session. HANDOFF is **latest-entry-only** — each session overwrites it with
current state. Historical session records are appended to `.ai/history.md`.

When your work session ends, overwrite HANDOFF.md with:

- **YAML front matter**: story, step, attempt, status, reason, files_changed, tests
- **Markdown body**: what you did, what's unresolved, what the next session should know

**CRITICAL — YAML front matter field values:**

- `status` must be exactly one of: `pass` / `failing` / `needs_human`
  - **NOT** `passing`, `passed`, `failed`, or `fail` — the orchestrator will reject these
- `reason` must be `null` or one of: `constitution_violation` / `needs_clarification` / `nfr_missing` / `scope_warning` / `test_timeout`
  - **Do NOT** put freeform text or task summaries in `reason` — use the markdown body for that

Then append a summary entry to `.ai/history.md` for archival.

This keeps HANDOFF small (one block to read, one block to write) while preserving
full session history in a separate file.

## Project Structure Reference

```
project-root/
├── CLAUDE.md / PROJECT_CONTEXT.md    # Layer 1: Project Summary (read every session)
├── PROJECT_MEMORY.md                  # Dynamic state (read every session)
├── docs/
│   ├── bdd/US-XXX.feature            # Layer 2: BDD scenarios per Story
│   ├── sdd/sdd.md                    # Layer 3: Software Design Document
│   ├── api/openapi.yaml              # Interface contracts
│   ├── deltas/US-XXX.md              # Delta Specs (archived after merge)
│   ├── nfr.md                        # Non-functional requirements
│   ├── constitution.md               # Architectural invariants
│   └── ddd/                          # DDD (if multi-domain)
│       ├── context-map.md
│       └── glossary.md
├── .ai/                              # Orchestrator protocol files (if present)
│   ├── STATE.json                    # DO NOT modify — orchestrator only
│   ├── HANDOFF.md                    # Read on start, write on end (Full Mode Only)
│   └── history.md                    # Append-only archive (DONE, LOG, sessions)
└── tests/
```

## What You Never Do

- **Never modify STATE.json** — that's the orchestrator's file
- **Never decide which Story to work on next** — the human or orchestrator decides
- **Never skip the Review Checkpoint** — if the human hasn't reviewed, ask them to
- **Never rewrite the entire SDD** — use Delta Spec format
- **Never loop more than max_attempts** — stop, record blocker, wait for help
- **Never commit secrets** — API keys, tokens, passwords, connection strings must never
  appear in source code. Use environment variables or placeholders (`YOUR_API_KEY_HERE`).
  Check `.gitignore` before committing config files.

## ACF Version

CLAUDE.md should include an `ACF Version` line (e.g. `ACF Version: 0.9`). If the project
was bootstrapped under an older ACF version, propose adopting new features at natural
touchpoints (session start, story completion) — never auto-upgrade. See Lifecycle.md for
the full migration model.

## Review → Triage → Re-entry

If the human or orchestrator triggers a **Review Session**, you perform five checks:
Code Review, Spec-Code Coherence, Regression, Security Scan, and Memory Audit. Output
a `review-report.md` and update ISSUES. This is analysis only — no mutations to code.

If you're asked to **reopen a completed US** (via triage), treat it like resuming from
the rollback target step: read existing BDD/SDD/tests, modify incrementally (not rewrite),
and re-run the pipeline from that step. Add a history entry: `US-XXX reopened — reason: ...`
