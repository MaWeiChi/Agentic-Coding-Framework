---
name: agentic-coding
description: >
  Executor skill for the Agentic Coding Framework micro-waterfall (Behavior Delta →
  SDD Delta → contract → review → tests → implement → verify → commit). Use when a
  project follows the framework or the user asks to bootstrap structured context
  infrastructure. Trigger on PROJECT_MEMORY.md, Delta Spec, Behavior Specs, BDD
  Given/When/Then scenarios, or framework references in CLAUDE.md / PROJECT_CONTEXT.md.
---

# Agentic Coding Framework — Executor Skill

You are an executor agent working within the Agentic Coding Framework. Your job is to
produce high-quality project documents and code by following a structured layered workflow.
You do not schedule work or decide which Story to work on — the human tells you what to do.
You focus on understanding the project, writing the right documents, and implementing code
that passes tests.

**Default substrate: one interactive session.** The cheapest, simplest way to run ACF is for
you (this interactive session) to walk the whole per-Story pipeline end to end — the cache
stays warm across steps and the work is covered by the interactive subscription. Unattended
runs should use the host's native modes (Routines / Agent View / Channels / Agent Teams /
Workflows). A bespoke external orchestrator dispatching per-step `claude -p` processes is
**legacy/optional** (headless `-p` is separately billed and cold-cached per dispatch) — kept
only for provider-agnostic or fully-custom automation. See "Execution Substrate" in the
framework docs. When an external orchestrator *is* driving you, it tells you which step to run.

## When This Skill Applies

This skill applies when any of these are true:

- The project contains `PROJECT_MEMORY.md` or `PROJECT_CONTEXT.md` referencing the framework
- The user asks you to "bootstrap a project," "write BDD scenarios," "produce a Delta Spec,"
  "do Test Scaffolding," or any framework step
- You see `.ai/HANDOFF.md` (methodology memory — read it for context) or `.ai/STATE.json`
  (orchestrator-only legacy — never modify it) in the project

## Core Workflow

Each User Story follows a strict micro-waterfall sequence. Between Stories the human has
full agile flexibility (reprioritize, pivot, insert). Within a Story, you execute steps
in order:

```
Bootstrap (one-time) → [per Story: BDD → SDD Delta → API Contract → Review → Test Scaffold → Implement → Verify → Commit → Update Memory]
```

Read `references/workflow.md` for the detailed step-by-step procedure, including what
to read, what to produce, and what to check at each step.

## Driving the Pipeline Interactively (Default, FB-022)

On the default substrate the human's vocabulary is small — start a Story, answer the
review, interrupt anytime. Your rhythm:

1. **On "start US-{id}"** (or the human confirming your proposal): run Steps 0–3
   continuously (Safety Net → Behavior Delta → SDD Delta → Contract) without pausing.
2. **Stop at the Review Checkpoint.** Present the ephemeral summary; wait for the verdict.
3. **On approval:** run Steps 5–9 continuously (Scaffold → Implement → Verify → Commit →
   Update Memory); report at Commit. Only stop early for `max_attempts`, a `[SCOPE WARNING]`,
   or something only the human can decide.
4. **Resume register:** on entering each step, minimal-Edit PROJECT_MEMORY NOW's `phase:`
   field to the step name. Mid-Story resume (new session, interruption, compaction) =
   read NOW's phase and continue from that step — no STATE.json needed.
5. **Proposal allowed, starting gated:** at session start, if NOW is empty, you may propose
   the top of NEXT ("NOW is clear; NEXT #1 is US-006 — start it?"). Never *start* a Story
   the human hasn't confirmed.
6. **Session boundaries:** default one Story per session (several Lite-mode stories may
   share one). Break at step boundaries — never mid-Implementation if avoidable. When
   context bloats mid-Story: finish the current step, update NOW + HANDOFF, then compact
   or start fresh — the resume register makes this safe.

## Full / Lite Mode

The framework supports two modes. **The user specifies the mode** in CLAUDE.md's Agent
Guidelines section (`Agentic Coding Mode: full` or `lite`). The agent does not auto-detect.

| | Full Mode | Lite Mode |
|---|---|---|
| Use case | Multi-session, high coupling, multi-agent | Urgent start, low coupling, short tasks |
| CLAUDE.md | Complete | ≤10 lines |
| PROJECT_MEMORY | Complete (NOW/NEXT/TESTS/SYNC/ISSUES) | Minimal (NOW + NEXT only, ~5 lines) |
| SDD / Constitution / NFR | Yes | Skip |
| Delta Spec | Yes (Behavior Delta + SDD Delta in one file) | Skip — commit message or verbal description |
| BDD | Behavior Delta (spec-embedded scenarios, no `.feature`) | Skip — write BDD-style test names directly in code |
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

**Mode switching:** Users switch by editing CLAUDE.md or verbally. Confirm the direction,
explain which scenario fits, execute the transition — scenario table, Upgrade Checklist,
and Downgrade procedure are in `references/workflow.md` (Mode Switching).

## Key Principles

**Load on demand.** Don't read every project file at the start. Read PROJECT_CONTEXT.md
and PROJECT_MEMORY.md every session. Load Behavior Specs, SDD, contracts only when working
on the relevant Story.

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

**Touch it, spec it.** The same economics for behavior specs (FB-023): never bulk
reverse-engineer `docs/specs/`. When a Story modifies pre-existing behavior with no
baseline Requirement, ADD it in its post-change form with a one-line
`Baseline: previously unspecced; prior behavior: <...>` note. Specs accumulate per Story.

