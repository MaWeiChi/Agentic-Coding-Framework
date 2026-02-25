# Agentic Coding Protocol

**Orchestrator × Executor Communication Protocol and Automation Process**

This document is the fourth core document of the [Agentic Coding Framework](Framework.md), defining how the orchestrator and executor communicate, how state is passed, and how steps advance automatically.

---

## Related Documents

| Document | Content | When Agent Loads |
|----------|---------|-----------------|
| [Framework.md](Framework.md) | Framework core: layered definitions, core principles, processes | Required reading every conversation |
| [Lifecycle.md](Lifecycle.md) | Operating mechanism: iteration model, testing strategy, CI/CD interface | Load when planning iterations or configuring CI |
| [Templates.md](Templates.md) | Framework details: document templates for each layer, writing guides, examples | Load when writing BDD/SDD/contracts/Memory |
| This document | Communication protocol: orchestrator ↔ executor state management and automation | Load when configuring automation or integrating orchestrator |
| [Protocol-Advanced.md](Protocol-Advanced.md) | Advanced: multi-executor collaboration, reference implementations (OpenClaw, Agent Teams) | Load only when setting up multi-executor or building custom orchestrator |

---

## Architecture Model: Orchestrator × Executor

The first three documents of the framework define "what to do" and "how to do it," but don't explain "who drives whom." When the development process is driven by an automated orchestrator, a clear communication protocol is needed.

### Role Distribution

| Role | Responsibility | What It Doesn't Do |
|------|-----------------|-------------------|
| **Orchestrator** | Understand human instructions, read STATE to determine next step, dispatch executor, report progress | Doesn't read project files, doesn't understand code, doesn't make design decisions |
| **Executor** | Read project files, write BDD/SDD/code/test, run tests, update Memory | Doesn't schedule, doesn't notify humans, doesn't judge "which Story to do next" |
| **Human** | Set priorities, Review, clarify requirements, handle blockers | Doesn't intervene in executor's specific implementation |

### Design Principle: Cheap Orchestration × Expensive Execution

The orchestrator's design goal is **zero reasoning, zero LLM tokens** (or minimal tokens). All decision logic is deterministic code—table lookup, comparison, template filling. The executor bears the main token cost, handling work that requires understanding.

Benefits of this model:

- **Predictable costs**: orchestrator overhead is fixed (code execution), executor overhead correlates with Story complexity
- **Don't waste high-capability models**: orchestrator doesn't need to understand code, doesn't waste expensive models' reasoning on "reading JSON, determining next step"
- **Fault isolation**: orchestrator and executor are independent sessions, one crash doesn't affect the other's state

---

## Progressive Adoption: From Manual to Fully Automatic

This protocol is designed for progressive adoption in three stages. You don't need to wait for full automation to start using it—in manual mode, all document outputs of the framework (BDD / SDD / TDD / DDD) already have value.

### Level 0: Human as Orchestrator (Available Today)

Simplest mode: you are the orchestrator. Through a communication channel (WhatsApp / Telegram / CLI), give OpenClaw each step's instruction, and OpenClaw simply forwards it to Claude Code for execution.

**Prerequisite:** The project's CLAUDE.md or PROJECT_CONTEXT.md references framework documents, so the executor knows what workflow to follow.

#### Starting a New Project

```
You: Help me set up a todo-app project using the agentic coding framework,
     Go backend + React frontend. Start with Bootstrap (project summary + SDD skeleton + Constitution)
```

Executor output:
- `PROJECT_CONTEXT.md` (Why / Who / What + tech stack + project structure)
- `docs/sdd.md` (module division + data model skeleton)
- `docs/constitution.md` (3-5 core architecture principles)
- `PROJECT_MEMORY.md` (initial state)
- Directory structure (`docs/bdd/`, `docs/deltas/`, `docs/api/`)

#### Adding Features to Existing Project

```
You: Add shopping cart feature to A project, start with BDD
```
→ executor reads PROJECT_MEMORY.md + SDD, produces `docs/bdd/US-007.md`

```
You: OK, continue with SDD Delta and contract
```
→ executor produces `docs/deltas/US-007.md` + updates `docs/api/openapi.yaml`

```
You: I reviewed it, continue with scaffold + impl
```
→ executor produces test skeleton (red) → writes code to make tests pass → refactors

```
You: Continue with verify + update memory
```
→ executor performs triple verification → updates PROJECT_MEMORY.md

#### Supplementing Specifications or Tests in Ongoing Project

```
You: A project's US-003 product list is missing DDD Glossary, please add it
```
→ executor reads SDD + BDD, produces `docs/ddd/glossary.md`

```
You: A project, add NFR: search API must be p95 < 200ms
```
→ executor updates `docs/nfr.md` (adds PERF-01) + adds `@perf(PERF-01)` tag to corresponding BDD

```
You: A project US-005 is missing integration test, add it
```
→ executor reads BDD scenarios + contracts, adds `@integration` level tests in Test Scaffolding

#### Level 0 Limitations

