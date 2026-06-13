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

## Field Feedback — Pilot Project (FB-001~006)

Source: Pilot project field observations after completing US-001.

### FB-R01: Full/Lite Mode ← FB-004

**Decision: User specifies the mode in CLAUDE.md. Agent does not auto-detect.**

Configuration: Add `Agentic Coding Mode: full` or `lite` in CLAUDE.md's Agent Guidelines section.

**Lite mode also retains a minimal PROJECT_MEMORY (NOW + NEXT only, ~5 lines).** Rationale: even tasks assumed to be one-time may have follow-up sessions. The cost is negligible (~50 input tokens/turn) and provides a breakpoint for future sessions. This also makes Lite → Full upgrades smoother — NOW/NEXT already exist as a foundation.

| | Full Mode | Lite Mode |
|---|---|---|
| Use case | Multi-session handoff, high coupling, multi-agent | Urgent start, low coupling, short tasks |
| CLAUDE.md | Complete | ≤10 lines |
| PROJECT_MEMORY | Complete (NOW/NEXT/TESTS/SYNC/ISSUES) | Minimal (NOW + NEXT only, ~5 lines) |
| SDD / Constitution / NFR | Yes | Skip |
| Delta Spec | Yes | Verbal or commit message |
| BDD | Full Gherkin | Write tests directly |
| HANDOFF | Yes | Not used |

**Lite mode positioning — an on-ramp to Full:**

Lite mode is not just "for small tasks." It also serves as an entry point for projects that will eventually need Full mode but can't afford the Bootstrap cost right now.

| Scenario | Mode | Rationale |
|----------|------|-----------|
| New project, 5+ stories planned | Full | Worth the upfront investment |
| Existing project, full framework adoption | Full | Bootstrap once, amortize over time |
| Existing project, urgent need to start NOW | Lite → upgrade to Full later | Ship first, build infrastructure later |
| Full project winding down, only small fixes left | Full → downgrade to Lite | Infrastructure overhead no longer justified |
| One-off bug fix or small feature | Lite | Will never need upgrade |

**Mode switching:**

Users can switch modes in two equivalent ways:
1. Directly edit the mode line in CLAUDE.md
2. Tell the agent verbally (e.g., "switch to Full mode") — agent updates CLAUDE.md

**Agent behavior on mode switch — must acknowledge and inform:**

When the agent detects a mode change (either by reading CLAUDE.md or receiving a verbal instruction), it MUST:
1. Confirm the switch direction (Lite → Full or Full → Lite)
2. Explain which scenario this matches from the table above, and why this mode fits
3. Execute the corresponding transition

Example: User says "switch to Full mode" →
> "Switching to Full mode. This is typically for projects needing multi-session handoff or where stories have high coupling. I'll run the Upgrade Checklist to set up the missing infrastructure..."

**Upgrade Checklist (Lite → Full):**
```
1. ☐ Expand CLAUDE.md (add Why/Who/What, Project Structure, Development Conventions)
2. ☐ Expand PROJECT_MEMORY.md (add TESTS/SYNC/ISSUES to existing NOW/NEXT)
3. ☐ Create docs/sdd/sdd.md (scan codebase, reverse-engineer)
4. ☐ Create docs/constitution.md (3-5 core principles)
5. ☐ Create .ai/HANDOFF.md + .ai/history.md
6. ☐ Human confirms above outputs
```

**Downgrade (Full → Lite):**
- Update CLAUDE.md mode line
- Agent stops maintaining SDD/HANDOFF/full Memory
- Existing docs remain (not deleted), just no longer actively maintained
- Slim PROJECT_MEMORY to NOW + NEXT only

**Design rationale:**
- Agent auto-detection is unreliable (story count ≠ complexity)
- The real decision axes are "handoff frequency × change coupling", which require human context
- CLAUDE.md exists in both modes, making it the most natural location for this setting
- Persists across sessions without needing to be re-stated verbally
- Mode switching via verbal instruction is natural and equivalent to manual CLAUDE.md edit

**Status:** ✅ Incorporated into Framework v0.18 + Skill

---

### FB-R02: Token Cost Optimization ← FB-001 + FB-003

**Decision: Two-layer approach — slim down auto-resent files + HANDOFF as latest-entry-only.**

**Layer 1: Input tokens — PROJECT_MEMORY slim-down**

Design principle: Files auto-resent by system-reminder = files you pay for every turn. Only keep information the agent needs every turn.

