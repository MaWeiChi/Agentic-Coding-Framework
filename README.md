# Agentic Coding Framework

**Project Context Infrastructure for AI-Assisted Development**

A tool-agnostic framework that turns implicit project knowledge into explicit, structured documents — so AI coding agents spend tokens on implementation, not guessing your architecture.

## The Problem

Every new conversation with an AI coding agent starts from scratch. The agent doesn't know your architecture, your naming conventions, your API contracts, or where you left off. You end up repeating the same context, correcting the same misunderstandings, and burning tokens on re-explanation instead of real work.

## The Solution

This framework defines a layered set of project documents that agents load on demand. Stable information (project purpose, architecture) is written once and reused across hundreds of conversations. Dynamic state (current progress, blockers) is tracked in a living memory file. The result: each agent session starts with full context and zero ramp-up cost.

## Framework Layers

```
Layer 1: Project Summary       — Why / Who / What (read every session)
         PROJECT_MEMORY.md     — Dynamic state: where we are, what's next
Layer 2: BDD Scenarios         — Given / When / Then behavior specs
Layer 3: SDD                   — Architecture, modules, tech decisions
         API Contracts         — OpenAPI / AsyncAPI interface definitions
         ── Review Checkpoint ── Human confirms direction before coding
Layer 4: TDD                   — Test Scaffolding (red) → Implementation (green) → Verify
```

Each User Story runs through Layers 2–4 as an independent micro-waterfall cycle. Between stories, you maintain full agile flexibility — reprioritize, pivot, or insert new work at any time.

## Documents

| Document | Purpose | When to Load |
|----------|---------|-------------|
| [Framework](Framework/Agentic_Coding_Framework.md) | Core concepts: layered definitions, principles, workflow | Every conversation |
| [Lifecycle](Framework/Agentic_Coding_Lifecycle.md) | Operating mechanism: iteration model, test strategy, CI/CD | When planning iterations or CI setup |
| [Templates](Framework/Agentic_Coding_Templates.md) | Concrete templates: BDD, SDD, API contract, Memory, DDD | When writing any framework document |
| [Protocol](Framework/Agentic_Coding_Protocol.md) | Orchestrator ↔ Executor communication: state management, dispatch, hooks | When setting up automation or multi-agent flows |
| [Refinement](Framework/Agentic_Coding_Refinement.md) | Refinement tracking: what was evaluated, what was incorporated | Reference only |

## Key Design Decisions

**Macro-agile, micro-waterfall.** Between stories is agile (reprioritize freely). Within a story is waterfall (BDD → SDD → Review → TDD → Verify). This gives agents the clear sequential inputs they work best with, while preserving human strategic flexibility.

**Incremental, not rewrite.** SDD updates use Delta Spec format (ADDED / MODIFIED / REMOVED). Agents never regenerate the entire architecture document — they read what exists and append changes. This saves tokens and prevents accidentally losing prior design decisions.

**Load on demand.** Agents don't read everything every session. The Project Summary and Memory are always loaded. BDD, SDD, and contracts are loaded only when relevant to the current story. The Protocol is loaded only when configuring automation.

**Review before code.** A human Review Checkpoint sits between design and implementation. At this point, BDD scenarios, the SDD delta, and API contract changes are all visible — and changes are cheap. Once implementation begins, the cost of going back rises sharply.

**Tool-agnostic.** The framework defines *what documents your project needs* and *in what order to produce them*. It doesn't prescribe which AI tool runs the process. Claude Code, Cursor, Windsurf, Copilot, or a custom orchestrator can all consume these documents.

## Optional Extensions

The framework starts minimal and scales up as complexity demands:

- **ADR** (Architecture Decision Records) — Why you chose A over B. Prevents agents from "helpfully refactoring" designs that have specific reasons.
- **DDD Strategic Design** — Bounded contexts, ubiquitous language, aggregate roots. Triggered when multiple business domains cause naming conflicts.
- **Constitution** — Inviolable architectural principles (e.g., "no direct cross-module DB access"). Agents check these before every design decision.
- **NFR** (Non-Functional Requirements) — Performance, security, availability thresholds with unique IDs referenced by BDD scenario tags.

## Protocol: Multi-Agent Automation

The [Protocol document](Framework/Agentic_Coding_Protocol.md) defines how an external orchestrator can automate the micro-waterfall cycle:

- **Three-layer architecture**: External Orchestrator → Story-Level Coordinator → Executor group
- **Three-file protocol**: `STATE.json` (machine state) + `HANDOFF.md` (context) + `PROJECT_MEMORY.md` (cross-tool state)
- **Progressive adoption**: Level 0 (fully manual) → Level 1 (semi-automated hooks) → Level 2 (fully automated dispatch)
- **Complexity-based dispatch**: Simple stories get a single executor; complex stories get a coordinated team with role-based context isolation

## Quick Start

### New Project

1. Write a Project Summary (Why / Who / What) in your repo root
2. Create `PROJECT_MEMORY.md` with current state
3. For your first User Story, write BDD scenarios using the [Templates](Framework/Agentic_Coding_Templates.md)
4. Define affected architecture in the SDD (or SDD Delta Spec)
5. Review. Then let the agent write test scaffolding and implement.

### Existing Project

1. Have an agent scan your codebase and reverse-engineer a Project Summary + SDD
2. Manually correct — add implicit knowledge the agent can't read from code
3. Add characterization tests for existing behavior
4. New features enter the normal BDD → SDD → TDD flow

## Project Structure

```
your-project/
├── CLAUDE.md / PROJECT_CONTEXT.md    # Layer 1: Project Summary
├── PROJECT_MEMORY.md                  # Dynamic state tracking
├── docs/
│   ├── bdd/                           # Layer 2: BDD scenarios per story
│   │   └── US-001.feature
│   ├── sdd/                           # Layer 3: Software Design Document
│   │   └── sdd.md
│   ├── api/                           # Interface contracts
│   │   └── openapi.yaml
│   ├── deltas/                        # SDD Delta Specs (archived)
│   │   └── US-001.md
│   ├── nfr.md                         # Non-functional requirements
│   ├── constitution.md                # Architectural invariants
│   └── ddd/                           # DDD strategic design (if needed)
│       ├── context-map.md
│       └── glossary.md
├── .ai/                               # Protocol files (if using orchestrator)
│   ├── STATE.json
│   └── HANDOFF.md
└── tests/                             # Layer 4: Test files
```

## Versions

| Document | Version | Date |
|----------|---------|------|
| Framework | v0.18 | 2026-02-16 |
| Lifecycle | v0.4 | 2026-02-16 |
| Templates | v0.9 | 2026-02-16 |
| Protocol | v0.7 | 2026-02-16 |
| Refinement | v0.9 | 2026-02-17 |

## License

[MIT](LICENSE)