| You need to do | After full automation, orchestrator does |
|----------------|------------------------------------------|
| Remember which step each project is on | STATE.json automatically tracks |
| Decide when to move to next step | Step rules table auto-advances |
| Judge whether to retry or go back on failure | Reason-Based Routing automatically decides |
| Manually say "continue" | Orchestrator automatically dispatches next step |
| Remember switching between projects | Per-project STATE.json each independent |

### Level 1: Semi-Automatic (Requires STATE.json Adapter Implementation)

Executor completes and hook automatically writes STATE.json, but orchestrator doesn't auto-advance. You still manually say "continue," but orchestrator reads STATE.json to tell you where you left off, what's next, and how many times it failed.

**Required implementation:** hook → STATE.json adapter (≈ 100 lines)

### Level 2: Fully Automatic (Requires Orchestrator State Machine Implementation)

You only need to say "continue A," and the orchestrator automatically advances through each step of the micro-waterfall, pausing only at review checkpoints and blockers.

**Required implementation:** Orchestrator state machine (≈ 300 lines) + Step rules table loader (≈ 50 lines) + .ai/ initialization tool (≈ 100 lines) + Timeout Poller (≈ 50 lines)

**Timeout Polling**: Level 2 can't rely solely on passive hook waiting—if the executor crashes without triggering a hook, the orchestrator needs to actively detect it. Recommended to implement a poller:

```javascript
// Check every N seconds (recommended 30s)
function pollTimeout(project) {
  const state = readJSON(`${project}/.ai/STATE.json`);
  if (state.status !== 'running') return;

  const elapsed = (now() - state.dispatched_at) / 60000;
  const rules = STEP_RULES[state.step];

  if (elapsed > rules.timeout_min) {
    state.status = 'timeout';
    writeJSON(`${project}/.ai/STATE.json`, state);
    notify(user, `${state.story}'s ${state.step} timed out (${Math.round(elapsed)} minutes)`);
  }
}
```

### Token Budget Reference Table

The following is an estimated token budget for each step to help projects evaluate costs. Values are based on medium complexity Stories ([M], 3-8 files), and actual consumption correlates with Story complexity.

| Step | Executor Read Tokens | Executor Output Tokens | Notes |
|------|---------------------:|----------------------:|-------|
| bdd | ≈ 2,000-4,000 | ≈ 500-1,500 | Read Memory + Context, output scenarios |
| sdd-delta | ≈ 3,000-6,000 | ≈ 800-2,000 | Read BDD + existing SDD, output Delta |
| contract | ≈ 2,000-4,000 | ≈ 500-1,000 | Read Delta + existing contracts, update YAML |
| review | 0 | 0 | Human review, no executor tokens |
| scaffold | ≈ 2,000-4,000 | ≈ 1,000-3,000 | Read BDD + contracts, output test skeleton |
| impl | ≈ 4,000-10,000 | ≈ 2,000-8,000 | Highest consumption, includes iterations |
| verify | ≈ 3,000-6,000 | ≈ 200-500 | Read multiple files, compare, output minimal |
| commit | ≈ 500-1,000 | ≈ 100-300 | Stage + commit code, record hash in HANDOFF |
| update-memory | ≈ 1,000-2,000 | ≈ 200-500 | Read Memory + HANDOFF (commit_hash), update Memory |
| **Single Story Total** | | | **≈ 15,000-40,000 tokens** |

Orchestrator tokens (Gemini Flash or similar): approximately 100-200 tokens per interaction, about 5-10 interactions per Story, total ≈ 500-2,000 tokens.

Multi-Executor mode token estimates see "Multi-Executor Collaboration Mode → Token Cost Impact" section.

---

## Communication Protocol: Three Files

Orchestrator and executor don't communicate directly; instead, they exchange information through three files in the file system. This design decouples the protocol from any specific tool—as long as the orchestrator and executor can read/write these three files, they can cooperate. In Level 0 manual mode, STATE.json is not needed; the executor directly reads and writes project files.

```
{project_root}/
  .ai/
    STATE.json          ← Bidirectional: hook writes results, orchestrator writes instructions
    HANDOFF.md          ← Unidirectional: executor session → next session
  PROJECT_MEMORY.md     ← Executor's world (orchestrator doesn't touch)
