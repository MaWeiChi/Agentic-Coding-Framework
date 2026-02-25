# Agentic Coding Lifecycle

**Iteration Mechanism, Testing Strategy, CI/CD Interface**

This document is a supplement to the [Agentic Coding Framework](Framework.md), explaining how the framework operates along the timeline.

---

## Related Documents

| Document | Content | When Agent Loads |
|----------|---------|-----------------|
| [Framework.md](Framework.md) | Framework core: layered definitions, core principles, workflow | Read every conversation |
| This document | Operation mechanism: iteration model, testing strategy, CI/CD interface | Load when planning iterations or setting up CI |
| [Templates.md](Templates.md) | Framework details: document templates per layer, writing guidelines, examples | Load when writing BDD/SDD/contracts/Memory |
| [Protocol.md](Protocol.md) | Communication protocol: state management and automation for orchestrator ↔ executor | Load when setting up automation flows or integrating orchestrator |

---

## Execution Granularity and Iteration Model

The framework's layering describes "what documents are needed and in what order," but doesn't explain how it works across multiple User Stories. Here we supplement the framework's temporal dimension.

### Macro-Agile × Micro-Waterfall

This framework adopts a two-level structure: **Between Stories is agile, within a Story is waterfall.**

Micro-waterfall refers to the strict sequential execution of steps within a single User Story (BDD → SDD incremental update → contract update → Review → TDD → Implementation). Sequentiality is an advantage at this granularity level—each step has clear inputs and outputs, and agents don't need to make ambiguous judgments.

Macro-agile refers to maintaining flexibility in story sequencing, prioritization, and requirement changes. You might discover after completing the third Story that the direction is wrong, cancel the fourth, and insert a new one. Each Story is an independent iteration unit, and micro-waterfall doesn't constrain macro-level flexibility.

This combination works for Agentic Coding because: the risk of traditional waterfall (wasting an entire project on the wrong direction) is compressed to a single Story's scope; simultaneously, the "clear input → clear output" pattern that agents excel at is fully utilized in micro-waterfall. Strategic decisions at the macro level (which Stories first, whether to pivot) are left to humans.

### Bootstrap (One-Time)

Bootstrap differs by mode:

**Full Mode:** Project summary (Why / Who / What), initial SDD skeleton, Constitution (3-5 principles), PROJECT_MEMORY (hot sections only: NOW/NEXT/TESTS/SYNC/ISSUES), `.ai/history.md` (empty), `.ai/HANDOFF.md` (empty), and directory structure. The Bootstrap phase should also define already-known inter-module interfaces (internal interfaces)—at least to the level of function signatures and data structures. This is a contract-first approach, allowing subsequent Stories to develop against interfaces and reducing coupling between Stories.

**Lite Mode:** CLAUDE.md (≤10 lines: Why/What + tech stack + `Agentic Coding Mode: lite`) and a minimal PROJECT_MEMORY (NOW + NEXT only, ~5 lines). That's it — no SDD, no HANDOFF, no Constitution.

For existing projects (Full Mode), Bootstrap corresponds to the "scan Codebase → reverse-generate documents → manual correction" workflow. **Do NOT write characterization tests for all existing code at this stage** — use the Step 0 "touch it, test it" approach per Story instead (see below).

### Step 0: Safety Net Check (Full Mode, Existing Codebases Only)

Before starting each Story's micro-waterfall, check whether the code about to be modified has test coverage. If not, add a characterization test for the specific functions being changed — not the entire module.

**Scope rule:** Only test the functions this Story will modify. Don't test the entire module or unrelated functions. This avoids spending an entire session on tests for modules that may never be changed.

Lite Mode skips this step — tests are written directly without distinguishing characterization vs new.

### Mode Switching

Users can switch modes (Lite ↔ Full) by editing CLAUDE.md or by verbal instruction. When the agent detects a mode change, it must:

1. Confirm the switch direction (Lite → Full or Full → Lite)
2. Explain which scenario fits from the scenario table in the [Framework Document](Framework.md)
3. Execute the corresponding transition

**Upgrade Checklist (Lite → Full):**
1. Expand CLAUDE.md (add Why/Who/What, Project Structure, Development Conventions)
2. Expand PROJECT_MEMORY.md (add TESTS/SYNC/ISSUES to existing NOW/NEXT)
3. Create `docs/sdd/sdd.md` (scan codebase, reverse-engineer)
4. Create `docs/constitution.md` (3-5 core principles)
5. Create `.ai/HANDOFF.md` + `.ai/history.md`
6. Human confirms above outputs

