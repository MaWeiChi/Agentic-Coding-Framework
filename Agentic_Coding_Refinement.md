# Agentic Coding Framework — Refinement Checklist

**Tool-Agnostic · Filtered by Token / Quality / Autonomy Dimensions**

This document contains refinement suggestions for the framework itself, independent of any specific tool or orchestrator. These apply to any AI tool (Claude Code, Cursor, Windsurf, Copilot, etc.) adopting this framework.

---

## Filtering Criteria

From four comparative analyses (BDD / SDD / TDD / DDD) yielding 30 suggestions, filtered by three dimensions:

| Dimension | Guiding Question |
|-----------|-----------------|
| **Token** | Does it save tokens in actual agent workflows? (Prevent reruns, reduce ambiguity, avoid scope bloat) |
| **Quality** | Does it measurably improve agent output quality? |
| **Autonomy** | Does it make agents more self-directed, reducing human intervention? |

All three dimensions → Must-Do, two → Worth-Doing, one or fewer → Not Included.

---

## Must-Do (8 Items) — All Incorporated

### ~~1. TDD Recursion Limit~~ → **Incorporated** into Lifecycle v0.2 + Protocol v0.1 (max_attempts)

### ~~2. Data Model Source of Truth~~ → **Incorporated** into Templates v0.7 (SDD Writing Principles)

### ~~3. Non-Goals / Out of Scope~~ → **Incorporated** into Templates v0.7 (BDD + SDD Delta Spec)

### ~~4. Scenario Outline (Parameterized Scenarios)~~ → **Incorporated** into Templates v0.7 (BDD Template)

### ~~5. AST Linting Integration~~ → **Incorporated** into Lifecycle v0.2 + Protocol v0.1 (post_check)

### ~~6. Helper Function Extraction Principles~~ → **Incorporated** into Templates v0.7 (Test Scaffolding Writing Principles)

### ~~7. Subdomain Classification~~ → **Incorporated** into Templates v0.7 (DDD Level 1 Context Map)

### ~~8. testify Pattern Integration~~ → **Incorporated** into Templates v0.7 (Test Scaffolding: require/assert + Table-Driven + Suite)

---

## Worth-Doing (5 Items) — All Incorporated

| # | Suggestion | Status |
|---|-----------|--------|
| ~~9~~ | **Declarative Style Guidelines** | **Incorporated** into Templates v0.7 (BDD Writing Principles) |
| ~~10~~ | **System Context Description** | **Incorporated** into Templates v0.7 (SDD Writing Principles) |
| ~~11~~ | **Mermaid Diagram Guidelines** | **Incorporated** into Templates v0.7 (SDD Writing Principles) |
| ~~12~~ | **Anti-Pattern Checklist** | **Incorporated** into Templates v0.7 (BDD Writing Principles) |
| ~~13~~ | **Domain Event Registry** | **Incorporated** into Templates v0.7 (DDD Format Guidelines) |

---

## Not Included (17 Items) and Rationale

| Original Suggestion | Reason for Exclusion |
|--------------------|---------------------|
| Background Syntax Standardization | Cosmetic formatting; agents can parse existing syntax |
| @wip / @skip Tags | `[NEEDS CLARIFICATION]` already covers the core need |
| Example Mapping | Human process, not an agent process |
| Module Error Handling Strategy | Project-level detail; framework should not prescribe |
| ADR Status Mechanism | Human process management; agents only need "what is the current decision" |
| Event Storming Integration | Human process; framework is positioned as the agent's working foundation |
| Context Mapping Patterns (supplement) | Only needed for enterprise-scale scenarios; add when encountered |
| ~~Dynamic Context Loading~~ | ~~Implementation-layer concern~~ → **Incorporated** into Protocol v0.4 Multi-Executor Scoped Context Loading |
| ~~Test/Impl Context Isolation~~ | ~~Implementation-layer concern~~ → **Incorporated** into Protocol v0.4 Multi-Executor Role-Based Context Isolation |
| Aggregate Design Principles | Only triggered at Level 3; too early to define |
| Context Evolution Strategy | Very few projects encounter this |
| Runtime View | BDD scenarios already describe behavior |
| Cross-cutting Concerns | Can be folded into Constitution |
| Deployment View | Framework intentionally excludes; stops at image push |
| ~~Agent Subscription Mechanism~~ | ~~Multi-agent collaboration implementation-layer~~ → **Incorporated** into Protocol v0.4 Multi-Executor Coordinator ↔ Executor Communication |
| ~~YAML Handoff Format~~ | ~~Multi-agent collaboration implementation-layer~~ → **Incorporated** into Protocol v0.4 Multi-Executor Per-Task HANDOFF + Protocol v0.5 HANDOFF.md Hybrid Format (YAML front matter) |
| Multi-Language Test Scaffolding | Extend as needed; no need to predefine |

---

## Impact Summary

| Document | Must-Do | Worth-Doing | Total | Status |
|----------|:-------:|:-----------:|:-----:|:------:|
| Templates → BDD | 2 | 2 | 4 | All Incorporated |
| Templates → SDD | 2 | 2 | 4 | All Incorporated |
| Templates → Test | 2 | 0 | 2 | All Incorporated |
| Templates → DDD | 1 | 1 | 2 | All Incorporated |
| Lifecycle | 2 | 0 | 2 | All Incorporated |
| **Framework (main)** | **0** | **0** | **0** | — |
| **Total** | **8** | **5** | **13** | **13/13** |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2026-02-13 | Initial version: Filtered 30 comparative suggestions down to 13 (8 Must-Do + 5 Worth-Doing) using Token/Quality/Autonomy dimensions |
| v0.2 | 2026-02-14 | Status update: All 13 items incorporated (8 Must-Do → Templates v0.7 + Lifecycle v0.2 + Protocol v0.1; 5 Worth-Doing → Templates v0.7); 4 "Not Included" items incorporated into Protocol v0.4 Multi-Executor collaboration mode |