```

### 1. STATE.json — Orchestrator's Work Order

Orchestrator only looks at this file. **Machine parsed, zero LLM tokens.**

```json
{
  "project": "cart-app",
  "story": "US-005",

  "step": "impl",
  "attempt": 2,
  "max_attempts": 5,
  "status": "failing",
  "reason": null,

  "dispatched_at": "2026-02-13T14:30:00Z",
  "completed_at": "2026-02-13T14:31:15Z",
  "timeout_min": 10,

  "tests": { "pass": 42, "fail": 2, "skip": 1 },
  "failing_tests": [
    "cart_test.go:TestApplyCoupon",
    "cart_test.go:TestRemoveExpired"
  ],
  "lint_pass": true,
  "files_changed": ["internal/cart/service.go"],

  "blocked_by": [],
  "human_note": null
}
```

#### Field Specifications

| Field | Type | Writer | Notes |
|-------|------|--------|-------|
| project | string | orchestrator | Project identifier |
| story | string | orchestrator | Current User Story ID |
| step | enum | orchestrator / hook | Current micro-waterfall step |
| attempt | int | orchestrator | Attempt count for current step |
| max_attempts | int | Step rules table | Maximum attempts |
| status | enum | hook | `pending` / `running` / `pass` / `failing` / `needs_human` / `timeout` |
| reason | string? | hook | Failure reason code (see Reason-Based Routing) |
| dispatched_at | ISO8601 | orchestrator | Dispatch timestamp |
| completed_at | ISO8601? | hook | Completion timestamp |
| timeout_min | int | Step rules table | Timeout minutes |
| tests | object? | hook | Test result summary |
| failing_tests | string[]? | hook | Names of failed tests |
| lint_pass | bool? | hook | Linting result |
| files_changed | string[]? | hook | Files modified in this run |
| blocked_by | string[]? | orchestrator | Story IDs that this Story depends on but aren't complete (e.g., `["US-003"]`) |
| human_note | string? | orchestrator | Human instruction (transcribed from communication channel) |

#### Valid step Values

`bdd` · `sdd-delta` · `contract` · `review` · `scaffold` · `impl` · `verify` · `commit` · `update-memory` · `done`

These steps correspond to the micro-waterfall loop in the [Lifecycle document](Lifecycle.md).

#### status State Machine

```
pending → running → pass → (orchestrator advances to next step)
                  → failing → (orchestrator retries or routes)
                  → timeout → (orchestrator notifies human)
                  → needs_human → (wait for human instruction)

Note: Steps with `treat_failing_as_pass: true` (scaffold) auto-normalize
"failing" → "pass" when no error reason is present. This handles the scaffold
semantic where RED (failing) tests are the expected, correct output.
```

#### Valid reason Values

`null` (general failure/success) · `constitution_violation` · `needs_clarification` · `nfr_missing` · `scope_warning` · `test_timeout`

### 2. HANDOFF.md — Executor-to-Executor Handoff Notes (Full Mode Only)

Written at the end of each executor session, read at the start of the next session. **Latest-entry-only: overwritten each time.** Historical session records are appended to `.ai/history.md` for archival. This keeps HANDOFF small (one block to read, one block to write) while preserving full session history.

#### Hybrid Format: Structured Header + Freeform Body

HANDOFF.md uses a **hybrid format design**. The first half is structured YAML front matter for machines to parse (zero LLM tokens); the second half is freeform markdown for the next executor session to read detailed context.

```markdown
---
story: US-005
step: impl
attempt: 2
status: failing
reason: null
files_changed:
  - internal/cart/service.go
  - internal/discount/engine.go
tests_pass: 42
tests_fail: 2
tests_skip: 1
---

# HANDOFF — US-005 impl attempt:2

## What was done this time
- Modified DiscountEngine.ApplyCoupon() to add coupon expiration check
- Unified timezone to UTC in CartService

## Not yet resolved
- TestApplyCoupon: expired coupon boundary conditions in UTC+8 not handled
- TestRemoveExpired: batch delete SQL WHERE clause needs to change from <= to <