**Downgrade (Full → Lite):**
1. Update CLAUDE.md mode line to `lite`
2. Slim PROJECT_MEMORY to NOW + NEXT only
3. Stop maintaining SDD, HANDOFF, Delta Spec, BDD
4. Existing docs remain (not deleted), just no longer actively maintained

### Iterative Execution (One Cycle per User Story)

After Bootstrap is complete, each User Story enters one independent micro-waterfall cycle:

| Step | Description |
|------|-------------|
| Step 0 (Full Mode, existing codebases) | Safety Net Check: verify test coverage for functions being modified; add characterization tests if missing |
| BDD (Full Mode) / Write Tests Directly (Lite Mode) | Write behavior scenarios **only for the current Story** (use RFC 2119 language, mark `[NEEDS CLARIFICATION]`). Lite Mode: skip Gherkin, write test files directly, then skip to Implementation |
| SDD Incremental Update | Append or modify affected modules and architecture sections, output **Delta Spec** (ADDED/MODIFIED/REMOVED), don't rewrite the entire SDD |
| API Contract Incremental Update | Add or adjust affected endpoints / events, don't rewrite the entire contract |
| **Review Checkpoint** | **Human confirms current BDD + Delta Spec + contract differences + clarifies all `[NEEDS CLARIFICATION]`** |
| Test Scaffolding | Based on current BDD scenario tags, output corresponding test level scaffolding (red light) |
| Implementation | Implementation to pass tests → Refactor (includes self-correction loop, see below) |
| AST Linting | After each Implementation iteration, run syntax-level checks; failure does not enter Verify |
| Component Test | Validate front-end component behavior (Playwright component testing) |
| **Verify** | **Triple verification: completeness/correctness/coherence (see Verify step below)** |
| **Commit** | **Stage and commit code changes, record commit hash in HANDOFF.md (do NOT commit Memory/history)** |
| **Update Memory** | **Update PROJECT_MEMORY.md with correct commit hash from HANDOFF (see rules below)** |

### Handling Dependencies Between Stories

Dependencies between Stories fall into two types:

**Technical dependency**—Story B needs modules or data structures produced by Story A to start (e.g., "user login" must precede "personal profile"). This dependency is hard; schedule dependent Stories in order. Since interfaces are locked in Bootstrap, once the dependent Story is complete, subsequent Story SDD incremental updates typically require only minor adjustments.

**Functional dependency**—multiple Stories share certain modules but don't block each other (e.g., "product search" and "product favorites" both depend on product list component). These Stories can enter micro-waterfall in parallel; if their SDD incremental updates touch the same module, human confirms no conflicts at Review Checkpoint.

**Dependencies discovered during development**—while doing Story C, you discover it depends on a component from Story A. At this point, add the dependency to the SDD, assess whether to pause C and do A first, or define A's component interface (stub) first to let C continue. This is where macro-agile flexibility comes into play—Story ordering can be dynamically adjusted.

**Heuristic Rule:** Story splitting should favor vertical slicing (vertical slice, from UI to API to DB in one cut) rather than horizontal layering, which naturally reduces inter-Story dependencies. If the dependency chain exceeds two levels (A → B → C), revisit Story splitting or SDD module boundaries to ensure they're reasonable.

### Verify Step (After Implementation, Before Update Memory)

Verify is the quality gate for each Story's micro-waterfall, executed after all tests pass but before updating Memory. The agent automatically performs three checks:

| Check Dimension | Content | Determination Method | Action on Failure |
|-----------------|---------|---------------------|------------------|
| **Completeness** | Are all BDD scenarios covered by corresponding tests? Have all ADDED items in Delta Spec been implemented? Are there any unresolved `[NEEDS CLARIFICATION]` remaining? | **Semi-deterministic**: test existence can be confirmed by grep; "all implemented" requires LLM judgment | Return to corresponding step to complete |
| **Correctness** | Do all tests pass? Are NFR thresholds met? | **Deterministic**: `go test` / `npm test` exit code + numerical results from NFR tools | Return to Implementation to fix |
| **Coherence** | Has the main SDD file merged Delta Spec? Does the API contract match the implementation? Are Constitution principles violated? | **LLM-dependent**: executor needs to read multiple documents and compare semantic consistency | Fix inconsistencies |