| Section | Keep/Move | Rationale |
|---------|-----------|-----------|
| NOW | Keep | Needed every turn |
| NEXT | Keep | Scope guard + priority |
| TESTS | Keep | Quick quality status check |
| SYNC | Keep | Orientation / locator |
| ISSUES | Keep | Scope guard reference (FB-002: saw hardcoded IP → checked TD-03 → belongs to US-002 → don't touch) |
| DONE | Move → `.ai/history.md` | Only useful at session start, not needed every turn |
| LOG | Move → `.ai/history.md` | git log is always available, not needed every turn |

Estimated effect: PROJECT_MEMORY ~55 lines → ~35 lines, saving ~200 input tokens per turn.

**Layer 2: Output tokens — HANDOFF latest-entry-only + history archive**

- HANDOFF.md is latest-entry-only: each session overwrites it with current state
- Historical session records are appended to `.ai/history.md` (shared with DONE/LOG)
- Agent only needs to read HANDOFF (one entry) at session start; reads history only when needed

Effect: HANDOFF write volume is fixed and small (one block), no more full-file rewrites.

**Impact on Skill files:**
1. workflow.md — Update Memory step: DONE and LOG write to `.ai/history.md`
2. templates.md — PROJECT_MEMORY template slimmed down, DONE and LOG removed, new location noted
3. SKILL.md — New principle: "Keep auto-resent files minimal"
4. workflow.md — HANDOFF section changed to latest-entry-only + history archive

**Status:** ✅ Incorporated into Skill v0.18

---

### FB-R03: Bootstrap Strategy ← FB-005 + FB-006

**Decision: Characterization tests moved from Bootstrap checklist to per-Story Step 0 pre-check. "Touch it, test it" strategy.**

**Scope Rule: Only test the current behavior of functions this Story will modify. Don't test the entire module.**

Example: US-002 modifies `setupPeerConnection` → only add characterization tests for `setupPeerConnection`, not for `closePeerConnection` in the same module that nobody is changing.

**Step 0: Safety Net Check (Full Mode only, existing codebases only)**
```
- List the functions/modules this Story will modify
- Check if each has existing test coverage
- If no coverage → add characterization test (current behavior only)
- If covered → proceed
```

Lite Mode does not distinguish characterization vs new tests — write tests directly.

**Design rationale:**
- Writing all characterization tests at once is too expensive (entire session with zero feature output)
- May write tests for modules that will never be modified — waste
- Just-in-time testing: only spend cost when protection is needed
- Cost is naturally amortized across Stories, no single session is all-testing

**Impact on Skill files:**
1. workflow.md — Bootstrap section: remove "write characterization tests for all existing features"
2. workflow.md — Add Step 0: Safety Net Check before Per-Story Steps
3. SKILL.md — New principle: "Touch it, test it"

**Status:** ✅ Incorporated into Skill v0.18

---

### FB-R04: PROJECT_MEMORY + HANDOFF Value Assessment ← FB-002

**Observation recorded, no independent action needed.** Conclusion merged into FB-R01 (Full/Lite mode applicability).

Cross-session projects benefit from Memory/HANDOFF. Single-session tasks do not. This is exactly why Lite Mode exists.

**Status:** ✅ Merged into FB-R01

---

### FB-R05: Lite Mode Fast Path ← FB-007 Item 1

**Decision: Lite mode auto-skips `.feature` file, Delta Spec, API Contract, Review Checkpoint, and Constitution/NFR checks.**

The BDD value is in the thinking process (defining scope), not in the `.feature` file format. In Lite mode, write BDD-style test function names (`Given_When_Then`) directly in code. No separate document layer.

| Skipped in Lite Mode | Replacement |
|---------------------|-------------|
| `.feature` file | BDD-style test names in code |
| Delta Spec | Commit message or verbal description |
| API Contract | Only for new API design |
| Review Checkpoint | Only on architecture-level changes |
| Constitution / NFR | Skipped (principles internalized) |

**Impact on Skill files:**
1. SKILL.md — Full/Lite comparison table expanded with API Contract and Review Checkpoint rows
2. workflow.md — Step 1 Lite Mode shortcut rewritten as "fast path" with explicit skip list

**Status:** ✅ Incorporated

---

### FB-R06: System-Reminder Token Cost Warning ← FB-007 Item 2

**Decision: Add explicit token budget numbers to the "Keep auto-resent files minimal" principle in SKILL.md.**

Real-world measurement from pilot project:
- Before slimming: ~1.5K input tokens/turn (PROJECT_MEMORY 85 lines + CLAUDE.md)
- After slimming: ~0.7K input tokens/turn (PROJECT_MEMORY 33 lines + CLAUDE.md)
- Saving: 53% per turn, ~16K tokens over a 20-turn session

Framework overhead per US: ~11K tokens (Memory update + HANDOFF + BDD + Delta), vs ~15K tokens for implementation itself = 42% overhead ratio.

**Impact on Skill files:**
1. SKILL.md — Added token budget reference box under "Keep auto-resent files minimal"

**Status:** ✅ Incorporated

---

### FB-R07: Team Size Modifier ← FB-007 Item 3

**Decision: Add `Team Size: 1|N` as an orthogonal modifier to Full/Lite mode in CLAUDE.md.**

Solo developers using Full mode need the memory infrastructure (PROJECT_MEMORY, SYNC, history) but not the inter-person coordination artifacts (Delta Spec, Review Checkpoint, API Contract for minor changes).

| Step | Solo (Team Size: 1) | Team (Team Size: N) |
|------|---------------------|---------------------|
| Delta Spec | Optional — commit message may suffice | Required |
| Review Checkpoint | Skip unless architecture-level | Always |
| API Contract | Only for new API design | Always |
| HANDOFF | Recommended | Required |

Default: Team behavior (safer) when `Team Size` not specified.

**Impact on Skill files:**
1. SKILL.md — New "Team Size Modifier" subsection under Full/Lite Mode
2. templates.md — CLAUDE.md template includes `Team Size: 1` line

**Status:** ✅ Incorporated

---

### FB-007: Full Project ROI Review (US-001→009 Completion)

**Date:** 2026-02-16
**Context:** End-of-project review after completing all 9 US + 10 TD. 14 commits across multiple sessions.

#### High ROI Elements (Retain)

| Element | Rating | Explanation |
|---------|--------|-------------|
| **PROJECT_MEMORY** | ⭐⭐⭐ | One line of NOW locates breakpoint across sessions; SYNC replaces grepping entire codebase |
| **HANDOFF.md** | ⭐⭐⭐ | Prevents repeated decisions, preserves Key Decisions, zero-cost onboarding for new sessions |
| **SYNC section** | ⭐⭐⭐ | Quickly locate files for each concern — 10x faster than grep |
| **ISSUES list** | ⭐⭐ | Effective scope guard — see a problem, check if it belongs to another US first, prevents scope creep |
| **BDD-driven scoping** | ⭐⭐ | Gherkin scenarios → Go test almost 1:1 conversion, clear definition prevents over-building |
| **Touch-it-test-it (FB-006)** | ⭐⭐ | Avoids one-time big-bang testing, cost naturally amortized across each US |

#### Low ROI Elements (Simplify or Skip)

| Element | Problem | Recommendation |
|---------|---------|----------------|
| **.feature files** | No BDD runner (Go doesn't use Cucumber), files are human-readable docs only | Write BDD-style function names directly in test files, skip the document layer |
| **Delta Spec** | For solo development, implementing directly is faster than writing Delta then implementing | Solo: commit message suffices; Team: still needed |
| **Review Checkpoint** | Every time it's manual "ok" auto-pass, no substantive review | Only pause for review on architecture-level changes |
| **Constitution / NFR** | Written once, rarely consulted afterward — principles are internalized | Valuable initially, freeze after stabilization, no longer actively maintain |
| **API Contract (OpenAPI)** | Adding a query param is overhead to update OpenAPI | Only write for new API design, skip for incremental changes |

#### Token Consumption Analysis

**System-reminder per-turn hidden cost:**
```
Before slimming: PROJECT_MEMORY (85 lines) + CLAUDE.md ≈ ~1.5K input tokens/turn
After slimming:  PROJECT_MEMORY (33 lines) + CLAUDE.md ≈ ~0.7K input tokens/turn
Saving: ~53% per turn
```

**Per-US Framework overhead:**
```
Memory update:  ~4K output tokens (Read + Edit)
HANDOFF update: ~2K output tokens (Write)
BDD document:   ~3K output tokens (Write .feature)
Delta Spec:     ~2K output tokens (Write)
─────────────────────────────────
Framework total: ~11K tokens / US (excluding implementation)
```
Compared to US-009 implementation itself at ~15K tokens, Framework overhead ≈ 42%.

**Slimming measures effectiveness:**

| Measure | Saving | Implemented? |
|---------|--------|-------------|
| DONE/LOG/ISSUES moved to .ai/history.md | 61% line reduction (85→33) | ✅ |
| SYNC entries slimmed to one line | ~15% line reduction | ✅ |
| HANDOFF changed to latest-entry-only | ~30% output reduction | ✅ |

#### Applicability Conclusions (Updates FB-004)

| Scenario | Assessment | Recommended Mode |
|----------|-----------|-----------------|
| 5+ stories across multiple sessions | ✅ Worth it | Full (but skip .feature, Delta Spec optional) |
| 2-3 stories medium tasks | ⚠️ Borderline | Lite (keep only NOW + NEXT + SYNC) |
| Single bug fix | ❌ Not worth it | Don't use Framework |
| Multi-person / multi-agent collaboration | ✅ Most valuable | Full + HANDOFF required |

#### Core Learnings

1. **Memory system is the biggest winner** — cross-session handoff cost approaches zero, one line of NOW locates position
2. **Document layer should be minimized** — only put "needed every turn" information in system-reminder re-sent files
3. **BDD's value is not in the .feature file** — value is in the thinking process (defining scope), not in the output file format
4. **Solo projects should skip ceremonial steps** — Delta Spec, Review Checkpoint, API Contract have no substantive benefit for solo work
5. **Touch-it-test-it > one-time catchup** — characterization test strategy (FB-006) proven effective in practice, avoids waste
6. **Framework's biggest hidden benefit: output stability** — structural constraints eliminate agent uncertainty, reducing output variance per turn:
   - SYNC lets agent know which files to change without re-exploration — prevents changing wrong files
   - ISSUES acts as scope guard — see a problem, check attribution first, prevents ad-hoc fixes
   - HANDOFF prevents cross-session design drift — prevents re-discussing already-decided decisions
   - BDD-style naming makes test intent explicit — edge cases don't get missed
   - Without these constraints, agents commonly exhibit scope creep, forgotten decisions, modifications in unrelated locations

**Actionable items:** → FB-R05 (Lite fast path), FB-R06 (token warning), FB-R07 (Team Size)

**Status:** ✅ Recorded. FB-R05~R07 incorporated.

---

### FB-008: Agentic Coding Skill vs Claude Code Agent Teams / Sub-agents (Strategic Roadmap)

**Date:** 2026-02-16
**Context:** Comparison analysis after reading Agent Teams + Sub-agents official documentation.

#### Concept Mapping

| Skill Element | Agent Teams / Sub-agents Equivalent | Difference |
|---|---|---|
| **PROJECT_MEMORY** | Sub-agent `memory: project` (persistent memory) | Skill version is manually maintained; sub-agent version auto-injects first 200 lines of MEMORY.md |
| **HANDOFF.md** | Agent Teams mailbox + shared task list | Skill version persists across sessions; teams version is runtime-only, no session resumption |
| **SYNC section** | Sub-agent spawn prompt context | Teams docs emphasize teammates don't inherit lead's history — need sufficient context in spawn prompt. SYNC solves exactly this |
| **ISSUES scope guard** | Agent Teams task dependency | Teams support blocked tasks waiting for dependency completion; ISSUES is the static version of the same concept |
| **BDD → Test Scaffold** | Sub-agent chaining (plan → implement → verify) | Can be split into sub-agents each executing independently |
| **Review Checkpoint** | Agent Teams `requirePlanApproval` | Teams can require teammate plan approval from lead — more structured than our manual "ok" |

#### High Alignment: Skill Solved the Same Problems Before Agent Teams Existed

**1. Persistent Memory = PROJECT_MEMORY**
Sub-agents' `memory` field lets agents save learning across sessions to `.claude/agent-memory/<name>/MEMORY.md`. Our PROJECT_MEMORY is the manual version of the same concept — implemented earlier, battle-tested.

**2. Spawn Context = SYNC**
Agent Teams docs repeatedly emphasize: teammates don't inherit lead's conversation history. Solution is giving sufficient context in spawn prompt. Our SYNC section is essentially pre-prepared spawn context — any new agent reads SYNC to know where each module lives.

**3. Shared Task List = ISSUES + US Attribution**
Agent Teams' shared task list (pending/in-progress/completed + dependency) and our ISSUES list (attributed to which US) are the same coordination mechanism.

#### Upgrade Directions (When Agent Teams Matures)

**1. Split Framework Steps into Sub-agents**
```
Current (single session):
  BDD → Delta Spec → Test Scaffold → Implement → Verify → Update Memory

Upgraded (sub-agent division):
  plan-agent:      BDD + Delta Spec (permissionMode: plan, read-only)
  implement-agent: Write code (tools: Edit, Write, Bash)
  verify-agent:    Run tests + triple check (tools: Bash, Read)
```
Benefit: Each agent has independent context window. BDD documents don't consume implementation context.

**2. Use Persistent Memory Instead of System-Reminder Re-send**
Sub-agent's `memory: project` reads MEMORY.md once at startup (first 200 lines), not re-sent every turn like our PROJECT_MEMORY via system-reminder. If the Skill is restructured as a sub-agent, token cost drops further.

**3. Agent Teams for Large-Scope US**
Agent Teams docs recommend for:
- Research and review (multi-angle simultaneous exploration)
- New modules (each responsible for separate files)
- Cross-layer coordination (frontend + backend + test each with their own agent)

Example: A US spanning SFU (backend) + quality selector (frontend) + testing is ideal for an agent team.

#### Not Recommended to Change

**1. Single-person Single-session Doesn't Need Agent Teams**
Agent Teams' core value is direct inter-teammate communication (mailbox). Our skill is for single-person use — no need for inter-agent messaging. Occasional sub-agent division is sufficient.

**2. Agent Teams Is Currently Experimental + High Token Cost**
Official documentation explicitly notes:
- Experimental, disabled by default
- No session resumption with in-process teammates
- Token cost far higher than single session
- Task status can lag

Our Skill achieves similar coordination effects with more token-efficient means (persistent files).

#### Conclusion

> **Agentic Coding Skill is the "poor man's Agent Teams" — simulating shared task list + mailbox + persistent memory via the file system. Because it doesn't require runtime multi-agent overhead, token efficiency is actually higher.**

#### Future Migration Path (When Agent Teams Matures)

| Trigger | Migration Action |
|---------|-----------------|
| Agent Teams supports session resumption | Consider HANDOFF.md → shared task list |
| Sub-agent persistent memory stabilizes | Consider PROJECT_MEMORY → `memory: project` auto-inject |
| Token cost of multi-agent drops significantly | Large-scope US → agent team, small-scope → single session + skill |
| `requirePlanApproval` becomes reliable | Review Checkpoint → structured lead approval |

**Decision: No immediate changes. Current file-based approach is more stable and token-efficient. Record as strategic roadmap for future evaluation.**

**Status:** ✅ Recorded as strategic roadmap. No immediate action.

---

### FB-009: ISSUES-Driven Triage — From Bug List to Pipeline Re-entry

**Date:** 2026-02-26
**Context:** After completing Sprint 3 (US-001→010) on go-netagent, PROJECT_MEMORY.md's ISSUES section accumulated several unfixed items. The framework has no defined path for turning these ISSUES back into actionable work — the gap between "bug discovered" and "pipeline re-entry" is entirely manual and ad-hoc.

#### The Gap

ACF currently defines ISSUES as:
- **Scope guard** — "see a problem, check if it belongs to another US first, don't touch" (FB-002)
- **Blocker record** — max_attempts exceeded → write to ISSUES (Lifecycle)
- **Cleanup target** — resolved ISSUES cleared when Story completes (Lifecycle)

What ACF does NOT define:
- How unfixed ISSUES drive new work
- How to re-enter the pipeline from an ISSUES item
- Whether to reopen an existing US or create a new one
- Which pipeline step to roll back to

#### Observed Problem

After a sprint completes, the team has:
1. A `PROJECT_MEMORY.md` ISSUES section with unfixed items (some High, some Med)
2. A `review report` or `bug list` from testing / QA / field usage
3. No framework-defined path to turn these into pipeline work

Current workaround: human manually decides which US to reopen or create, manually runs `orchestrator start-story` or `rollback`. This breaks the "Macro-Agile × Micro-Waterfall" model because the macro-level feedback loop has no structure.

#### Proposed Flow: Review → Triage → Re-entry

The complete feedback cycle has three phases:

```
Human or orchestrator triggers review (any time)
        │
        ╔══════════════════════════════════════════════╗
        ║  Phase 1: REVIEW SESSION                     ║
        ║  CC freezes current state, audits project    ║
        ╚══════════════════════════════════════════════╝
        │
        ├── 1a. Code Review
        │     • Cross-US dependency check: do modules from different US integrate correctly?
        │     • Dead code / unused imports from removed features
        │     • Consistency: naming conventions, error handling patterns across US
        │
        ├── 1b. Spec-Code Coherence
        │     • BDD scenarios vs actual test coverage — any gaps?
        │     • SDD architecture vs actual code structure — any drift?
        │     • API contracts vs actual endpoints — any mismatches?
        │
        ├── 1c. Regression Check
        │     • Run full test suite (all levels: unit + integration + e2e)
        │     • Compare test counts: expected vs actual (from TESTS section)
        │     • Flag any tests that were passing before but now fail
        │
        ├── 1d. PROJECT_MEMORY Audit
        │     • ISSUES: are any marked "fixed" but actually not? Are there new issues?
        │     • SYNC: do file mappings still reflect reality after multi-US changes?
        │     • NEXT: is the priority order still relevant post-sprint?
        │
        └── Output: review-report.md (structured findings)
              → New/updated ISSUES written to PROJECT_MEMORY.md
              → Each ISSUE gets: severity, description, linked US (if identifiable)
        │
        ╔══════════════════════════════════════════════╗
        ║  Phase 2: TRIAGE                             ║
        ║  CC classifies each unfixed ISSUE            ║
        ╚══════════════════════════════════════════════╝
        │
        ├── Filter: status != fixed
        │
        ├── For each unfixed item:
        │     │
        │     ├── Has linked US (e.g. "linked: US-008")
        │     │     │
        │     │     ├── Determine rollback target:
        │     │     │     • Spec gap (missing scenario)     → rollback to bdd
        │     │     │     • Design flaw (wrong architecture) → rollback to sdd-delta
        │     │     │     • Implementation bug               → rollback to impl
        │     │     │
        │     │     └── Reopen US-008 at target step
        │     │
        │     └── No linked US
        │           │
        │           └── Create new US (next available ID)
        │                 → Full pipeline from bootstrap/bdd
        │                 → ISSUES item updated with linked US
        │
        └── Output: triage-plan (which US reopened, which created, rollback targets, priority)
        │
        ╔══════════════════════════════════════════════╗
        ║  Phase 3: RE-ENTRY                           ║
        ║  Pipeline resumes per triage decisions       ║
        ╚══════════════════════════════════════════════╝
        │
        ├── Reopened US: pipeline resumes from rollback target step
        │     → bdd → sdd → ... → done
        │     → Bug fix traced in original US's spec history
        │
        └── New US: full pipeline from bootstrap/bdd
              → Cross-cutting issues get their own US
```

#### Review Session Detail

The Review Session is an **on-demand health check**, not a fixed pipeline step. It can be triggered at any time — the orchestrator freezes the current project state and CC audits everything up to that point.

**Trigger scenarios:**

| When | Why |
|------|-----|
| Sprint complete (all US done) | Post-sprint retrospective, plan next sprint |
| Mid-sprint checkpoint | Verify cross-US integration before continuing |
| Single US just completed | Quick check for regressions or spec drift |
| Returning after a break | Understand current project health before resuming |
| Pre-release | Final quality gate before shipping |
| Human feels something is off | Ad-hoc health check |
| **Existing project, not yet using ACF** | **Reverse-engineer current state → produce ISSUES + review-report as Bootstrap input** |

The key insight: **Review is decoupled from the sprint lifecycle.** It operates on the current state of the project, whatever that state is. Some US may be done, some may be in-progress (paused for review), some may not have started yet. Review audits what exists.

**Review as ACF on-ramp for existing projects:**

An existing project that hasn't adopted ACF can use Review Session as its first contact with the framework. CC scans the codebase without any prior BDD/SDD/Memory context and produces:
- A review-report.md with findings (code quality, architecture issues, missing tests, tech debt)
- An ISSUES list derived from the review findings

This output becomes the input for two possible next steps:
1. **Adopt ACF** → the ISSUES list feeds directly into Bootstrap (create CLAUDE.md, SDD, Memory with ISSUES already populated) → then triage into US
2. **Don't adopt ACF** → the review-report.md is still a useful standalone artifact — a comprehensive codebase health check

This makes Review Session the **lowest-cost entry point** to ACF. No commitment to the full framework is required — just run `orchestrator review` on any project and get value immediately.

| Dimension | Verify (micro, per-US) | Review Session (macro, on-demand) |
|-----------|------------------------|-------------------------------------|
| Scope | Single US changes | All project changes since last review (or all time) |
| Checks | Completeness, correctness, coherence of one US | Cross-US integration, regression, spec drift, tech debt |
| Trigger | After impl, before commit | **Any time** — human or orchestrator initiated, **any project** (ACF or not) |
| Output | Pass/fail → commit or fix | review-report.md → ISSUES → triage (or Bootstrap) |
| Token cost | ~3K-6K (read US files) | ~10K-20K (varies with scope) |
| ACF required? | Yes (part of US pipeline) | **No** — works on any codebase, ACF adoption optional |

**Review Session works in all modes:** Full Mode projects get the full review + triage + re-entry cycle. Lite Mode or non-ACF projects get a standalone review-report.md + ISSUES list.

**Review Session checklist template:**

```markdown
## Sprint Review: Sprint {N}

### Code Review
- [ ] Cross-US module integration verified
- [ ] No dead code / unused imports from feature changes
- [ ] Naming and error handling consistency across US

### Spec-Code Coherence
- [ ] All BDD scenarios have corresponding tests
- [ ] SDD architecture matches actual code structure
- [ ] API contracts match actual endpoints

### Regression
- [ ] Full test suite passes (unit: X, intg: X, e2e: X)
- [ ] No regressions from previous sprint baseline
- [ ] Performance baselines maintained (if @perf tests exist)

### Security
- [ ] No hardcoded secrets across full repo (API keys, tokens, passwords, private keys)
- [ ] `.gitignore` covers secret file patterns (.env, *.key, credentials.json, *.pem)
- [ ] No credentials in logs, error messages, or API responses
- [ ] Test fixtures use mock values, not real credentials

### Memory Audit
- [ ] ISSUES section reflects current reality
- [ ] SYNC file mappings are accurate
- [ ] NEXT priorities updated for post-sprint context

### Findings
| # | Severity | Description | Linked US | Recommended Action |
|---|----------|-------------|-----------|-------------------|
```

#### Key Design Decisions (To Discuss)

**1. Who determines the rollback target?**

| Option | Pro | Con |
|--------|-----|-----|
| **A. CC decides** | Zero human intervention, fully autonomous | May misjudge — rollback too shallow (impl) when the real problem is spec (bdd) |
| **B. Human decides** | Accurate | Blocks the pipeline, defeats automation purpose |
| **C. CC proposes, human confirms** | Best of both worlds | Adds one round-trip latency |

**Leaning:** Option A with guardrails — CC decides, but if the reopened US fails verify again after fix, auto-escalate rollback one level deeper (impl → sdd-delta → bdd). This is consistent with the existing "reason-based routing" philosophy.

**2. ISSUES format: explicit linked US or CC infers?**

Current ISSUES format (from Templates.md):
```markdown
## ISSUES
- [High] 4 independent web apps, no shared state or navigation | status: open
```

Option A — Add explicit `linked` field:
```markdown
- [High] 4 independent web apps, no shared state | linked: US-008 | status: open
```

Option B — CC infers from context (reads history.md, BDD docs, git log):
```markdown
- [High] 4 independent web apps, no shared state | status: open
```
CC reads `.ai/history.md` → finds US-008 built the web apps → infers link.

**Leaning:** Option A for agent-written ISSUES (structured, zero ambiguity), Option B allowed for human-written ISSUES (humans won't always know the linked US). CC should attempt inference when `linked` is absent.

**3. Reopen semantics: what happens to the "done" US?**

When US-008 is reopened:
- STATE.json is overwritten with the reopened step (e.g. `step: bdd, status: pending`)
- Previous completion record stays in `.ai/history.md` (append-only, never deleted)
- A new entry is added to history: `US-008 reopened — reason: [ISSUES item description]`
- BDD/SDD/test files from the previous completion are preserved — CC modifies them, not rewrites

This is consistent with the "incremental not rewrite" principle.

**4. What about ISSUES that span multiple US?**

Example: "No shared navigation between 4 web apps" might touch US-003 (app A), US-005 (app B), US-008 (app C).

**Leaning:** Create a new US that references all related US. Don't reopen multiple US simultaneously — that breaks the single-story-at-a-time pipeline model. The new US's BDD should define the cross-cutting behavior, and its SDD delta can reference the existing modules.

**5. Review Session: autonomous or human-gated?**

| Option | Pro | Con |
|--------|-----|-----|
| **A. Fully autonomous** | CC runs review + triage + re-entry without stopping | May miss context that only human knows; could reopen wrong US |
| **B. Review auto, triage human-gated** | CC produces review report + triage plan, human approves before re-entry | One round-trip, but human sees the full picture before pipeline restarts |
| **C. All human-gated** | Every phase needs approval | Too slow, defeats automation purpose |

**Decision:** Option B with agent recommendations — Review Session runs autonomously (analysis only, no mutations), triage plan includes CC's **reasoned recommendations** (not just a list), human confirms before execution.

CC's triage plan should include for each ISSUE:
- **Recommended action:** reopen US-XXX at step Y / create new US
- **Rationale:** why this rollback target (e.g. "BDD for US-008 has no scenario for shared navigation — spec gap, not impl bug")
- **Impact estimate:** which files/modules will be affected, estimated scope
- **Priority suggestion:** recommended execution order with reasoning (e.g. "fix US-008 first — US-011 depends on its shared state module")

Human sees CC's reasoning, can override any decision, then approves the final plan.

The flow becomes:
```
CC runs Review Session autonomously
    → produces review-report.md + updates ISSUES
    → CC runs triage, outputs triage-plan with recommendations + rationale
    → Human reviews plan (sees CC's reasoning, can override)
    → Human approves → orchestrator executes triage plan
    → Pipeline re-entry begins
```

#### Impact Assessment (Token / Quality / Autonomy)

| Dimension | Impact |
|-----------|--------|
| **Token** | ⭐⭐ Saves tokens by routing bugs back to the correct spec level instead of ad-hoc fixes that miss root cause and require re-fixing. Review Session costs ~10-20K tokens but prevents multiple rounds of wrong-level fixes |
| **Quality** | ⭐⭐⭐ Review Session catches cross-US issues that per-US Verify misses (integration gaps, spec drift, regression). Bugs are fixed at the spec level (BDD/SDD), not just patched in code |
| **Autonomy** | ⭐⭐⭐ Removes the biggest remaining manual bottleneck: "sprint is done, now what?" CC can review, triage, and propose next actions autonomously — human only confirms |

**Verdict: Must-Do** (all three dimensions score ⭐⭐+)

#### Relationship to Existing Concepts

- **Verify step** (Lifecycle.md): Review Session is the macro-level equivalent — Verify checks one US, Review checks the whole sprint.
- **Reason-Based Routing** (Protocol.md): Already handles "failing → retry or route" within a running story. Triage extends this to completed stories.
- **Rollback** (Protocol.md v0.12): Already implemented in ACO. Reopen = rollback on a completed story.
- **Touch-it-test-it** (FB-R03): When reopening, Step 0 Safety Net Check applies — verify test coverage before modifying.
- **Macro-Agile** (Lifecycle.md): Review → Triage → Re-entry is the missing feedback loop that closes the macro-agile cycle: sprint → review → triage → next sprint.
- **Review Checkpoint** (Lifecycle.md): Triage plan human-gate is the sprint-level analogue of the per-US Review Checkpoint.

**Status:** ✅ All 5 design decisions confirmed. Incorporated into Lifecycle.md v0.7 + Protocol.md v0.13 + Templates.md v0.10.

---

### FB-010: Framework Migration — Versioned Adoption for Existing Projects

**Date:** 2026-02-27
**Context:** As ACF evolves (v0.6 → v0.7 Lifecycle, v0.12 → v0.13 Protocol, etc.), existing projects bootstrapped under earlier versions have no defined path to adopt new capabilities. go-netagent was bootstrapped before FB-009 (Review → Triage → Re-entry) existed — how does it start using those features?

#### The Gap

ACF defines how to bootstrap a new project and how to run the pipeline, but not how a project transitions when the framework itself changes. This is different from code migration — ACF is a set of conventions, not software with APIs. But conventions still evolve, and existing projects need a smooth path to benefit from new capabilities.

#### Design: Version Tag + Gradual Adoption + Backward Compatibility

**1. CLAUDE.md records ACF version**

Add to Agent Guidelines section:
```
ACF Version: 0.7
```

CC reads this to know which ACF capabilities the project was set up under. When CC reads a newer ACF spec, it compares versions and knows what's new for this project.

**2. Gradual adoption at natural touchpoints**

CC does NOT auto-upgrade existing projects. Instead, it proposes new features at natural moments:

| Touchpoint | What CC proposes |
|------------|-----------------|
| Session start | "ACF has new Review → Triage → Re-entry. Want me to explain what it adds?" |
| Story completion | "Your ISSUES could benefit from `linked: US-XXX` format for automated triage. Want me to add links to existing ISSUES?" |
| Review Session | During Memory Audit, CC backfills `linked` on ISSUES where it can infer the linked US from history.md + BDD/SDD |
| Triage | CC infers `linked` for any ISSUES that don't have it, as part of classification |

Human approves which features to adopt. No forced migration.

**3. Backward compatibility — nothing breaks**

| ACF change type | Impact on old projects |
|----------------|----------------------|
| Additive (new command like `review`) | Available when needed, ignored otherwise |
| Format extension (ISSUES `linked` field) | Old format still works; CC infers when `linked` is absent |
| New pipeline step (e.g. commit step v0.11) | CC follows new spec on next dispatch; no project-side change needed |
| Behavioral change (e.g. HANDOFF latest-entry-only) | CC adopts new behavior; old HANDOFF content preserved in history |

**4. CC backfills `linked` on ISSUES automatically**

When CC encounters ISSUES without `linked` — at Triage or Review Session — it reads `.ai/history.md`, BDD/SDD docs, and git log to infer the linked US. If inference is confident, CC adds the `linked` field directly. This is consistent with design decision #2 from FB-009 (CC infers for human-written ISSUES).

Backfill timing:
- **Triage:** always — CC must classify every ISSUE, so inference happens naturally
- **Review Session:** always — Memory Audit checks ISSUES accuracy, backfill is part of that
- **Session start:** optional — costs extra tokens, only if human opts in

#### Design Decisions

**1. No migration script — CC is the migration engine**

ACF is read by CC every session. When the spec changes, CC's behavior changes. The "migration" is CC reading the new spec and applying it. No external tooling needed.

**2. Version in CLAUDE.md, not in a separate file**

CLAUDE.md is already the project's configuration file for ACF (mode, team size). Adding version there is consistent. CC reads CLAUDE.md every session — zero extra cost.

**3. Human-gated adoption, not auto-upgrade**

Same philosophy as Triage (FB-009): CC recommends, human confirms. This prevents surprises when a project suddenly behaves differently because the framework updated.

#### Impact Assessment (Token / Quality / Autonomy)

| Dimension | Impact |
|-----------|--------|
| **Token** | ⭐ Minimal cost — one line in CLAUDE.md, version comparison is trivial |
| **Quality** | ⭐⭐ Existing projects get access to new quality mechanisms (Review, Triage) without starting over |
| **Autonomy** | ⭐⭐ CC can self-assess what's new and propose adoption — human doesn't need to read changelogs |

**Verdict: Worth-Doing** (two dimensions score ⭐⭐)

**Status:** ✅ Design confirmed. Ready to incorporate into Lifecycle.md + Templates.md.

---

### FB-011: Security Principle — Secrets Handling as a Framework Constraint

**Date:** 2026-02-27
**Context:** ACF has no guidance on how agents should handle secrets (API keys, tokens, credentials, connection strings). In practice, agents frequently encounter these during implementation — config files, environment setup, test fixtures, CI integration. Without a framework-level constraint, agents may hardcode secrets, commit `.env` files, or expose credentials in test data.

#### The Gap

Constitution defines 3-5 project principles, but security is not a default. Verify checks completeness/correctness/coherence but not security. Review Session checks code quality and spec drift but not credential exposure. Security is entirely left to the developer's memory.

#### Design: Three-Layer Security Integration

**Layer 1: Constitution — Default Security Principle (Bootstrap)**

Every project's Constitution includes a security principle by default. Template provides a starter set; teams can customize.

```markdown
## Security
- Never hardcode secrets (API keys, tokens, passwords, connection strings) in source code
- Use environment variables or secret management; document required vars in README
- Ensure .gitignore covers secret files (.env, *.key, credentials.json, *.pem) before first commit
- Test fixtures use fake/mock values, never real credentials
- If a secret is needed for implementation, add a placeholder with clear naming (e.g. `YOUR_API_KEY_HERE`)
```

**Layer 2: Verify — Security Check (Per-US)**

Extend Verify from three checks to four:

| Check Dimension | Content | Determination Method |
|-----------------|---------|---------------------|
| **Security** | No hardcoded secrets in committed files? `.gitignore` covers secret file patterns? Test fixtures use mock values? | **Semi-deterministic**: grep for common secret patterns (`password=`, `apikey=`, `token=`, `BEGIN RSA`), check `.gitignore` entries |

Action on failure: return to Implementation to fix. Same as Correctness — this is a hard gate, not a warning.

**Layer 3: Review Session — Security Scan (Cross-US)**

Add to Review Session's Code Review checklist:
- No secrets committed across any US (scan full repo, not just current diff)
- `.gitignore` still covers all secret patterns after multi-US changes
- No credentials leaked in logs, error messages, or API responses
- Dependencies with known vulnerabilities flagged (if tooling available)

#### Why Not a US?

A US produces a deliverable and completes. Security is not something you "finish" — it's a constraint that applies to every US. This is exactly what Constitution + Verify + Review are designed for: cross-cutting concerns that persist across the entire project lifecycle.

#### Design Decisions

**1. Constitution security is a default, not optional**

Unlike other Constitution principles which are project-specific (3-5 chosen by the team), the security principle is pre-populated in the template. Teams can modify the specifics but not remove the category entirely.

**2. Verify security check is semi-deterministic**

Pattern-based grep catches most common mistakes (hardcoded passwords, API keys, private keys). It won't catch everything (e.g. a secret disguised as a normal string), but it catches the 80% case at near-zero token cost. The remaining 20% is caught by Review Session's broader scan.

**3. Lite Mode still gets Constitution security**

Even Lite Mode projects benefit from the security principle. Since Lite Mode skips Verify's full triple-check, the Constitution text in CLAUDE.md serves as the primary guardrail — CC reads it every session and applies it during implementation.

#### Impact Assessment (Token / Quality / Autonomy)

| Dimension | Impact |
|-----------|--------|
| **Token** | ⭐ Near-zero cost — Constitution is a few lines, Verify grep is cheap, Review adds one checklist item |
| **Quality** | ⭐⭐⭐ Prevents the most common and dangerous agent mistake — committing secrets to version control |
| **Autonomy** | ⭐⭐ Agent self-checks for secrets without human needing to remember to ask |

**Verdict: Must-Do** (Quality ⭐⭐⭐ alone justifies it)

**Status:** ✅ Design confirmed. Ready to incorporate into Templates.md (Constitution) + Lifecycle.md (Verify + Review).

---

### FB-012: Spec-Embedded Scenarios — Behavior Specs Replace `.feature` Files

**Date:** 2026-06-11
**Context:** Field feedback from BDD-structured requirement-writing practice, plus a review of OpenSpec's spec-driven development model. ACF's BDD step produces standalone Gherkin files (`docs/bdd/US-{id}.feature`) per Story. Two structural issues surfaced: the `.feature` files have no consumer in ACF's actual loop, and per-Story scenario files never consolidate into a "current behavior" truth — unlike the SDD, which has a Delta → merge lifecycle.

#### The Gap

1. **`.feature` files have no consumer.** The framework scaffolds testify/Playwright/pytest tests manually from scenarios (Test Scaffolding step); no Gherkin runner (cucumber/behave/pytest-bdd) executes them, and reviewers read markdown. The `.feature` file is a behavior document in a different syntax — a middleman artifact.
2. **Scenarios have no stable IDs.** Traceability is a comment (`// Generated from: BDD US-XXX — <Scenario>`) — story-level only, not behavior-level, and not machine-checkable.
3. **No current-behavior truth.** `docs/bdd/` accumulates per-Story snapshots; after 20 Stories, answering "how does the system behave today?" means replaying all of them. The SDD solves exactly this with Delta → merge; behavior scenarios never got the same treatment.
4. **Lite Mode already proved `.feature` is droppable** — it writes BDD-style test names directly in code and works.

#### Design: OpenSpec-Style Behavior Specs with the Same Delta → Merge Lifecycle as the SDD

```
docs/specs/<capability>.md     # current behavior truth: Requirements + embedded Scenarios
docs/deltas/US-{id}.md         # per-Story delta: SDD delta + Behavior delta (ADDED/MODIFIED/REMOVED Requirements)
```

1. **Step 1 (BDD) produces a Behavior Delta, not a `.feature`:** ADDED / MODIFIED / REMOVED Requirements, each Requirement carrying its scenarios inline.
2. **Spec format (OpenSpec-style):**

```markdown
### Requirement: <short behavior statement> [R-<CAP>-NNN]
The system SHALL ...

#### Scenario: <branch label> (Test Level: integration)
- Given <precondition>
- When <trigger>
- Then <expected result>
```

3. **Stable behavior-level IDs.** One Requirement ID = one independently verifiable behavior = one test. Scaffolded tests carry a machine-readable header (`id`, `given/when/then`, `assertion_type`) instead of a free-text comment.
4. **Test-level tags become spec fields** (`Test Level: integration | component | e2e`); NFR tags (`@perf(PERF-01)`, `@secure(SEC-01)`) attach to the Scenario label.
5. **Unit-level scenarios exit the spec entirely.** Specs collect externally observable behavior only; unit-level GWT lives as test names in code (generalizes the Lite-mode fast path to Full Mode). Behavior documents must not describe implementation-internal behavior.
6. **Scenario Outline / Examples retired** — parameterized cases derive mechanically from the Parameters table (see FB-013) via table-driven tests / parametrize.
7. **Merge on Verify pass (Step 7):** the Behavior delta merges into `docs/specs/` at the same moment the SDD delta merges into the SDD. Specs are the single current truth; deltas archive as history.
8. **Gherkin becomes opt-in:** only when the project stack actually executes `.feature` (cucumber/behave/pytest-bdd). In that case `.feature` is a **test-layer artifact derived from the spec**; the spec remains the behavior truth.
9. **Verify Completeness check becomes ID-based:** every Requirement ID touched by the Story has a corresponding test — mechanically checkable, replacing "all BDD scenarios have tests".

#### Design Decisions

**1. Why Requirement + Scenario structure instead of bare scenario lists?**
The Requirement is the addressable unit — it carries the ID, appears in deltas, and maps to tests. A flat scenario list has nothing stable to reference when behavior changes across Stories.

**2. Why give behavior specs the SDD's merge lifecycle?**
Symmetry keeps the framework coherent: one delta per Story covering both architecture and behavior, one merge point, one answer to "what is current truth." This is the part of OpenSpec's model that per-Story `.feature` files structurally cannot replicate.

**3. ACF stays self-contained — no upstream-document dependency.**
Company- or domain-mandated requirement formats stay out of scope. If an upstream document exists, the Behavior Delta may cite it as a source, but ACF's pipeline reads and writes only its own specs. What is adopted here are format conventions, not a tool dependency — no OpenSpec CLI required.

**4. Migration**
`docs/bdd/` is retired from the project structure; existing `.feature` files are archived (not deleted — history matters). Adoption follows FB-010's versioned migration path at natural touchpoints.

#### Impact Assessment (Token / Quality / Autonomy)

| Dimension | Impact |
|-----------|--------|
| **Token** | ⭐⭐ One fewer artifact to write and keep in sync per Story; no GWT duplication; "current behavior" lookup is one file, not N snapshots |
| **Quality** | ⭐⭐⭐ Single source of truth for behavior; behavior-level traceability survives requirement churn |
| **Autonomy** | ⭐⭐ ID-based Completeness check is mechanically verifiable; agent self-checks coverage without human cross-reading two documents |

**Verdict: Must-Do**

**Status:** ✅ Incorporated (2026-06-11) into Framework v0.21, Lifecycle v0.10, Protocol v0.14, Templates v0.13, README, and Skill (SKILL.md + workflow.md + templates.md re-derived). `.feature` retired; specs self-contained with no upstream-document dependency; `docs/bdd/` → `docs/specs/`.

---

### FB-013: Requirement-Semantics Rules for Behavior Specs

**Date:** 2026-06-11
**Context:** Field feedback from BDD-structured requirement-writing practice surfaced requirement-semantics rules that ACF's BDD/Templates layer lacks. Without them, agents produce "fake BDD" for parameter-type stories, hand-fill boundary values into Examples tables, and leak API details into scenarios.

#### Items

**1. Scenario exemption rule.** Pure parameter/field/range requirements do not get forced GWT — a Parameters table + Error Cases suffice. The scenario field stays present with an explicit reason: `Not needed — <reason>`, or `Deferred — blocked by TBD-N`. Forcing GWT onto non-behavioral requirements produces scenarios with no test value.

**2. Parameters table as a first-class artifact.** Eight columns: Parameter / Type / Unit / Range / Default / Example / R/W / Notes. Key sub-rules:
- **Counter / Gauge / UpDownCounter typology** — Counter Range is `0 - (none)` with wrap/saturate behavior in Notes; Gauge Range is the real requirement/physical bound (e.g. `0-100` %, `-40-85` °C).
- **Unbounded notation** — never write type ceilings (`2^63-1`) as Range; they are not requirement constraints and boundary tests cannot validate them. Write `0 - (none)`.
- **usage/limit separation** — device-dependent ceilings split into `xxxUsage` (Range = `0 - (limit)`) and `xxxLimit` (actual device value), isolating device variance.
- **Type abstraction** — requirement-level categories only (`integer`, `number`, `string`, `boolean`, `enum`); OpenAPI `format` (int32, float…) never backfills into the spec.
- **Boundary tests derive mechanically** from Range / Error Cases via table-driven tests / parametrize. This **replaces Scenario Outline + Examples** (Templates v0.7 item 4): hand-filling boundary permutations into a requirement document is test-plan work and an anti-pattern at spec level.

**3. Answerable TBDs upgrade `[NEEDS CLARIFICATION]`.** Numbered `TBD-N`, phrased as a question the owner can actually answer (not "to be confirmed"). Distinguish from **disclosed assumptions**: when the source has a defensible hint, the agent extracts a candidate value and discloses it for challenge (see FB-014) instead of asking.

**4. No API details in scenarios.** Scenarios state behavior intent; endpoint, HTTP status, JSON field names belong to the API Contract step. Optionally one line `API Reference: METHOD /path (see openapi.yaml)` links requirement → endpoint for traceability — it adds no new test semantics.

**5. Event trigger discipline.** Event-type requirements must state: precise **Trigger** condition, explicit **NOT-Triggered** condition, and **message format + variables** with matching examples — not buried in a scenario `Then` clause.

#### Impact Assessment (Token / Quality / Autonomy)

| Dimension | Impact |
|-----------|--------|
| **Token** | ⭐⭐ Kills fake-BDD bloat and Examples-table hand-expansion; boundary cases generated, not authored |
| **Quality** | ⭐⭐⭐ Range/Default/boundary semantics become testable facts; event triggers become assertable |
| **Autonomy** | ⭐⭐ Agent decides AC-vs-Parameters mechanically; boundary expansion needs no human input |

**Verdict: Must-Do** (items 1–3); items 4–5 Worth-Doing alongside.

**Status:** ✅ Incorporated (2026-06-11) into Templates v0.13 (Behavior Spec writing principles, Parameters Table guide, Scenario Outline retirement) and Skill workflow.md Step 1 / templates.md.

---

### FB-014: Agent-First Disclosure — Self-Check and Assumptions Before Review Checkpoint

**Date:** 2026-06-11
**Context:** Field feedback from BDD-structured requirement-writing practice: when the agent self-checks its output and discloses its assumptions *before* requesting review, human review shifts from "find all bugs" to "challenge listed assumptions" — materially cheaper and more targeted. ACF's Review Checkpoint has only a Pending Clarification table; the agent runs no self-check before requesting review and discloses no assumptions.

#### Design

**1. Pre-review self-check (before the Review Checkpoint):**
- **Mechanical pass:** ID format and placement, template compliance, tag/Test-Level presence, no API details in scenarios (FB-013 item 4).
- **Semantic pass:** scenario executability (can each Given/When/Then become a test assertion?), boundary sanity (Ranges/Defaults make sense semantically, not just schema-complete), Error Case coverage (permission / invalid input / missing resource / concurrency), cross-Story conflict and redundancy, full coverage of the source Story.

**2. Review Checkpoint template gains three sections:**
- **Assumptions Made** — what the agent inferred and on what basis, listed for challenge.
- **Source Mapping** — which source items (Story description, referenced documents) were handled, partially handled, or deferred (with reason).
- **Cross-Story Conflict Scan** — redundancy, contradiction, undeclared dependencies against existing specs.

**3. Reviewer entry point becomes:** read Assumptions Made → TBD list → spot-check the spec body. Same philosophy as FB-009/FB-010: agent recommends and discloses, human confirms.

#### Impact Assessment (Token / Quality / Autonomy)

| Dimension | Impact |
|-----------|--------|
| **Token** | ⭐ A few lines per US; the self-check passes are checklist runs, not regeneration |
| **Quality** | ⭐⭐ Undisclosed assumptions are today's silent failure mode at Review |
| **Autonomy** | ⭐⭐⭐ Review round-trips drop; human attention goes only where the agent was uncertain |

**Verdict: Must-Do** (Autonomy ⭐⭐⭐ is the framework's core dimension)

**Status:** ✅ Incorporated (2026-06-11) into Templates v0.13 (Review Checkpoint template + Pre-Review Self-Check), Lifecycle v0.10 (Review Checkpoint row), and Skill workflow.md Step 4 / templates.md.

---

### FB-015: Delta Disposition — Archive-on-Merge Replaces "Archive or Delete"

**Date:** 2026-06-12
**Context:** FB-012 made the per-Story delta file (`docs/deltas/US-{id}.md`, Behavior Delta + SDD Delta) the BDD/SDD steps' working artifact, but left its post-merge disposition ambiguous: "archive in place or delete, project's choice."

#### The Gap

1. **State ambiguity.** A file at `docs/deltas/US-003.md` looks identical whether it is (a) the in-flight working draft of an active Story or (b) merged history from weeks ago. Tooling cannot treat file presence as a signal (the pre-dispatch check and rollback heuristic already try to), and an agent globbing `docs/deltas/` may misread a merged delta as pending work.
2. **Delete loses the only home of per-Story rationale.** SDD Delta MODIFIED sections carry `Reason:`/`Impact:`; Behavior Delta MODIFIED notes previous behavior. None of this merges — specs/SDD store current state only, git diff shows what changed but not why, ADRs cover only architecture-level decisions.
3. **Delete breaks mid-pipeline reopen.** `reopen --target scaffold|verify` steps list the active delta in `claude_reads`; deletion forces every reopen back to `bdd`.
4. **The `.feature` analogy does not transfer.** `.feature` was a *live* second copy with ongoing sync cost; a merged delta is *frozen* — zero maintenance, not auto-resent, in no future Story's `claude_reads`. The real cost is ambiguity, not storage.

#### Design: Archive-on-Merge (OpenSpec-style)

1. **Verify step, after the dual merge passes:** move `docs/deltas/US-{id}.md` → `docs/deltas/archive/{YYYY-MM-DD}-US-{id}.md`.
2. **Path encodes state:** the active path exists ⟺ the Story is in flight. Pre-dispatch file checks and the rollback heuristic become deterministic signals instead of heuristics; absence of an active delta for a completed Story is the expected state, not an error.
3. **Date prefix** handles reopen cycles: a US reopened at `bdd` produces a fresh active delta covering only the fix; on its merge, the second archive entry does not collide with the first.
4. **Delete remains a project-level option** for projects that fully trust git history; the default is archive.

#### Open Follow-Up

Post-merge reopen at steps that read the delta (`scaffold`, `verify`) should arguably read `docs/specs/` (the merged truth) rather than the old delta — "make code match spec" re-entry. This changes per-step `claude_reads` semantics in Protocol and is deferred; for now, reopen at those steps may consult `docs/deltas/archive/` read-only for context, or roll back to `bdd`.

#### Impact Assessment (Token / Quality / Autonomy)

| Dimension | Impact |
|-----------|--------|
| **Token** | ⭐ Prevents agents loading stale deltas as pending work; archive is cold (never auto-read) |
| **Quality** | ⭐⭐ Per-Story rationale preserved; active-vs-merged state unambiguous |
| **Autonomy** | ⭐⭐ File-presence checks (pre-dispatch, rollback suggestion) become reliable signals |

**Verdict: Worth-Doing** (two dimensions; incorporated immediately since the change is one move operation)

**Status:** ✅ Incorporated (2026-06-12) into Lifecycle v0.11, Protocol v0.15, Templates v0.14, and Skill (SKILL.md structure, workflow.md Step 7).

---

### FB-016: Review Disclosure Lives in the Delta; the Review Summary Is Ephemeral

**Date:** 2026-06-13
**Context:** FB-014 added the Review Checkpoint summary (Change Summary, Assumptions Made, Source Mapping, Cross-Story Conflict Scan, Pending Clarification, Review Conclusion). But — exactly like the pre-FB-015 delta — its *disposition* was never defined: Templates gives a template, workflow.md says "produce the Review summary", and Protocol's `review` step has `claude_writes: []`. Each agent improvises (print to chat, write `docs/review/US-XXX.md`, stuff it into HANDOFF), and any agent that writes a file creates a permanently stale snapshot.

Note: this is distinct from FB-009's on-demand `review-report.md`, which has a defined home (`.ai/`) and a defined consumer (triage). That artifact is fine. The gap is the per-Story Review *Checkpoint* summary.

#### The Gap — where each block belongs after review ends

| Summary block | Destination after review | Pre-FB-016 state |
|---------------|--------------------------|------------------|
| Change Summary (counts) | None — a view derived from the delta; discard | OK, nobody stored it |
| **Assumptions Made** | **The only block with durable value** — accepted assumptions are the *rationale* behind requirements; must persist | ✗ no home, evaporates at review end |
| Pending Clarification (TBD-N) | Answered → into delta/spec; unanswered → Memory ISSUES | OK, rule exists |
| Source Mapping | Deferred items → Memory NEXT; rest discard | ⚠ NEXT convention exists but unwritten |
| Cross-Story Conflict Scan | Fix delta now, or log to ISSUES | ⚠ same |
| Review Conclusion (sign-off) | Orchestrated → STATE.json review pass; manual → history.md session block | OK |

The decisive observation: **FB-015 already solved half of this.** Archive-on-merge gives every Story a frozen record; if the disclosure is written *into the delta*, it rides along to `docs/deltas/archive/` automatically — no separate review snapshot file is needed.

#### Design: disclosure is a delta section; summary is an assembled view

1. **The delta file gains a third top-level section** `## Review Disclosure — US-XXX` (Assumptions Made / Source Mapping / Cross-Story Conflict Scan), built incrementally: the `bdd` step records behavior-level assumptions, `sdd-delta` adds architecture assumptions and the conflict scan, and Step 4 finalizes it.
2. **The merge reads only `## Behavior Delta` and `## SDD Delta`; it explicitly skips `## Review Disclosure`.** Specs/SDD store current behavior and architecture, not the meta-rationale. The whole delta file (disclosure included) then moves to `docs/deltas/archive/` per FB-015 — so the rationale is preserved as frozen history, co-located with the change it explains.
3. **The Review Checkpoint summary becomes an ephemeral view**, assembled from the delta (Change Summary counts derived from it, Review Disclosure surfaced, Pending Clarifications collected from `[NEEDS CLARIFICATION]` markers) and presented in chat / the orchestrator message. It is **never written to a file** — no `docs/review/`, no `.ai/REVIEW.md`.
4. **Convergence rules at Step 4 close-out** (now written explicitly, per the table above): a challenged assumption → edit the delta to match and update its Review Disclosure entry; an answered TBD → apply into the delta/spec and remove from Memory ISSUES; an unanswered TBD → stays in Memory ISSUES; a deferred Source Mapping item → Memory NEXT; a found conflict → fix the delta now or log to ISSUES.

Note the pre-review self-check (FB-014, mechanical + semantic passes) stays ephemeral — those are *checks*, not artifacts. Only the disclosure (Assumptions / Source Mapping / Conflict Scan) becomes a delta section.

#### Considered and Rejected

- **Keep summary as a file for team audit (Team Size N):** real teams carry sign-off in PR review; STATE.json (orchestrated) and history.md (manual) already record the gate. A standalone review file would re-stale immediately.
- **Merge the disclosure into specs:** specs are current-behavior truth; assumptions are meta. Mixing them pollutes the spec. The archived delta is the correct home (same reasoning as keeping `Reason:`/`Impact:` out of the merged SDD — FB-015).

#### Impact Assessment (Token / Quality / Autonomy)

| Dimension | Impact |
|-----------|--------|
| **Token** | ⭐ No second artifact; summary is assembled on demand, never stored or re-read |
| **Quality** | ⭐⭐ Requirement rationale (accepted assumptions) is preserved with the change, not lost at review end; no stale review snapshots |
| **Autonomy** | ⭐⭐ Disposition is fully specified — the agent stops improvising where the summary goes |

**Verdict: Worth-Doing** (Quality + Autonomy)

**Status:** ✅ Incorporated (2026-06-13) into Lifecycle v0.12, Protocol v0.16, Templates v0.15, and Skill (workflow.md Steps 1/2/4/7, templates.md).

---

## Future Notes

Items identified as potential improvements but not yet prioritized for design or implementation.

| # | Topic | Description | Priority |
|---|-------|-------------|----------|
| FN-001 | **Metrics / Measurement** | Define KPIs for ACF effectiveness: token cost per US, retry rate, triage reopen ratio, regression rate across sprints. Data source: hook.log + STATE.json history. Purpose: continuous improvement of the framework itself | Low — need more field data first |
| FN-002 | **Estimation** | Complexity estimation at BDD stage (S/M/L) based on scenario count, module coupling, and history of similar US. Could inform sprint planning and token budget prediction | Low — useful but not blocking |
| FN-003 | **Cross-Project Learning** | Mechanism for patterns learned in one project (e.g. "WebRTC US needs deeper SDD") to transfer to new projects. Could be a shared knowledge base or agent memory that spans projects | Low — single-project workflow is solid first |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2026-02-13 | Initial version: Filtered 30 comparative suggestions down to 13 (8 Must-Do + 5 Worth-Doing) using Token/Quality/Autonomy dimensions |
| v0.2 | 2026-02-14 | Status update: All 13 items incorporated (8 Must-Do → Templates v0.7 + Lifecycle v0.2 + Protocol v0.1; 5 Worth-Doing → Templates v0.7); 4 "Not Included" items incorporated into Protocol v0.4 Multi-Executor collaboration mode |
| v0.3 | 2026-02-16 | Field Feedback: Added FB-R01~R04 from pilot project (US-001). FB-R01 (Full/Lite mode) finalized; FB-R02 (token optimization) and FB-R03 (bootstrap strategy) pending discussion |
| v0.4 | 2026-02-16 | FB-R02 (Token cost optimization) finalized: PROJECT_MEMORY slim-down (DONE/LOG → .ai/history.md) + HANDOFF latest-entry-only + history archive |
| v0.5 | 2026-02-16 | FB-R03 (Bootstrap strategy) finalized: Characterization tests → Step 0 per-Story pre-check ("touch it, test it"), not one-time big-bang |
| v0.6 | 2026-02-16 | FB-R01~R03 incorporated into Skill (SKILL.md, workflow.md, templates.md). All field feedback items translated to English |
| v0.7 | 2026-02-16 | FB-R01 expanded: Lite mode retains minimal PROJECT_MEMORY (NOW+NEXT); Lite as on-ramp to Full (scenario table); mode switching mechanism (verbal + CLAUDE.md edit); Upgrade Checklist + Downgrade procedure; agent must acknowledge and inform on mode switch |
| v0.8 | 2026-02-17 | FB-R05~R07 incorporated into Skill. FB-007/FB-008 summary recorded |
| v0.9 | 2026-02-17 | FB-007 expanded: full ROI tables (high/low elements), token consumption analysis (53% saving, 42% overhead ratio), applicability conclusions, 6 core learnings. FB-008 expanded: full concept mapping table, upgrade directions (sub-agent split, persistent memory, agent team for large US), future migration path triggers table |
| v0.10 | 2026-02-26 | FB-009: ISSUES-Driven Triage — Review → Triage → Re-entry flow for turning unfixed ISSUES into pipeline work (reopen linked US or create new US), 6 design decisions confirmed, Review Session as on-demand health check and ACF on-ramp for existing projects |
| v0.11 | 2026-02-27 | FB-010: Framework Migration — version tag in CLAUDE.md, gradual adoption at natural touchpoints, backward compatibility, CC backfills `linked` on ISSUES automatically. Future Notes section added: FN-001 (Metrics), FN-002 (Estimation), FN-003 (Cross-Project Learning) |
| v0.12 | 2026-02-27 | FB-011: Security Principle — three-layer security integration: Constitution default security principle (Bootstrap), Verify fourth check dimension (per-US), Review Session security scan (cross-US). Default in all modes including Lite |
| v0.13 | 2026-06-11 | FB-012~014 (field feedback from BDD requirement-writing practice + OpenSpec model review): FB-012 OpenSpec-style Behavior Specs replace `.feature` (Requirement/Scenario format with behavior-level IDs, Delta → merge lifecycle mirroring SDD, Gherkin demoted to opt-in, ID-based Completeness check); FB-013 requirement-semantics rules (Parameters table + Counter/Gauge typology, scenario exemption, answerable TBD-N, no API in scenarios, event trigger discipline, Scenario Outline retirement); FB-014 agent-first disclosure (mechanical+semantic self-check, Assumptions/Source Mapping/Conflict Scan in Review Checkpoint). Direction confirmed; incorporation pending |
| v0.14 | 2026-06-11 | FB-012~014 incorporated: Framework v0.21, Lifecycle v0.10, Protocol v0.14, Templates v0.13, README project structure; Skill re-derived (SKILL.md, workflow.md, templates.md) with new derivation line. FB-012 status note: ACF stays self-contained — no upstream requirement-document dependency; OpenSpec-style format conventions only, no tool dependency |
| v0.15 | 2026-06-12 | FB-015: delta disposition — archive-on-merge replaces "archive or delete"; Verify moves the active delta to `docs/deltas/archive/{date}-US-{id}.md` so path encodes in-flight vs merged state; rationale (Reason/Impact) preserved; delete remains project option; open follow-up recorded (post-merge reopen should read docs/specs/ instead of old delta). Incorporated into Lifecycle v0.11, Protocol v0.15, Templates v0.14, Skill |
| v0.16 | 2026-06-13 | FB-016: Review Disclosure (Assumptions Made / Source Mapping / Cross-Story Conflict Scan) becomes a third top-level section of the delta file, built incrementally and finalized at Review Checkpoint; merge skips it (rides to archive with the delta, FB-015); the Review Checkpoint summary is an ephemeral assembled view, never written to a file (distinct from FB-009's `.ai/review-report.md`); Step 4 close-out convergence rules made explicit. Incorporated into Lifecycle v0.12, Protocol v0.16, Templates v0.15, Skill |