## Next session should note
- Don't modify CartService.AddItem(), it's working fine
- Coupon expires_at in DB is UTC, frontend may send local time
```

#### YAML Front Matter Fields

| Field | Type | Reader | Notes |
|-------|------|--------|-------|
| story | string | hook / orchestrator | Current Story ID |
| step | enum | hook / orchestrator | Current step (same as STATE.json step) |
| attempt | int | hook / orchestrator | Attempt number |
| status | enum | hook | `pass` / `failing` / `needs_human` |
| reason | string? | hook | Failure reason code (same as STATE.json) |
| files_changed | string[] | hook / orchestrator | Files modified in this run |
| tests_pass / tests_fail / tests_skip | int | hook | Test result counts |

Hook parses YAML front matter to update STATE.json, **no need to grep the markdown body**. This solves the same problem that executor-result previously tried to solve—but HANDOFF.md itself now shoulders the responsibility of structured reporting, making an extra file unnecessary.

#### Relationship with executor-result

| Approach | Machine-Readable Part | Human/LLM-Readable Part | File Count |
|----------|----------------------|------------------------|-----------|
| HANDOFF.md (hybrid) | YAML front matter | Markdown body | 1 |
| executor-result + HANDOFF.md | executor-result | HANDOFF.md | 2 |

Both approaches work. The hybrid format's advantage is a single file and reduced executor output burden; the dual-file approach's advantage is better separation of concerns. Projects can choose based on preference; hooks should support both.

#### Why Separate File

| Consideration | HANDOFF.md | PROJECT_MEMORY.md |
|---------------|-----------|-------------------|
| Lifecycle | Each session overwrites | Long-term record for entire project |
| Granularity | Single step details | Story-level summary |
| Readers | hook (YAML) + next executor (body) | Any session startup context |
| Bloat risk | None (overwrites) | Yes (needs manual cleanup) |

### 3. PROJECT_MEMORY.md — Executor's World

Maintains the existing design in the [Templates document](Templates.md). Orchestrator doesn't touch this file. Only adjustment: remove state machine responsibility (handled by STATE.json), return to pure project context.

---

## Executor Output Rules

Executor output should follow the "minimal output, structure first" principle to reduce parsing cost for downstream (hook, orchestrator, next session).

### Output Categories and Format Requirements

| Output Category | Format | Output Strategy | Notes |
|-----------------|--------|-----------------|-------|
| **Documents** (BDD, Delta Spec, contracts) | Corresponding format (Gherkin / Markdown / YAML) | Write to path specified in `claude_writes` | git tracks diffs |
| **Code** | Source code | Write to path specified in `claude_writes` | git tracks diffs |
| **Status Report** | HANDOFF.md YAML front matter or executor-result | Structured, hook parses | Zero LLM token parsing |
| **Handoff Context** | HANDOFF.md markdown body | Freeform, next session reads | Describe what was done, what's stuck |

### Diff-Only Principle

When modifying existing files, **only modify affected paragraphs, don't rewrite entire files**. This embodies the framework's core principle of "incremental not rewrite" at the output layer.

| Step | Diff-Only Behavior | Anti-Pattern |
|------|-------------------|--------------|
| sdd-delta | Output independent Delta Spec file, don't modify main SDD | Rewrite entire SDD |
| contract | Only add/remove affected endpoints / channels | Regenerate entire openapi.yaml |
| impl | Only modify affected functions and files | Refactor unrelated code for "cleanliness" |
| update-memory | Only update changed sections | Rewrite entire PROJECT_MEMORY.md |
| verify (merge Delta) | Merge Delta's ADDED/MODIFIED/REMOVED into corresponding SDD sections | Use Delta content to overwrite entire SDD |

### Structure First

When executor outputs content consumed by **machines**, prioritize structured formats:

- API contracts: OpenAPI / AsyncAPI YAML (don't use markdown tables to describe APIs)
- Test results: JSON format (`go test -json`) → hook parses and writes to STATE.json
- Status report: HANDOFF.md YAML front matter or executor-result
- Delta Spec: Fixed ADDED / MODIFIED / REMOVED structure

When executor outputs content consumed by **humans/LLMs**, natural language is acceptable:

- HANDOFF.md body (handoff context)
- BDD scenario Given/When/Then (business language)
- SDD module descriptions (architecture explanation)

### Output Instructions in Dispatch Prompt

Each step's dispatch prompt should clearly tell executor the output requirements. Add to the end of existing `step_instruction`:

```
Output rules:
- Only modify affected files and paragraphs, don't rewrite unrelated content
- After completion, update .ai/HANDOFF.md (include YAML front matter)
- If touching Non-Goals scope, mark scope_warning in HANDOFF.md reason field
```

---

## Step Transition Rules Table

Orchestrator checks this table to decide the next step. **Deterministic, zero reasoning.**

```yaml
steps:
  bdd:
    next_on_pass: sdd-delta
    next_on_fail: bdd
    max_attempts: 3
    timeout_min: 5
    requires_human: false
    claude_reads:
      - PROJECT_CONTEXT.md      # Project summary
      - PROJECT_MEMORY.md       # NOW + NEXT
      - .ai/HANDOFF.md          # Previous handoff (if any)
    claude_writes:
      - docs/bdd/US-{story}.md
    post_check: null

  sdd-delta:
    next_on_pass: contract
    next_on_fail: sdd-delta
    max_attempts: 3
    timeout_min: 5
    requires_human: false
    claude_reads:
      - PROJECT_CONTEXT.md
      - PROJECT_MEMORY.md
      - docs/bdd/US-{story}.md   # Current BDD
      - docs/sdd.md               # Existing SDD (affected modules)
      - .ai/HANDOFF.md
    claude_writes:
      - docs/deltas/US-{story}.md

  contract:
    next_on_pass: review
    next_on_fail: contract
    max_attempts: 2
    timeout_min: 5
    requires_human: false
    claude_reads:
      - docs/sdd.md               # Affected modules
      - docs/deltas/US-{story}.md  # Current Delta
      - docs/api/openapi.yaml     # Existing contracts
      - .ai/HANDOFF.md
    claude_writes:
      - docs/api/openapi.yaml

  review:
    next_on_pass: scaffold
    on_fail:
      default: bdd                    # Wrong direction, back to BDD
      needs_clarification: bdd        # Requirement unclear → rewrite BDD
      constitution_violation: sdd-delta # Architecture issue → redesign
      scope_warning: sdd-delta         # Scope issue → adjust Delta
    requires_human: true          # orchestrator sends message, waits for human
    claude_reads: []              # executor doesn't participate
    claude_writes: []

  scaffold:
    next_on_pass: impl
    next_on_fail: scaffold
    max_attempts: 2
    timeout_min: 5
    requires_human: false
    treat_failing_as_pass: true  # RED stubs are expected; "failing" auto-normalizes to "pass"
    claude_reads:
      - docs/bdd/US-{story}.md    # Current BDD (with tags)
      - docs/nfr.md               # NFR thresholds
      - docs/api/openapi.yaml     # Contracts
      - .ai/HANDOFF.md
    claude_writes:
      - "*_test.go"
      - "*.spec.ts"

  impl:
    next_on_pass: verify
    on_fail:
      default: impl                    # Retry
      constitution_violation: sdd-delta # Architecture violation → back to design
      needs_clarification: review       # Need human
      scope_warning: review             # Touched Non-Goals
    max_attempts: 5
    timeout_min: 10
    requires_human: false
    claude_reads:
      - docs/sdd.md                # Affected modules
      - docs/api/openapi.yaml     # Contracts
      - .ai/HANDOFF.md            # Previous attempt's handoff
    claude_writes:
      - "*.go"
      - "*.ts"
    post_check: "go vet ./... && golangci-lint run"

  verify:
    next_on_pass: commit
    on_fail:
      default: impl                # Back to impl
    max_attempts: 2
    timeout_min: 5
    requires_human: false
    claude_reads:
      - docs/bdd/US-{story}.md
      - docs/deltas/US-{story}.md
      - docs/api/openapi.yaml
      - docs/constitution.md
      - .ai/HANDOFF.md
    claude_writes: []

  commit:
    next_on_pass: update-memory
    next_on_fail: commit
    max_attempts: 2
    timeout_min: 3
    requires_human: false
    claude_reads:
      - PROJECT_MEMORY.md
      - .ai/HANDOFF.md
    claude_writes: []              # Only git operations, no file writes
    # Stage and commit all code changes. Use conventional commit with story ID.
    # Do NOT commit PROJECT_MEMORY.md or .ai/history.md (updated in next step).
    # Record commit hash in HANDOFF.md front-matter as `commit_hash: <hash>`.

  update-memory:
    next_on_pass: done
    next_on_fail: update-memory
    max_attempts: 2
    timeout_min: 3
    requires_human: false
    claude_reads:
      - PROJECT_MEMORY.md
      - .ai/STATE.json            # Test results
      - .ai/HANDOFF.md            # commit_hash from commit step
    claude_writes:
      - PROJECT_MEMORY.md
      - .ai/history.md            # Append DONE + LOG entry