**Significance of Determination Method Classification**: Deterministic checks (Correctness) can be automatically executed by hooks with zero LLM tokens; semi-deterministic and LLM-dependent checks (Completeness, Coherence) require executor session handling, consuming tokens. Orchestrator can run deterministic checks in the hook phase first, and only dispatch executor for Coherence checks after all pass, saving token costs on failures.

Verify is automatic checking by the agent, not human Review. If all three checks pass, proceed to Commit; if any check fails, return to the corresponding step to fix and re-run Verify.

### Implementation Self-Correction Loop and Recursion Limit

The self-correction loop during Implementation (write code → run tests → fix code → run tests again) iterates at most **N times** (recommended 3-5 times, configured in the Step rules table of the [Protocol document](Protocol.md) with `max_attempts`). When the limit is exceeded, the agent must:

1. Mark blocker to the `ISSUES` section of MEMORY
2. Record failed test names and attempted fix directions (write to HANDOFF.md)
3. Pause current Story, awaiting human intervention

This limit prevents agents from looping infinitely. If 3 attempts don't fix it, it usually means design issues (should return to SDD) or unclear requirements (should return to Review), not insufficient code quality.

### AST Linting Gate

After each Implementation iteration, before entering Verify, run syntax-level checks:

| Tech Stack | Linting Tool |
|------------|--------------|
| Go backend | `go vet` + `golangci-lint` |
| TypeScript frontend | `eslint` + `tsc --noEmit` |

Linting failure does not enter Verify; return directly to Implementation to fix. This saves an entire round compared to discovering it during Verify—syntax errors are the cheapest errors and should be caught at the earliest stage.

Linting tools are configured by each project in the Step rules table of the [Protocol document](Protocol.md) via the `post_check` field.

### Delta Spec Lifecycle

Delta Spec is the structured format for SDD incremental updates (ADDED / MODIFIED / REMOVED), with complete template in the SDD template section of the [Templates document](Templates.md).

The workflow in micro-waterfall:

1. **Output when updating SDD**: agent analyzes affected modules based on BDD scenarios and outputs Delta Spec
2. **Review at Review Checkpoint**: humans review Delta Spec (what changed) rather than entire SDD (what it looks like now)
3. **Merge during Verify step**: after confirming implementation is complete, Delta content is formally merged into the main SDD file
4. **Archive or delete**: after merging, Delta file moves to `docs/deltas/US-XXX.md` (traceable) or is directly deleted (saves space)

Projects using Change Folder isolation (medium to large, multi-agent collaboration) can place each Story's Delta Spec + corresponding tests in an independent folder `changes/US-XXX/`, merging back to main files after Review passes.

### PROJECT_MEMORY Update Timing and Rules

Memory updates are embedded in the micro-waterfall workflow, automatically executed by agents at specific times.

**Session startup (every conversation begins):**

1. Read PROJECT_MEMORY.md
2. Compare git commit hash (see Git Commit Verification mechanism in [Templates document](Templates.md))
3. If inconsistent, sync Memory first before starting work

**When Story completes (last step of micro-waterfall, Full Mode only):**

| Memory Section | Update Content |
|----------------|-----------------|
| `<!-- -->` | Update to current commit hash |
| `NOW` | Clear or update to next Story |
| `TESTS` | Update pass counts per level |
| `NEXT` | Re-rank priorities based on completion |
| `ISSUES` | Append new issues, don't delete human-marked ones |
| `SYNC` | Update if module relationships changed |

DONE and LOG no longer live in PROJECT_MEMORY — they are appended to `.ai/history.md`:

```markdown
## US-{id} {title} — {date}
status: complete
tests: unit:N intg:N comp:N
commit: {hash}
changes: [short list of files]
```

HANDOFF.md is overwritten with the latest session state (latest-entry-only). Historical session records are preserved in `.ai/history.md`.

Lite Mode: skip Memory update. Commit message serves as the record.

**When interrupted mid-session (abnormal session end or manual stop):**

Agent should, if possible, update the "current task" section of Memory before interruption, recording which step was reached and what problem caused the stall, allowing the next agent to continue (possibly a different tool).

