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

## Field Feedback — WebRTC Project (FB-001~006)

Source: `go-webrtc/.ai/feedback.md` — Field observations after completing US-001 Room Isolation.

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

Real-world measurement from go-webrtc project:
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

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2026-02-13 | Initial version: Filtered 30 comparative suggestions down to 13 (8 Must-Do + 5 Worth-Doing) using Token/Quality/Autonomy dimensions |
| v0.2 | 2026-02-14 | Status update: All 13 items incorporated (8 Must-Do → Templates v0.7 + Lifecycle v0.2 + Protocol v0.1; 5 Worth-Doing → Templates v0.7); 4 "Not Included" items incorporated into Protocol v0.4 Multi-Executor collaboration mode |
| v0.3 | 2026-02-16 | Field Feedback: Added FB-R01~R04 from WebRTC project (go-webrtc US-001). FB-R01 (Full/Lite mode) finalized; FB-R02 (token optimization) and FB-R03 (bootstrap strategy) pending discussion |
| v0.4 | 2026-02-16 | FB-R02 (Token cost optimization) finalized: PROJECT_MEMORY slim-down (DONE/LOG → .ai/history.md) + HANDOFF latest-entry-only + history archive |
| v0.5 | 2026-02-16 | FB-R03 (Bootstrap strategy) finalized: Characterization tests → Step 0 per-Story pre-check ("touch it, test it"), not one-time big-bang |
| v0.6 | 2026-02-16 | FB-R01~R03 incorporated into Skill (SKILL.md, workflow.md, templates.md). All field feedback items translated to English |
| v0.7 | 2026-02-16 | FB-R01 expanded: Lite mode retains minimal PROJECT_MEMORY (NOW+NEXT); Lite as on-ramp to Full (scenario table); mode switching mechanism (verbal + CLAUDE.md edit); Upgrade Checklist + Downgrade procedure; agent must acknowledge and inform on mode switch |
| v0.8 | 2026-02-17 | FB-R05~R07 incorporated into Skill. FB-007/FB-008 summary recorded |
| v0.9 | 2026-02-17 | FB-007 expanded: full ROI tables (high/low elements), token consumption analysis (53% saving, 42% overhead ratio), applicability conclusions, 6 core learnings. FB-008 expanded: full concept mapping table, upgrade directions (sub-agent split, persistent memory, agent team for large US), future migration path triggers table |