```

### Component Test Location

Component Test (Playwright component testing) is defined in the [Lifecycle document](Lifecycle.md) as a step after Implementation and before Verification. In the Step rules table, Component Test **is not a standalone step**—it's included in the `impl` step's `post_check` (for frontend projects) or as one of the `verify` step's Correctness checks.

Reason: Component Test execution timing differs from backend unit/integration tests (requires frontend components to be ready), but in automation workflows, it naturally follows impl completion. Projects can integrate `npx playwright test --project=ct` in `impl.post_check` for frontend projects.

### Relationship Between Rules Table and Lifecycle

The rule table's step sequence corresponds to the micro-waterfall loop in the [Lifecycle document](Lifecycle.md). The `claude_reads` field defines what files the executor should load at each step, corresponding to the Framework's "load on demand" principle. `post_check` corresponds to AST Linting integration in Lifecycle (`go vet` + `golangci-lint`); frontend projects can extend it to `eslint . && tsc --noEmit && npx playwright test --project=ct`.

### Custom Rules Table

Each project can override defaults in `.ai/step-rules.yaml`. Common customization scenarios:

- Frontend project's `post_check` changes to `eslint . && tsc --noEmit`
- Simple CRUD project reduces `max_attempts`
- High-security project adds security scan to `verify`

---

## Dispatch Logic

After receiving human instruction, the orchestrator executes the following deterministic logic. **Zero LLM tokens—pure code.**

```javascript
function dispatch(project) {
  const state = readJSON(`${project}/.ai/STATE.json`);
  const rules = STEP_RULES[state.step];

  // Timeout check
  if (state.status === 'running') {
    const elapsed = (now() - state.dispatched_at) / 60000;
    if (elapsed > rules.timeout_min) {
      state.status = 'timeout';
      notify(user, `${state.story}'s ${state.step} timed out`);
      return;
    }
    notify(user, `${state.story} is still running (${state.step})`);
    return;
  }

  // Need human
  if (rules.requires_human && state.status !== 'pass') {
    state.status = 'needs_human';
    notify(user, formatReviewRequest(state));
    return;
  }

  // Success → next step
  if (state.status === 'pass') {
    state.step = rules.next_on_pass;
    state.attempt = 1;
    state.status = 'pending';
    state.human_note = null;
  }
  // Failure → retry or route
  else if (state.status === 'failing') {
    if (state.attempt >= rules.max_attempts) {
      notify(user, `${state.story} stuck at ${state.step} (${state.attempt} attempts)`);
      return;
    }
    // reason-based routing
    const nextStep = rules.on_fail?.[state.reason]
                  ?? rules.on_fail?.default
                  ?? state.step;
    if (nextStep !== state.step) {
      state.step = nextStep;
      state.attempt = 1;
    } else {
      state.attempt++;
    }
  }

  // Assemble dispatch prompt (template filling, zero LLM)
  const prompt = buildPrompt(state, rules);

  // Update STATE and dispatch
  state.status = 'running';
  state.dispatched_at = now();
  state.completed_at = null;
  writeJSON(`${project}/.ai/STATE.json`, state);

  dispatchExecutor(project, prompt);
}
```

---

## Dispatch Prompt Template

Each step's prompt is template filling, the orchestrator doesn't need to improvise.

```
You are executing step {step_display_name} for {story}.
{if attempt > 1}(Attempt {attempt} of {max_attempts}){endif}

