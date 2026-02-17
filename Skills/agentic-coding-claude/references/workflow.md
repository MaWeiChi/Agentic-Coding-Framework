# Executor Workflow Reference

Detailed step-by-step procedure for each phase of the micro-waterfall cycle. Read this
when you need specifics on what to read, produce, and check at each step.

---

## Bootstrap (One-Time)

**Goal:** Establish project context foundations for all subsequent Stories.

**Read:** Nothing yet (you're starting fresh)

**Full Mode — Produce:**
1. `PROJECT_CONTEXT.md` (or `CLAUDE.md`) — Why / Who / What + tech stack + project structure + `Agentic Coding Mode: full`
2. `docs/sdd/sdd.md` — Module division + data model skeleton + inter-module interfaces (at least function signatures and data structures)
3. `docs/constitution.md` — 3–5 inviolable architectural principles (RFC 2119 SHALL level)
4. `PROJECT_MEMORY.md` — Initial state (see Memory template — only hot sections: NOW/NEXT/TESTS/SYNC/ISSUES)
5. `.ai/history.md` — Empty file (will hold DONE, LOG, and session history)
6. `.ai/HANDOFF.md` — Empty file
7. Directory structure: `docs/bdd/`, `docs/deltas/`, `docs/api/`, `docs/ddd/` (if multi-domain)

**Lite Mode — Produce:**
1. `CLAUDE.md` — ≤10 lines: Why/What + tech stack + `Agentic Coding Mode: lite`
2. `PROJECT_MEMORY.md` — Minimal: NOW + NEXT only (~5 lines). Even one-off tasks
   benefit from this in case follow-up sessions occur.
3. Do NOT create `.ai/` files (HANDOFF.md, history.md) — these are Full Mode only.

**For existing projects** (Full Mode), Bootstrap = scan codebase → reverse-engineer
Project Summary + SDD → human corrects. Do NOT write characterization tests for all
existing code at this stage — use the Step 0 "touch it, test it" approach per Story instead.

---

## Per-Story Steps

### Step 0: Safety Net Check (Full Mode, Existing Codebases Only)

**Goal:** Ensure the code you're about to change has test coverage before you change it.

**Read:** PROJECT_MEMORY.md (NOW), BDD scenarios or Story description, source code of affected modules

**Produce:** Characterization tests for uncovered functions (if needed)

**Rules:**
- List the functions/modules this Story will modify
- Check if each has existing test coverage
- If no coverage → write a characterization test capturing current behavior (happy path + key edge cases)
- If coverage exists → skip, proceed to Step 1
- **Scope rule:** Only test the functions you're about to change. Don't test the entire module or unrelated functions.

This step is skipped in Lite Mode (tests are written directly without distinguishing characterization vs new).

---

### Step 1: BDD (Full Mode) / Write Tests Directly (Lite Mode)

**Lite Mode shortcut:** Skip Gherkin scenarios. Write test files directly from the Story
description. Use the same naming conventions (`Given_When_Then`) but go straight to code.
Then skip Steps 2–4 and jump to Step 5 (Test Scaffolding) or Step 6 (Implementation) if
tests are already written.

**Full Mode — Read:** PROJECT_CONTEXT.md, PROJECT_MEMORY.md (NOW + NEXT), existing SDD (affected modules), HANDOFF.md (if exists)

**Produce:** `docs/bdd/US-{id}.feature`

**Rules:**
- Write scenarios **only** for the current Story
- Use RFC 2119 language (SHALL / MUST / SHOULD / MAY)
- Tag each scenario with test levels: `@unit`, `@integration`, `@component`, `@e2e`
- For NFR-related scenarios, use ID-bearing tags: `@perf(PERF-01)`, `@secure(SEC-01)`
- Mark unclear requirements with `[NEEDS CLARIFICATION]`
- Use Scenario Outline for parameterized cases

**Template:**
```gherkin
@unit @component
Scenario: Short description of expected behavior
  Given [precondition]
  When [action]
  Then [expected result]

@perf(PERF-01)
Scenario Outline: Parameterized scenario
  Given <precondition>
  When <action> with <parameter>
  Then <expected_result>

  Examples:
    | precondition | parameter | expected_result |
    | ...          | ...       | ...             |
```

### Step 2: SDD Delta

**Read:** PROJECT_MEMORY.md, existing SDD, BDD scenarios for current Story, HANDOFF.md

**Produce:** `docs/deltas/US-{id}.md`

**Rules:**
- Output **Delta Spec** format: ADDED / MODIFIED / REMOVED sections
- Never rewrite the entire SDD
- Reference affected SDD modules by name
- If touching data model, ensure Source of Truth is clear (which module owns the data)
- Include Non-Goals / Out of Scope section

**Template:**
```markdown
# Delta Spec — US-{id}: {Story Title}

## ADDED
### Module: {ModuleName}
- **Purpose:** ...
- **Interface:** ...
- **Data model:** ...

## MODIFIED
### Module: {ExistingModuleName}
- **Change:** ...
- **Reason:** ...
- **Impact:** ...

## REMOVED
(Nothing removed in this Story)

## Non-Goals / Out of Scope
- ...
```

### Step 3: API Contract

**Read:** Existing SDD, Delta Spec, existing `docs/api/openapi.yaml`, HANDOFF.md

**Produce:** Updated `docs/api/openapi.yaml` (or `docs/api/asyncapi.yaml` for events)

**Rules:**
- Only add/modify affected endpoints or events
- Don't regenerate the entire contract
- Use OpenAPI 3.x for REST, AsyncAPI for WebSocket/MQTT/etc.

### Step 4: Review Checkpoint

**You don't produce anything here.** The human reviews BDD + Delta Spec + contract changes. Wait for human confirmation. If the human has modification requests, they'll come via HANDOFF.md's human_note or direct instruction.

If any `[NEEDS CLARIFICATION]` items exist, the human clarifies them at this point.

### Step 5: Test Scaffolding (Red)

**Read:** BDD scenarios (with tags), NFR table, API contracts, HANDOFF.md

**Produce:** Test file skeletons in `tests/` (all tests must fail)

**Rules:**
- Map BDD scenario tags to test levels:
  - `@unit` → unit test files
  - `@integration` → API integration test files
  - `@component` → Playwright component test files
  - `@e2e` → Playwright browser test files
  - `@perf(ID)` → look up NFR table for threshold, tool, scope
- Use project's test framework conventions as defined in PROJECT_CONTEXT.md
- All tests should fail at this point — no implementation code yet
- Extract helper function patterns early if multiple tests share setup

### Step 6: Implementation (Green)

**Read:** Failing test output, SDD, API contracts, BDD scenarios, HANDOFF.md

**Produce:** Source code that makes tests pass

**Rules:**
- Write minimal code to pass tests, then refactor
- Self-correction loop: run tests → fix → run again (max 3–5 attempts)
- After each iteration, run the project's configured linting tools
- If linting fails, fix before continuing
- Only modify affected files and functions (Diff-Only principle)
- Don't refactor unrelated code
- If stuck after max_attempts: record blocker in HANDOFF.md + Memory ISSUES, stop

### Step 7: Verify (Quality Gate)

**Read:** BDD scenarios, Delta Spec, SDD, API contracts, Constitution, test results, HANDOFF.md

**Produce:** Nothing (check only). If passing, proceed. If failing, return to relevant step.

**Three checks:**

| Check | What to Verify | On Failure |
|-------|---------------|-----------|
| **Completeness** | All BDD scenarios have tests? All ADDED items in Delta implemented? No unresolved `[NEEDS CLARIFICATION]`? | Return to the step that's incomplete |
| **Correctness** | All tests pass? NFR thresholds met? | Return to Implementation |
| **Coherence** | Main SDD merged with Delta? API contract matches implementation? Constitution not violated? | Fix the inconsistency |

After all three pass:

1. **Merge Delta into SDD** — Apply ADDED/MODIFIED/REMOVED from Delta Spec into the
   main `docs/sdd.md`. This is when the SDD becomes the single source of truth again.
2. **Archive Delta** — Keep `docs/deltas/US-{id}.md` as historical record.

### Step 8: Update Memory (Full Mode Only)

**Read:** PROJECT_MEMORY.md, git log, test results

**Produce:** Updated PROJECT_MEMORY.md + HANDOFF.md + `.ai/history.md` append

**PROJECT_MEMORY.md update rules (use minimal Edit, not full rewrite):**

| Section | Update |
|---------|--------|
| `<!-- -->` | Current commit hash |
| `NOW` | Clear or update to next Story |
| `TESTS` | Update pass counts per level |
| `NEXT` | Re-rank priorities |
| `ISSUES` | Append new issues, don't delete human-marked ones |
| `SYNC` | Update if module relationships changed |

**`.ai/history.md` append (DONE + LOG go here, not in Memory):**

Append one block. Format depends on whether the Story completed or the session was interrupted:

**Story completed:**
```markdown
## US-{id} {title} — {date}
status: complete
tests: unit:N intg:N comp:N
commit: {hash}
changes: [short list of files]
```

**Session interrupted (mid-Story):**
```markdown
## Session: US-{id} ({date})
status: in-progress
step: {current step}
summary: {what was accomplished}
unresolved: {what's stuck or incomplete}
next: {what the next session should pick up}
```

**HANDOFF.md (overwrite, latest-entry-only):**

Overwrite with YAML front matter (story, step, attempt, status, reason, files_changed,
tests) + markdown body (what was done, what's unresolved, what next session should note).

Lite Mode: skip this entire step. Commit message serves as the record.

---

## Mode Switching

Users can switch modes by editing CLAUDE.md or by verbal instruction. Lite mode is an
on-ramp to Full — projects often start Lite and upgrade when the Bootstrap cost is justified.

### Scenario Table

| Scenario | Mode | Rationale |
|----------|------|-----------|
| New project, 5+ stories planned | Full | Worth the upfront investment |
| Existing project, full framework adoption | Full | Bootstrap once, amortize over time |
| Existing project, urgent need to start NOW | Lite → upgrade to Full later | Ship first, build infrastructure later |
| Full project winding down, only small fixes left | Full → downgrade to Lite | Infrastructure overhead no longer justified |
| One-off bug fix or small feature | Lite | Will never need upgrade |

### Agent Behavior on Mode Switch

When the agent detects a mode change (reading CLAUDE.md or verbal instruction), it MUST:
1. Confirm the switch direction (Lite → Full or Full → Lite)
2. Explain which scenario from the table above matches the user's situation
3. Execute the corresponding transition

### Upgrade Checklist (Lite → Full)

```
1. ☐ Expand CLAUDE.md (add Why/Who/What, Project Structure, Development Conventions)
2. ☐ Expand PROJECT_MEMORY.md (add TESTS/SYNC/ISSUES to existing NOW/NEXT)
3. ☐ Create docs/sdd/sdd.md (scan codebase, reverse-engineer)
4. ☐ Create docs/constitution.md (3-5 core principles)
5. ☐ Create .ai/HANDOFF.md + .ai/history.md
6. ☐ Human confirms above outputs
```

### Downgrade (Full → Lite)

1. Update CLAUDE.md mode line to `lite`
2. Slim PROJECT_MEMORY to NOW + NEXT only (remove TESTS/SYNC/ISSUES)
3. Stop maintaining SDD, HANDOFF, Delta Spec, BDD
4. Existing docs remain (not deleted), just no longer actively maintained

---

## Session Startup Checklist

Every time you start a new session:

1. Read PROJECT_CONTEXT.md (or CLAUDE.md)
2. Read PROJECT_MEMORY.md
3. Compare git commit hash — if mismatch, sync Memory first
4. Read HANDOFF.md (if exists) for previous session context
5. Check what step you're on and continue from there

---

## Memory Conflict Resolution (Full Mode)

When Memory was edited by a human between sessions:

| Section | Authority | Your Action |
|---------|-----------|------------|
| `<!-- -->` | git (fact) | Update from git log |
| `NOW` | human intent | **Follow human's version** |
| `ISSUES` | mixed | Append new issues, don't delete human-marked ones |
| `TESTS` | CI / test results (fact) | Rerun and update |
| `SYNC` | human knowledge | **Append only**, never modify or delete |
| `NEXT` | human intent | **Follow human's ordering** |

Note: DONE and LOG now live in `.ai/history.md` and are not subject to conflict resolution
(they are append-only).

Core principle: fact-based sections follow git/tests, intent-based sections follow humans.