**When humans manually edit (conflict resolution strategy):**

When agent starts next time and reads Memory, it may face two sources of differences simultaneously: git hash inconsistency (code has new commits) + Memory content modified by humans. Handle strategy by "section authority source":

| Section | Authority Source | Conflict Strategy |
|---------|------------------|------------------|
| `<!-- -->` | git (fact) | Agent follows `git log`, updates directly |
| `NOW` | human intent | **Human priority** — if human changed it, follow human |
| `ISSUES` | mixed | Agent can append newly discovered issues, doesn't delete human-marked ones |
| `TESTS` | CI / test results (fact) | Agent reruns tests after update |
| `SYNC` | human knowledge | **Human priority** — agent only appends, doesn't modify or delete |
| `NEXT` | human intent | **Human priority** — if human reordered, follow human ordering |

Note: DONE and LOG now live in `.ai/history.md` (append-only) and are not subject to conflict resolution.

Core principle: **Fact-based sections follow git/tests, intent-based sections follow humans.** Agent can always "append," but for human-edited content can only "append," never "overwrite" or "delete."

### Memory Cleanup Timing

With DONE and LOG moved to `.ai/history.md`, PROJECT_MEMORY.md is significantly leaner. Remaining cleanup:

| Trigger Condition | Cleanup Action |
|-------------------|-----------------|
| Resolved issues in `ISSUES` | Clear corresponding ISSUES entries when Story completes |
| End of sprint / milestone | Human-led full cleanup: re-evaluate NEXT priorities, remove stale SYNC entries |
| `.ai/history.md` grows very large | Human decides whether to archive older entries (this file is append-only by design) |

Cleanup principle: **Fact-based sections can be auto-cleaned (truncate by rule), intent-based sections can only be cleaned by humans.** Agent never proactively deletes content in `NOW`, `NEXT`, `SYNC`.

### Why "Incremental Update" Rather Than "Rewrite"

SDD and API contract are **living documents**; each Story only touches affected parts. This has two benefits:

- **Save tokens**: agent doesn't regenerate entire SDD each time, only reads existing content and appends differences.
- **Reduce risk**: avoids accidentally losing prior design decisions or trade-offs recorded in ADRs when rewriting.

Practically, this means the SDD file should have clear module boundary demarcation, making each incremental update's scope easy to define.

---

## Testing Strategy

### BDD Scenario Tagging

BDD scenarios should be tagged with test level markers (tags), allowing agents to automatically output corresponding test-level scaffolding during Test Scaffolding phase. One scenario can have multiple tags, meaning it needs validation at different levels.

Tags come in two syntaxes:

- **Simple tags** (`@unit`, `@e2e`): define test level, agent outputs test scaffolding by level.
- **ID-bearing tags** (`@perf(PERF-01)`, `@secure(SEC-01)`): simultaneously define test level and reference specific thresholds in NFR table. Agent looks up NFR table during Test Scaffolding to get threshold, tool, scope, and directly fills in test script.

```gherkin
@unit @component
Scenario: Show error message when user enters invalid email
  Given user is on the registration page
  When input "not-an-email" to email field
  Then display "Please enter a valid email address"

@e2e
Scenario: User completes full registration flow
  Given user is on homepage
  When click registration button
  And fill all required fields
  And submit form
  Then redirect to welcome page
  And receive confirmation email

@perf(PERF-02) @secure(SEC-01)
Scenario: Product search maintains response time under high concurrency
  Given system under load of 1000 concurrent users
  When send search requests simultaneously
  Then search results return normally without errors
```

Available tags: `@unit`, `@integration`, `@component`, `@e2e`, `@perf(<NFR-ID>)`, `@load(<NFR-ID>)`, `@secure(<NFR-ID>)`. Specific thresholds for ID-bearing tags are defined in the NFR document; the NFR table is the single source of truth (see NFR template in [Templates document](Templates.md)).

### Testing Pyramid

| Level | Scope | Timing | Tool |
|-------|-------|--------|------|
| Unit Test | Single function / module logic | Each Story TDD phase | Go: `testing` + `testify` |
| API Integration Test | Backend API contract validation | Each Story TDD phase | Go: `net/http/httptest` + `testify` |
| Component Test | Front-end component behavior (isolated) | After each Story Implementation | Playwright component testing |
| Performance / Load Test | Performance baseline validation | Stories marked `@perf` or milestones | k6, vegeta |
| Full E2E Test | Complete user flow (front-end + back-end) | Cross-Story milestones | Playwright browser testing |