Please read the following files in order:
{for file in claude_reads}
- {file}
{endfor}

{if human_note}
=== Human Instruction ===
{human_note}
==========================
{endif}

{step_instruction}

After completion:
1. Update .ai/HANDOFF.md:
   - YAML front matter: fill in story, step, attempt, status, reason, files_changed, tests values
   - Markdown body: record what was done, what's unresolved, what next session should note
2. If requirements are unclear, fill reason field with needs_clarification
3. If Constitution violation found, fill reason field with constitution_violation
```

### Fixed Step Instructions (step_instruction)

| Step | Instruction |
|------|-------------|
| bdd | Based on MEMORY's NOW/NEXT, write BDD scenarios for this Story. Use RFC 2119 language, tag test levels. Mark unclear items `[NEEDS CLARIFICATION]` |
| sdd-delta | Based on BDD scenarios, analyze affected modules, produce Delta Spec (ADDED/MODIFIED/REMOVED) |
| contract | Based on Delta Spec, update affected endpoints/events in OpenAPI/AsyncAPI contracts |
| scaffold | Based on BDD scenario tags and NFR table, produce corresponding test skeleton. All tests must fail (red) |
| impl | Read failing tests, write minimal code to make tests pass, then refactor |
| verify | Execute triple check: Completeness (all BDD has tests, all Delta implemented), Correctness (tests pass, NFR met), Coherence (SDD merged Delta, contracts consistent, Constitution not violated) |
| commit | Stage and commit all code changes with conventional commit message including story ID. Do NOT commit PROJECT_MEMORY.md or .ai/history.md. Record commit hash in HANDOFF.md front-matter as `commit_hash: <hash>` |
| update-memory | Read HANDOFF.md commit_hash + STATE.json test results, update MEMORY's NOW/TESTS/NEXT/ISSUES/SYNC. Append DONE + LOG entry to `.ai/history.md`. Overwrite HANDOFF.md with latest session state |

---

## Hook Mechanism

After executor completes (or fails), hook automatically executes to write results back to STATE.json and notify orchestrator.

### Hook Responsibility

```bash
#!/bin/bash
# post-execution hook (pseudocode)
PROJECT_ROOT="$1"
STATE_FILE="$PROJECT_ROOT/.ai/STATE.json"
STEP=$(jq -r '.step' "$STATE_FILE")

# 1. Run tests (if this step requires tests)
if [[ "$STEP" =~ ^(scaffold|impl|verify)$ ]]; then
  TEST_OUTPUT=$(cd "$PROJECT_ROOT" && go test ./... -json 2>&1)
  PASS=$(echo "$TEST_OUTPUT" | grep -c '"Action":"pass"')
  FAIL=$(echo "$TEST_OUTPUT" | grep -c '"Action":"fail"')
  SKIP=$(echo "$TEST_OUTPUT" | grep -c '"Action":"skip"')
fi

# 2. Run post_check (if step rules define it)
if [[ -n "$POST_CHECK" ]]; then
  LINT_RESULT=$(cd "$PROJECT_ROOT" && eval "$POST_CHECK" 2>&1)
  LINT_PASS=$?
fi

# 3. Read executor's reason tag (prioritize YAML front matter parsing)
HANDOFF_FILE="$PROJECT_ROOT/.ai/HANDOFF.md"
if head -1 "$HANDOFF_FILE" | grep -q '^---$'; then
  # Hybrid format: parse reason from YAML front matter
  REASON=$(sed -n '/^---$/,/^---$/p' "$HANDOFF_FILE" | grep '^reason:' | awk '{print $2}')
  STATUS_FROM_HANDOFF=$(sed -n '/^---$/,/^---$/p' "$HANDOFF_FILE" | grep '^status:' | awk '{print $2}')
else
  # Fallback: old format, grep markdown body
  REASON=$(grep -o 'NEEDS CLARIFICATION\|CONSTITUTION VIOLATION\|SCOPE WARNING' \
           "$HANDOFF_FILE" | head -1)
fi

# 3.5 Validate status and reason before writing to STATE.json
#     CRITICAL: Orchestrator strictly validates these values.
#     Writing an invalid value (e.g., "passing" instead of "pass") will
#     break the entire auto pipeline.
VALID_STATUSES="pass failing needs_human timeout"
if [[ -n "$STATUS_FROM_HANDOFF" ]]; then
  if ! echo "$VALID_STATUSES" | grep -qw "$STATUS_FROM_HANDOFF"; then
    echo "⚠️  Hook: invalid status '$STATUS_FROM_HANDOFF', defaulting to 'failing'" >&2
    STATUS_FROM_HANDOFF="failing"
  fi
fi

VALID_REASONS="constitution_violation needs_clarification nfr_missing scope_warning test_timeout"
if [[ -n "$REASON" && "$REASON" != "null" ]]; then
  if ! echo "$VALID_REASONS" | grep -qw "$REASON"; then
    echo "⚠️  Hook: invalid reason '$REASON', defaulting to null" >&2
    REASON="null"
  fi
fi

# 4. Update STATE.json
#    Write status, reason, tests, failing_tests, lint_pass,
#    files_changed, completed_at

