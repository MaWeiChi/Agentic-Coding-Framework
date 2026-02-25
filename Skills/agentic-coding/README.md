# Agentic Coding Skill — Assessment

> Third-party review by Windsurf (Claude Opus 4.6 thinking), February 2026.

## What This Skill Is

A structured context protocol that turns an LLM coding agent into a disciplined executor following a repeatable per-Story micro-waterfall: BDD → SDD Delta → API Contract → Review → Test → Implement → Verify → Commit → Update Memory. It solves three specific problems.

---

## Problem 1: Context Loss Across Sessions

LLMs have no persistent memory. Every new session starts cold.

**How the skill solves it:**

- `PROJECT_MEMORY.md` carries hot state (NOW/NEXT/TESTS/SYNC/ISSUES) — re-sent every turn
- `.ai/history.md` archives cold state — loaded on demand
- `HANDOFF.md` bridges sessions with structured YAML + freeform context
- Git commit hash in the `<!-- -->` header provides a factual anchor to detect drift

**Effective?** Yes. This is the single highest-value aspect. Without it, multi-session agent work is essentially stateless — the agent re-discovers context every time, makes contradictory decisions, or silently drops prior work. The hot/cold split is particularly well-designed for token economy.

---

## Problem 2: Scope Creep and Architectural Drift

Agents will happily rewrite entire architectures, refactor unrelated code, or invent requirements if unconstrained.

**How the skill solves it:**

- Delta-only SDD updates — prevents full-document regeneration that loses prior decisions
- Non-Goals sections in BDD and Delta Spec — explicit scope boundaries
- Constitution — immutable architectural principles that act as guardrails
- `[NEEDS CLARIFICATION]` convention — forces the agent to stop instead of inventing
- Review Checkpoint — mandatory human gate before implementation
- "What You Never Do" list — hard behavioral boundaries

**Effective?** Yes. These are the exact failure modes of unconstrained agent coding. The Delta-only rule alone prevents a common and expensive failure: agent regenerates the SDD, silently drops 3 design decisions, and introduces contradictions.

---

## Problem 3: Quality Without Manual Oversight

Agents produce code that "looks right" but has gaps — untested paths, contract mismatches, broken invariants.

**How the skill solves it:**

- BDD-first — behavior defined before code exists
- Test scaffolding in RED — all tests must fail initially (TDD discipline)
- Triple verification gate (Completeness / Correctness / Coherence) before declaring done
- Self-correction loop with hard limit (max 3-5 attempts) — prevents infinite fix loops, escalates to human when stuck
- Step 0 characterization tests — safety net before modifying existing code

**Effective?** Yes. The triple-check is the key mechanism. Without it, agents declare "done" when tests pass but contract mismatches or missing scenarios go undetected. The max_attempts limit is also pragmatically important — it recognizes that repeated failures indicate a design problem, not a code problem.

---

## Cost-Benefit Summary

| Cost                                  | Benefit                                                                               |
| ------------------------------------- | ------------------------------------------------------------------------------------- |
| Bootstrap overhead (Full Mode)        | Amortized over all subsequent Stories                                                 |
| Token cost of PROJECT_MEMORY re-send  | Far less than agent re-discovering context each turn                                  |
| Workflow rigidity (8 steps per Story) | Prevents the costliest agent failures: scope creep, context loss, silent quality gaps |
| Human review gate (Step 4)            | Catches misunderstandings before implementation, not after                            |

---

## Where It Won't Help

- **Truly one-shot tasks** — the framework overhead exceeds the task itself. Lite Mode mitigates this but even ~5 lines of PROJECT_MEMORY is overhead for a single `sed` command.
- **Non-coding tasks** — the workflow is code-centric (BDD, SDD, tests). It doesn't apply to writing prose, data analysis, or system administration.
- **Agents that can't follow multi-step instructions** — the skill assumes an agent capable of reading templates, producing structured documents, and self-verifying. Weaker models may not reliably execute the workflow.

---

## Verdict

The skill is well-scoped and effective for its target use case: multi-session, structured software development with LLM agents. The Lite/Full mode split gives it range — from quick fixes to full project lifecycles. The core design decisions (hot/cold memory split, delta-only updates, mandatory review gate, triple verification, self-correction limits) each address a real and specific failure mode of agentic coding. No superfluous ceremony detected.