### Test Timing and Micro-Waterfall Integration

Testing executes in two phases within micro-waterfall:

**TDD phase (within Story, fast loop):** Unit Test + API Integration Test. This is the agent's self-correction loop; runs with every implementation, feedback must be fast. Primarily backend-focused, doesn't depend on front-end environment. Agent sees `@unit` and `@integration` tagged BDD scenarios and outputs corresponding Go test scaffolding.

**After Implementation (within Story, front-end validation):** Component Test. Validates front-end component behavior for the Story, uses Playwright component testing for isolated execution, doesn't require full application environment. Agent sees `@component` tagged scenarios and outputs Playwright tests.

**Milestone (cross-Story):** Full E2E Test + Performance Test. After accumulating multiple related completed Stories, run unified Playwright full browser test and k6/vegeta stress test. This level requires both front-end and back-end to be ready, unsuitable for every Story. Scenarios marked `@e2e` and `@perf` execute at this phase.

### Relationship of Tests to Other Documents

Functional test standards come from BDD scenarios; performance test standards come from NFR document. As Stories accumulate, previously passing tests continue serving as regression protection—this is CI's responsibility, detailed further in the CI/CD section below.

---

## CI/CD and Framework Interface

This section defines CI/CD's relationship to other framework parts, not covering concrete pipeline implementation or deployment target configuration.

### CI: BDD Tag-Driven Automated Testing

CI is the execution engine of testing strategy. BDD scenario tags simultaneously drive two things: which tests the agent outputs during Test Scaffolding, and which tests CI runs and when.

| Trigger Event | Test Tags Executed | Corresponding Framework Phase |
|---------------|-------------------|------------------------------|
| PR / Push | `@unit` + `@integration` + `@component` | Micro-waterfall TDD + Component Test |
| Merge to main branch | Above + `@e2e` | Cross-Story milestone validation |
| Scheduled / Manual | `@perf` + `@load` | NFR validation |

CI simultaneously provides regression protection: as Stories accumulate, previously passing tests rerun with each PR, ensuring new Stories don't break existing functionality. This extends the agent self-correction loop—agent runs one round locally, CI runs another before merge ensuring no environment differences.

### CD: Agent's Trust Boundary

In this framework, CD's key isn't "how to deploy" (that's infrastructure-layer configuration), but where the agent's responsibilities end.

**Agent responsible through:** CI all green + Container image build successful + push to registry.

**Agent doesn't intervene:** Deployment from registry to target environment. Whether target is Docker on IoT, future K8s, or cloud service, it's all infrastructure layer.

This boundary's benefit: deployment target changes don't require framework modifications. Agent's output is always a container image that passes all tests; deployment method is infrastructure configuration.

### CD Differences in Different Project Types

Different project types (Go container service, WordPress CMS, Astro + WordPress headless, etc.) have vastly different deployment methods, unsuitable for framework-level unification. Recommend annotating deployment type in SDD, handling differences via project-level CI/CD configuration. The framework's first half (BDD → SDD → TDD → CI testing) is universal across all project types.

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2026-02-13 | Initial version: iteration model, testing strategy, CI/CD interface separated from Framework |
| v0.2 | 2026-02-13 | Added Implementation Self-Correction Loop recursion limit (3-5 times, mark blocker if exceeded); added AST Linting gate (after Implementation before Verify, with tech stack tool correspondence table); added AST Linting step to iteration table |
| v0.3 | 2026-02-13 | Applied Windsurf Review: added "Determination Method" column to Verify triple-check table, distinguishing deterministic/semi-deterministic/LLM-dependent checks (P0); added Memory cleanup timing and rules (P2) |
| v0.4 | 2026-02-16 | Field feedback: Bootstrap split into Full/Lite mode; add Step 0 Safety Net Check ("touch it, test it"); add mode switching with Upgrade Checklist/Downgrade; Memory update rules changed (DONE/LOG → .ai/history.md); conflict resolution and cleanup rules updated |
| v0.5 | 2026-02-25 | Add Commit step between Verify and Update Memory; Verify pass now proceeds to Commit instead of Update Memory; aligned with Protocol v0.11 |