# 5. Notify orchestrator
notify_orchestrator "$STATE_FILE"
```

### .ai/executor-result File (Recommended)

Dispatch prompt should require executor to write a structured file on completion, allowing hook to reliably extract reason and status. **Recommended all projects adopt**—more reliable than grepping HANDOFF.md.

```
# .ai/executor-result
status: pass
reason: null
summary: Timezone issue in ApplyCoupon fixed, now using UTC for comparison
```

| Field | Type | Notes |
|-------|------|-------|
| status | enum | **Only**: `pass` / `failing` / `needs_human`. See common mistakes below. |
| reason | enum? | **Only**: `null` / `constitution_violation` / `needs_clarification` / `nfr_missing` / `scope_warning` / `test_timeout`. **Must NOT be freeform text.** |
| summary | string | One-sentence summary of this run (freeform text OK here) |

> **⚠️ Common Mistakes — will break the orchestrator `auto` pipeline:**
>
> | Wrong value | Correct value | Why |
> |-------------|---------------|-----|
> | `passing` | `pass` | Orchestrator only recognizes `pass` |
> | `passed` | `pass` | Same as above |
> | `failed` | `failing` | Orchestrator uses present-participle `failing` |
> | `fail` | `failing` | Same as above |
> | Long text in `reason` | `null` or enum value | `reason` is machine-parsed for routing, not a log field. Put details in `summary` or HANDOFF.md body. |

Hook read priority: `.ai/executor-result` → fallback to grepping HANDOFF.md. Projects not using executor-result still work normally, but reason extraction reliability is lower.

---

## Reason-Based Routing

Simple binary pass/fail isn't enough. When executor fails, the failure reason determines the next step.

### Problem

If impl failures are retried unconditionally, these situations occur:

- **Constitution violation**: executor's implementation violates architecture principles, retrying won't help → should go back to sdd-delta to redesign
- **Requirement unclear**: executor found BDD scenario ambiguity, guessed a direction but tests didn't pass → should go back to review for human clarification
- **Scope creep**: executor modified code in Non-Goals range → should go back to review to confirm if really needed

### Solution

The `on_fail` field in the Step rules table supports reason-based routing:

```yaml
impl:
  on_fail:
    default: impl                    # General failure → retry
    constitution_violation: sdd-delta # Architecture violation → redesign
    needs_clarification: review       # Requirement unclear → back to human
    scope_warning: review             # Touched Non-Goals → confirm
```

Reason is extracted from HANDOFF.md or executor-result by hook, written to STATE.json's `reason` field. Orchestrator looks up the table to decide next step without understanding reason semantics.

---

## Known Issues and Solutions

### Issue 1: STATE ↔ MEMORY Sync Drift

**Risk:** Hook updates STATE to pass, but executor writes stale descriptions in MEMORY.

**Solution:** MEMORY's NOW section is not directly written by executor in impl/verify steps. In the `update-memory` step, executor generates NOW content based on STATE.json facts (test results, files_changed), ensuring consistency.

### Issue 2: Session Interruption Without Hook

**Risk:** Executor crashes, API disconnects, hook doesn't execute. STATE stuck at `running`.

**Solution:** STATE.json records `dispatched_at` + `timeout_min`. When orchestrator receives human instruction, it checks: if `status: running` and exceeds timeout, mark `status: timeout`, notify human.

### Issue 3: Failed Session Context Passing

**Risk:** Executor modified files but not all tests passed; next retry session doesn't know what was done.

**Solution:** HANDOFF.md. Every session (successful or not) must write handoff notes. dispatch prompt's `claude_reads` always includes HANDOFF.md.

### Issue 4: Human Opinion in Review

**Risk:** Human replies with modification opinions in communication channel, but executor can't see.

**Solution:** Orchestrator summarizes human message to `STATE.json.human_note`. Dispatch prompt template has `{if human_note}` block for next session.

### Issue 5: Multi-Project Parallel

**Risk:** A and B projects running simultaneously, dispatch conflicts.

**Solution:** Per-project STATE.json (`{project_root}/.ai/STATE.json`). Orchestrator checks if target project's status is `running` before dispatching. If yes, refuse and notify human.

### Issue 6: Step Routing Exception

**Risk:** impl failure doesn't always mean retry—might be Constitution violation, requirement unclear, or touched Non-Goals.

**Solution:** Reason-Based Routing (see section above).

### Issue 7: Multi-Story Parallel (Advanced)

**Risk:** Current STATE.json is per-project single file, can only track one Story at a time. When multiple Stories need parallel execution (like multi-agent collaboration), single file becomes a bottleneck.

**Solution (Optional):** Change to per-story STATE files:

```
.ai/
  states/
    US-005.json    ← Each Story independent
    US-006.json
  HANDOFF.md       ← Still latest session's handoff
