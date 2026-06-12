# Executor Workflow Reference

> Derived from: Framework v0.21, Lifecycle v0.10, Protocol v0.14, Templates v0.13 (2026-06-11)

Detailed step-by-step procedure for each phase of the micro-waterfall cycle. Read this
when you need specifics on what to read, produce, and check at each step.

---

## Bootstrap (One-Time)

**Goal:** Establish project context foundations for all subsequent Stories.

**Read:** Nothing yet (you're starting fresh)

**Full Mode — Produce:**
1. `PROJECT_CONTEXT.md` (or `CLAUDE.md`) — Why / Who / What + tech stack + project structure + `Agentic Coding Mode: full` + `ACF Version: 0.9`
2. `docs/sdd/sdd.md` — Module division + data model skeleton + inter-module interfaces (at least function signatures and data structures)
3. `docs/constitution.md` — 3–5 inviolable architectural principles (RFC 2119 SHALL level). **Must include a "No Hardcoded Secrets" principle by default** (API keys, tokens, passwords in env vars, `.gitignore` covers secret files, test fixtures use mock values)
4. `PROJECT_MEMORY.md` — Initial state (see Memory template — only hot sections: NOW/NEXT/TESTS/SYNC/ISSUES)
5. `.ai/history.md` — Empty file (will hold DONE, LOG, and session history)
6. `.ai/HANDOFF.md` — Empty file
7. Directory structure: `docs/specs/`, `docs/deltas/`, `docs/api/`, `docs/ddd/` (if multi-domain)

**Lite Mode — Produce:**
1. `CLAUDE.md` — ≤10 lines: Why/What + tech stack + `Agentic Coding Mode: lite` + `ACF Version: 0.9`
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

**Read:** PROJECT_MEMORY.md (NOW), Behavior Delta or Story description, source code of affected modules

**Produce:** Characterization tests for uncovered functions (if needed)

**Rules:**
- List the functions/modules this Story will modify
- Check if each has existing test coverage
- If no coverage → write a characterization test capturing current behavior (happy path + key edge cases)
- If coverage exists → skip, proceed to Step 1
- **Scope rule:** Only test the functions you're about to change. Don't test the entire module or unrelated functions.

This step is skipped in Lite Mode (tests are written directly without distinguishing characterization vs new).

---

### Step 1: BDD — Behavior Delta (Full Mode) / Write Tests Directly (Lite Mode)

**Lite Mode fast path:** Skip the Behavior Delta entirely — no separate behavior
document. Write test files directly from the Story description using BDD-style function
names (`Given_When_Then`). Then skip Steps 2–4 (SDD Delta, API Contract, Review
Checkpoint) and jump straight to Step 5 (Test Scaffolding) or Step 6 (Implementation)
if tests are already written. Constitution and NFR checks are also skipped in Lite Mode.

**Full Mode — Read:** PROJECT_CONTEXT.md, PROJECT_MEMORY.md (NOW + NEXT), existing Behavior Specs in `docs/specs/` (affected capabilities), existing SDD (affected modules), HANDOFF.md (if exists)

**Produce:** the **Behavior Delta** section of `docs/deltas/US-{id}.md` (ADDED / MODIFIED / REMOVED Requirements with embedded scenarios). No `.feature` file — Gherkin is opt-in only when the project stack actually executes it (cucumber/behave/pytest-bdd), and then it is a test-layer artifact derived from the spec.

**Rules:**
- Write Requirements **only** for the current Story; specs collect **externally observable behavior** — unit-level GWT lives as test names in code, not here
- One Requirement ID (`[R-<CAP>-NNN]`) = one independently verifiable behavior = one test; IDs are stable across Stories
- Use RFC 2119 language (SHALL / MUST / SHOULD / MAY)
- Every scenario carries a `Test Level` field: `integration`, `component`, or `e2e` (no `unit` at spec scope)
- For NFR-related scenarios, attach ID-bearing tags to the Scenario label: `@perf(PERF-01)`, `@secure(SEC-01)`
- Label scenarios by product-semantic branches (enabled/disabled, DHCP/Static), not boundary permutations — boundary values go in the **Parameters table** and expand into table-driven tests
- **Scenario exemption:** pure parameter/field/range requirements need no GWT — Parameters table + Error Cases suffice; write `Scenarios: Not needed — <reason>`
- No API details (endpoints, status codes, JSON field names) in scenarios — those belong to Step 3
- Event-type requirements state precise **Trigger**, **NOT-Triggered** condition, and message format + variables
- Mark unclear requirements with `[NEEDS CLARIFICATION: TBD-N — <answerable question>]`; when the source gives a defensible hint, extract a candidate and disclose it as an assumption at Step 4 instead of asking

**Template:**
```markdown
## Behavior Delta — US-{id}: {Story Title}

### ADDED Requirements

### Requirement: {short behavior statement} [R-{CAP}-{NNN}]
The system SHALL {behavior}.

#### Scenario: {branch label} (Test Level: integration)
- Given {precondition}
- When {action}
- Then {expected result}

#### Scenario: {other branch} (Test Level: e2e) @perf(PERF-01)
- Given {precondition}
- When {action}
- Then {expected result}

**Parameters**: (only if configurable values exist)
| Parameter | Type | Unit | Range | Default | Example | R/W | Notes |
|-----------|------|------|-------|---------|---------|-----|-------|

**Error Cases**: {invalid input / permission / missing resource / concurrency}

### MODIFIED Requirements
{Restate the full updated Requirement block; note previous behavior in one line}

### REMOVED Requirements
- [R-{CAP}-{NNN}] {reason}
```

See `references/templates.md` for the Parameters table rules (Counter/Gauge typology,
`0 - (none)` notation, usage/limit separation).

### Step 2: SDD Delta

**Read:** PROJECT_MEMORY.md, existing SDD, the Behavior Delta for current Story, HANDOFF.md

**Produce:** the **SDD Delta** section appended to `docs/deltas/US-{id}.md` (same file as the Behavior Delta)

**Rules:**
- Output **Delta Spec** format: ADDED / MODIFIED / REMOVED sections
- Never rewrite the entire SDD
- Reference affected SDD modules by name
- If touching data model, ensure Source of Truth is clear (which module owns the data)
- Include Non-Goals / Out of Scope section

**Template:**
```markdown
## SDD Delta — US-{id}: {Story Title}

### ADDED
#### Module: {ModuleName}
- **Purpose:** ...
- **Interface:** ...
- **Data model:** ...

### MODIFIED
#### Module: {ExistingModuleName}
- **Change:** ...
- **Reason:** ...
- **Impact:** ...

### REMOVED
(Nothing removed in this Story)

### Non-Goals / Out of Scope
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

**Before requesting review, run the pre-review self-check** (FB-014):
- **Mechanical pass:** Requirement ID format and placement, Behavior/SDD Delta template compliance, `Test Level` present on every scenario, no API details in scenarios
- **Semantic pass:** scenario executability (each Given/When/Then can become a test assertion), boundary sanity (Ranges/Defaults make sense semantically), Error Case coverage (permission / invalid input / missing resource / concurrency), cross-Story conflict against existing specs, full coverage of the source Story

**Then produce the Review summary** (see Review Checkpoint template in `references/templates.md`), disclosing:
- **Assumptions Made** — what you inferred and on what basis, listed for challenge
- **Source Mapping** — which source items were handled, partially handled, or deferred (with reason)
- **Cross-Story Conflict Scan** — redundancy, contradiction, undeclared dependencies

The human reviews the Behavior Delta + SDD Delta + contract changes, entering via
Assumptions Made → Pending Clarifications → spot-check. Wait for human confirmation.
If the human has modification requests, they'll come via HANDOFF.md's human_note or
direct instruction.

If any `[NEEDS CLARIFICATION]` items exist, the human clarifies them at this point.

### Step 5: Test Scaffolding (Red)

**Read:** Behavior Delta (scenarios with `Test Level` fields + Parameters tables), NFR table, API contracts, HANDOFF.md

**Produce:** Test file skeletons in `tests/` (all tests must fail)

**Rules:**
- Map scenario `Test Level` fields to test levels:
  - `integration` → API integration test files
  - `component` → Playwright component test files
  - `e2e` → Playwright browser test files
  - `@perf(ID)` / `@secure(ID)` → look up NFR table for threshold, tool, scope
- Parameters tables expand into table-driven tests (Range boundaries + Error Cases as cases; `assertion_type: parameter`)
- Unit tests are NOT scaffolded from the spec — they accompany implementation directly with BDD-style names
- Each test file opens with a machine-readable header: `Spec:` (Requirement ID + statement), `Scenario:` (branch label), `Test Level`, `assertion_type`
- Use project's test framework conventions as defined in PROJECT_CONTEXT.md
- All tests should fail at this point — no implementation code yet
- Extract helper function patterns early if multiple tests share setup

### Step 6: Implementation (Green)

**Read:** Failing test output, SDD, API contracts, Behavior Delta, HANDOFF.md

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

**Read:** `docs/deltas/US-{id}.md` (Behavior Delta + SDD Delta), `docs/specs/` (affected capabilities), SDD, API contracts, Constitution, test results, HANDOFF.md

**Produce:** Nothing until checks pass; then perform the merges below. If failing, return to relevant step.

**Four checks:**

| Check | What to Verify | On Failure |
|-------|---------------|-----------|
| **Completeness** | Every Requirement ID touched by the Story (Behavior Delta ADDED/MODIFIED) has a corresponding test, matched via `Spec:` headers (grep-checkable)? All ADDED items in the SDD Delta implemented? No unresolved `[NEEDS CLARIFICATION]`? | Return to the step that's incomplete |
| **Correctness** | All tests pass? NFR thresholds met? | Return to Implementation |
| **Coherence** | Specs and main SDD merged with their Deltas? API contract matches implementation? Constitution not violated? | Fix the inconsistency |
| **Security** | No hardcoded secrets in committed files? `.gitignore` covers secret patterns (`.env`, `*.key`, `credentials.json`, `*.pem`)? Test fixtures use mock values? | Return to Implementation |

After all four pass:

1. **Merge Behavior Delta into specs** — Apply ADDED/MODIFIED/REMOVED Requirements into
   `docs/specs/<capability>.md`. Specs become the current behavior truth again.
2. **Merge SDD Delta into SDD** — Apply ADDED/MODIFIED/REMOVED into the main `docs/sdd.md`.
   Both merges happen at the same moment (FB-012).
3. **Archive Delta** — Keep `docs/deltas/US-{id}.md` as historical record.

### Step 8: Commit Changes

**Read:** PROJECT_MEMORY.md, HANDOFF.md

**Produce:** Git commit of all code changes. Record commit hash in HANDOFF.md.

- Stage and commit all code changes from this Story
- Use conventional commit message with story ID (e.g. `feat(US-013): implement cart discount engine`)
- Do NOT commit PROJECT_MEMORY.md or `.ai/history.md` — those are updated in the next step
- After committing, update HANDOFF.md front-matter: `commit_hash: <hash>`
- This solves the chicken-and-egg problem: Update Memory can now reference the correct hash

### Step 9: Update Memory (Full Mode Only)

**Read:** PROJECT_MEMORY.md, HANDOFF.md (commit_hash), test results

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

**Valid values (orchestrator strictly validates — wrong values break the auto pipeline):**

- `status`: `pass` / `failing` / `needs_human` (NOT `passing`, `passed`, `failed`, `fail`)
- `reason`: `null` / `constitution_violation` / `needs_clarification` / `nfr_missing` / `scope_warning` / `test_timeout` (NOT freeform text — put details in markdown body)

**Staleness scan** (after updating Memory, before ending session):

After completing the Story, scan Memory for stale content and warn the human:
- ISSUES that reference the just-completed Story → suggest removal: "US-{id} is done, these ISSUES may be resolved: ..."
- NEXT items that are now complete → suggest removal
- SYNC entries pointing to files/modules deleted or renamed during this Story → suggest update

This is the best moment for staleness detection — the agent has full context about what
changed. As always, **do not auto-modify** intent-based sections; only warn.

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
3. Stop maintaining SDD, HANDOFF, Delta Spec, Behavior Specs
4. Existing docs remain (not deleted), just no longer actively maintained

---

## Session Startup Checklist

Every time you start a new session:

1. Read PROJECT_CONTEXT.md (or CLAUDE.md)
2. Read PROJECT_MEMORY.md
3. Compare git commit hash — if mismatch, sync Memory first
4. **Staleness check** (Full Mode) — scan Memory for potentially outdated content:
   - If ISSUES contains items older than 2 sprints or referencing completed Stories → warn human: "These ISSUES may be stale: ..."
   - If NOW references a Story that is already merged to main → warn human: "NOW may be outdated"
   - If SYNC references modules/files that no longer exist in codebase → warn human: "SYNC entry may be stale: ..."
   - **Do not auto-modify** intent-based sections — only warn. Human decides what to clean up.
5. Read HANDOFF.md (if exists) for previous session context
6. Check what step you're on and continue from there

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
