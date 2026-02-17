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
| [Framework](Framework/Framework.md) | Core concepts: layered definitions, principles, workflow | Every conversation |
| [Lifecycle](Framework/Lifecycle.md) | Operating mechanism: iteration model, test strategy, CI/CD | When planning iterations or CI setup |
| [Templates](Framework/Templates.md) | Concrete templates: BDD, SDD, API contract, Memory, DDD | When writing any framework document |
| [Protocol](Framework/Protocol.md) | Orchestrator ↔ Executor communication: state management, dispatch, hooks | When setting up automation or multi-agent flows |
| [Protocol-Advanced](Framework/Protocol-Advanced.md) | Multi-executor collaboration, OpenClaw and Agent Teams reference implementations | Only when building multi-executor or custom orchestrator |
| [Refinement](Framework/Refinement.md) | Refinement tracking: what was evaluated, what was incorporated | Reference only |

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

The [Protocol document](Framework/Protocol.md) defines how an external orchestrator can automate the micro-waterfall cycle:

- **Three-layer architecture**: External Orchestrator → Story-Level Coordinator → Executor group
- **Three-file protocol**: `STATE.json` (machine state) + `HANDOFF.md` (context) + `PROJECT_MEMORY.md` (cross-tool state)
- **Progressive adoption**: Level 0 (fully manual) → Level 1 (semi-automated hooks) → Level 2 (fully automated dispatch)
- **Complexity-based dispatch**: Simple stories get a single executor; complex stories get a coordinated team with role-based context isolation

## Quick Start (5 Steps to Your First Story)

### Step 1 — Choose Your Mode

| Question | If yes → | If no → |
|----------|----------|---------|
| Will this project run for 3+ stories? | **Full Mode** | **Lite Mode** |
| Multiple agents or team members? | Full Mode | Either |
| Quick prototype or spike? | Lite Mode | Either |

Lite Mode skips `.feature` files, Delta Spec, API Contracts, and Review Checkpoint. You can upgrade to Full Mode at any time by adding those documents.

### Step 2 — Write a Project Summary

Create `CLAUDE.md` (or `PROJECT_CONTEXT.md`) in your repo root. This is the one file every agent session reads first. Cover three things:

```markdown
## Why — The problem this project solves
## Who — Target users and stakeholders
## What — Key features and technical boundaries (language, framework, constraints)
```

This takes 10–15 minutes and saves hours of repeated explanation across future sessions.

### Step 3 — Create PROJECT_MEMORY.md

This is your living state file. Start with a minimal version:

```markdown
# PROJECT_MEMORY

## NOW
Working on: (first story description)

## NEXT
- (second story)
- (third story)

## ISSUES
(none yet)
```

Agents update this file at the end of each session so the next session starts with full context.

### Step 4 — Run Your First Story

**Full Mode:** Write BDD scenarios → Design SDD delta → Review with human → Write tests → Implement → Verify.

**Lite Mode:** Describe the story in one sentence → Let the agent propose approach → Approve → Implement → Verify.

Both modes produce working, tested code. Full Mode produces additional design documents that compound in value as the project grows.

### Step 5 — Update Memory and Iterate

After the story is complete, update `PROJECT_MEMORY.md`: move the finished story out of NOW, pull the next one in, and note any blockers or decisions made. Each subsequent session starts from this checkpoint — no re-explanation needed.

### Adopting on an Existing Project

If you have an existing codebase, insert one extra step before Step 4: ask your agent to scan the repo and reverse-engineer a Project Summary + SDD from existing code. Then manually correct — add the implicit knowledge that only exists in your head (why you chose X over Y, what must never change). After that, new features enter the normal flow.

## Skill Package

The `Skills/agentic-coding/` directory contains a ready-to-install AI agent skill that encapsulates the framework's workflow into token-optimized reference files. Instead of loading the full framework documents (~160KB), the skill provides condensed references (~25KB) that give agents everything they need during a session.

The skill includes `SKILL.md` (entry point with mode selection, project structure, and principles), `references/workflow.md` (step-by-step micro-waterfall procedure), and `references/templates.md` (condensed document templates). See the [Skill README](Skills/agentic-coding/README.md) for a third-party effectiveness assessment.

## Installation

**Claude Code:**
```bash
cp -r Skills/agentic-coding ~/.claude/skills/
```

**Other AI tools (Cursor, Windsurf, Copilot, etc.):**
Copy the `Framework/` directory into your project and reference it in your tool's configuration file. The framework documents are tool-agnostic Markdown — any agent that can read files can use them.

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

## Acknowledgments

This framework was designed through comparative analysis with established methodologies and AI-assisted development tools. We gratefully acknowledge the following projects and standards whose ideas informed the framework's design:

**BDD:** Cucumber, SpecFlow, Behave, pytest-bdd — scenario syntax, declarative style, and tagging conventions.
**SDD:** arc42, C4 Model, IEEE 1016 — architecture documentation structure and layered description approaches.
**TDD:** GPT-Pilot Dev Loop, Aider Repo Map, MetaGPT Message Pool, OpenSpec / Spec Kit, testify — agent-driven development loops, context compression, and test scaffolding patterns.
**DDD:** Eric Evans (*Domain-Driven Design*), Vaughn Vernon (*Implementing Domain-Driven Design*) — strategic design, bounded contexts, and ubiquitous language.

## Versions

| Document | Version | Date |
|----------|---------|------|
| Framework | v0.18 | 2026-02-16 |
| Lifecycle | v0.4 | 2026-02-16 |
| Templates | v0.9 | 2026-02-16 |
| Protocol | v0.8 | 2026-02-17 |
| Protocol-Advanced | v0.8 | 2026-02-17 |
| Refinement | v0.9 | 2026-02-17 |

## License

[MIT](LICENSE)