```

Orchestrator's dispatch logic changes to scan `.ai/states/` directory, independently dispatch each Story with `status: pending`. The `blocked_by` field becomes especially important—orchestrator checks if dependent Stories are complete before dispatching.

**Note:** This is advanced mode; most projects work fine with single STATE.json. Only enable when truly needing multi-Story parallelism.

---

## Advanced Topics

The following advanced topics are covered in [Protocol-Advanced.md](Protocol-Advanced.md):

- **Multi-Executor Collaboration Mode** — Three-layer architecture, complexity-based dispatch, scoped context loading, role-based context isolation, coordinator ↔ executor communication, per-task HANDOFF, token cost impact
- **Reference Implementation: OpenClaw × Claude Code** — Architecture mapping, dispatch implementation, WhatsApp conversation example, adapter spec
- **Reference Implementation: Claude Code Agent Teams (Experimental)** — Three-layer architecture mapping, Lead behavior rules, spawn prompt examples, hook integration, known limitations

Most projects do not need these advanced features. Start with single-executor mode and upgrade when you need multi-Story parallelism or multi-executor collaboration.

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2026-02-13 | Initial: define Orchestrator × Executor architecture model, three-file communication protocol (STATE.json / HANDOFF.md / PROJECT_MEMORY.md), Step transition rules table, Dispatch logic, Hook mechanism, Reason-Based Routing, six known issues and solutions, OpenClaw × Claude Code reference implementation |
| v0.2 | 2026-02-13 | Add "Progressive Adoption" section: define Level 0 (manual) / Level 1 (semi-auto) / Level 2 (fully auto) three-stage adoption path, supplement concrete operation examples for new projects, adding features, supplementing specs |
| v0.3 | 2026-02-13 | Apply Windsurf Review: executor-result upgrade to recommended adoption (P0); STATE.json add blocked_by field (P1); review step support reason-based routing (P1); add OpenClaw Adapter Spec (P1); add Token Budget reference table (P2); clarify Component Test position in rules table (P2); Level 2 add Timeout Polling mechanism (P2); add per-story STATE design for multi-Story parallelism (P2) |
| v0.4 | 2026-02-14 | Add "Multi-Executor Collaboration Mode": three-layer architecture (Orchestrator → Coordinator → Executors), Complexity-Based Dispatch Mode (S/M/L), Scoped Context Loading (team_roles extension), Role-Based Context isolation, Coordinator ↔ Executor communication events, Per-Task HANDOFF format. Add "Reference Implementation: Claude Code Agent Teams (Experimental)": three-layer architecture mapping, Lead delegate mode behavior rules, Spawn Prompt example, Hook integration (TeammateIdle / TaskCompleted), complete Dispatch flow, known limitations and mitigations, four-phase experiment path. Incorporate Refinement four items: dynamic context loading, Test/Impl isolation, Agent subscription mechanism, handoff format |
| v0.5 | 2026-02-14 | Add "Executor Output Rules": Diff-Only principle (per-step anti-pattern table), Structure First (machine consumption vs human consumption category), Dispatch Prompt output instruction template. HANDOFF.md upgrade to hybrid format: YAML front matter (hook machine parsing) + Markdown body (executor natural language handoff), with field specs table; clarify relationship with executor-result (both approaches coexist) |
| v0.6 | 2026-02-14 | Apply Windsurf Round 2 Review: Hook pseudocode change to parse YAML front matter instead of grep (P0); Dispatch Prompt template reflect HANDOFF hybrid format requirements (P0); team_roles supplement test/verify role examples (P1); task_assigned scoped_context structure explanation (P1); STATE.json initialization example update complete schema (P2); Token Budget add Multi-Executor cross-reference (P2) |
| v0.7 | 2026-02-16 | Field feedback integration (FB-R01~R03): HANDOFF.md marked Full Mode Only with latest-entry-only + `.ai/history.md` archival; update-memory step instruction updated to write DONE/LOG to `.ai/history.md` and overwrite HANDOFF; update-memory `claude_writes` includes `.ai/history.md` |
| v0.8 | 2026-02-17 | Split advanced content into Protocol-Advanced.md: Multi-Executor Collaboration Mode, OpenClaw reference implementation, Agent Teams reference implementation. Core Protocol reduced from 1210 to ~800 lines |
| v0.9 | 2026-02-24 | Fix status/reason validation gap: Hook pseudocode adds step 3.5 (validate status against `pass`/`failing`/`needs_human`/`timeout` and reason against enum before writing STATE.json); executor-result section adds Common Mistakes table (`passing≠pass`, `failed≠failing`, freeform reason is invalid); strengthened field type docs from `string?` to `enum?` for reason |
| v0.10 | 2026-02-24 | Orchestrator self-describing responses: all `orchestrator auto` return values include `caller_instruction` (prevents LLM callers from hallucinating completion), `next_step` field in dispatched/query results; Step Boundary in dispatch prompt (executor must complete only current step, not advance); `startStory()` guards against restarting completed/running stories; STATE.json adds `last_error` field for executor crash/timeout diagnostics; new CLI `report-error` command for external error reporting |
| v0.11 | 2026-02-25 | Add `commit` step between verify and update-memory (solves commit hash chicken-and-egg problem); scaffold `treat_failing_as_pass` flag (RED stubs auto-normalize failing→pass, prevents infinite scaffold retry loop); Agent Teams structured spawn prompts from `DEFAULT_TEAM_ROLES` for parallel impl (backend/frontend/test teammates); pipeline now 10 steps: bdd→sdd-delta→contract→review→scaffold→impl→verify→commit→update-memory→done |