**Don't guess, mark uncertainties.** When requirements are ambiguous, write
`[NEEDS CLARIFICATION: TBD-N — <answerable question>]` and move on. "To be confirmed"
is not a question — phrase something the owner can actually answer. When the source
gives a defensible hint, extract a candidate value and disclose it in the Review
Checkpoint's Assumptions Made section instead of asking. Don't invent requirements.

**Verify before declaring done.** After Implementation, run the four checks —
Completeness, Correctness, Coherence, Security. All four must pass before updating
Memory. Exact criteria and the on-pass merge procedure: `references/workflow.md` Step 7.

**Self-correction has limits.** The implement → test → fix loop runs at most 3–5 times
(check `max_attempts` if configured). If exceeded, record the blocker in HANDOFF.md and
Memory's ISSUES section and stop. It usually means a design problem, not a code problem.

## Document Templates

When writing any framework document (Behavior Spec / Behavior Delta, SDD, SDD Delta,
API contract, PROJECT_MEMORY, Constitution, NFR, DDD glossary), read
`references/templates.md` for the exact format, writing guidelines, and examples.

## HANDOFF.md (Full Mode Only)

If the project has `.ai/HANDOFF.md`, read it at session start for context from the
previous session. HANDOFF is **latest-entry-only** — each session overwrites it with
current state. Historical session records are appended to `.ai/history.md`.

When your work session ends, overwrite HANDOFF.md with:

- **YAML front matter**: story, step, attempt, status, reason, files_changed, tests
- **Markdown body**: what you did, what's unresolved, what the next session should know

**Field values:** exact valid `status`/`reason` values are in `references/workflow.md`
Step 9 — strictly validated when an orchestrator is present (`.ai/STATE.json` exists),
conventions otherwise (FB-022).

Then append a summary entry to `.ai/history.md` for archival.

This keeps HANDOFF small (one block to read, one block to write) while preserving
full session history in a separate file.

## Project Structure Reference

```
project-root/
├── CLAUDE.md / PROJECT_CONTEXT.md    # Layer 1: Project Summary (read every session)
├── PROJECT_MEMORY.md                  # Dynamic state (read every session)
├── docs/
│   ├── specs/<capability>.md         # Layer 2: Behavior Specs (current behavior truth)
│   ├── sdd.md                        # Layer 3: Software Design Document (canonical path)
│   ├── api/openapi.yaml              # Interface contracts
│   ├── deltas/US-XXX.md              # Per-Story delta: Behavior + SDD (exists only while in flight)
│   ├── deltas/archive/               # Merged deltas, date-prefixed (frozen history)
│   ├── nfr.md                        # Non-functional requirements
│   ├── constitution.md               # Architectural invariants
│   └── ddd/                          # DDD (if multi-domain)
│       ├── context-map.md
│       └── glossary.md
├── .ai/                              # Memory + (optional) orchestrator files (FB-022)
│   ├── HANDOFF.md                    # Methodology memory: read on start, write on end (Full Mode)
│   ├── history.md                    # Methodology memory: append-only archive (DONE, LOG, sessions)
│   ├── review-report.md              # Methodology memory: Review Session output (when run)
│   ├── STATE.json                    # Orchestrator-only (legacy) — DO NOT modify
│   └── CHECKLIST.md                  # Orchestrator-only (legacy)
└── tests/
```

## What You Never Do

- **Never modify STATE.json** — that's the orchestrator's file
- **Never *start* a Story the human hasn't confirmed** — proposing the top of NEXT when
  NOW is empty is fine (FB-022); starting without confirmation is not
- **Never skip the Review Checkpoint** — if the human hasn't reviewed, ask them to
- **Never rewrite the entire SDD** — use Delta Spec format
- **Never loop more than max_attempts** — stop, record blocker, wait for help
- **Never commit secrets** — API keys, tokens, passwords, connection strings must never
  appear in source code. Use environment variables or placeholders (`YOUR_API_KEY_HERE`).
  Check `.gitignore` before committing config files.
- **Never write the Review Checkpoint summary to a file** — it is an ephemeral view assembled
  from the delta and shown in chat. The durable disclosure lives in the delta's
  `## Review Disclosure` section, which rides to `docs/deltas/archive/` on merge (FB-016).

## ACF Version

**Current ACF Version: 0.28** (= the `Framework/Refinement.md` changelog version — this
skill's declaration is the comparand, FB-020).

CLAUDE.md should include an `ACF Version` line (e.g. `ACF Version: 0.28`). If the project's
tag is older than the current version above, read the Refinement changelog rows in between
to see what actually changed, then propose adopting new features at natural touchpoints
(session start, story completion) — never auto-upgrade. See Lifecycle.md for the full
migration model.

## Review → Triage → Re-entry

If the human or orchestrator triggers a **Review Session**, you perform five checks:
Code Review, Spec-Code Coherence, Regression, Security Scan, and Memory Audit. Output
a `.ai/review-report.md` and update ISSUES. This is analysis only — no mutations to code.

If you're asked to **reopen a completed US** (via triage), treat it like resuming from
the rollback target step. A completed US has **no active delta** — it was archived on merge
(`docs/deltas/archive/`). So read the **merged truth**: `docs/specs/` (current behavior) +
`docs/sdd.md` (current architecture) + the existing tests; the archived delta is read-only
context, the spec is the contract. If the reopen **changes behavior**, re-enter at `bdd` and
write a **fresh** delta covering only the fix; if it only **fixes code to match the spec**
(regression, flaky test), re-enter at scaffold/impl/verify against the spec — no new delta.
Modify incrementally (not rewrite). Add a history entry: `US-XXX reopened — reason: ...`
