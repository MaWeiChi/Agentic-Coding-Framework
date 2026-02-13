# Agentic Coding Protocol

**Orchestrator × Executor Communication Protocol and Automation Process**

This document is the fourth core document of the [Agentic Coding Framework](Agentic_Coding_Framework.md), defining how the orchestrator and executor communicate, how state is passed, and how steps advance automatically.

---

## Related Documents

| Document | Content | When Agent Loads |
|----------|---------|-----------------|
| [Agentic_Coding_Framework.md](Agentic_Coding_Framework.md) | Framework core: layered definitions, core principles, processes | Required reading every conversation |
| [Agentic_Coding_Lifecycle.md](Agentic_Coding_Lifecycle.md) | Operating mechanism: iteration model, testing strategy, CI/CD interface | Load when planning iterations or configuring CI |
| [Agentic_Coding_Templates.md](Agentic_Coding_Templates.md) | Framework details: document templates for each layer, writing guides, examples | Load when writing BDD/SDD/contracts/Memory |
| This document | Communication protocol: orchestrator ↔ executor state management and automation | Load when configuring automation or integrating orchestrator |

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
| update-memory | ≈ 1,000-2,000 | ≈ 200-500 | Read Memory + STATE, update Memory |
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

`bdd` · `sdd-delta` · `contract` · `review` · `scaffold` · `impl` · `verify` · `update-memory` · `done`

These steps correspond to the micro-waterfall loop in the [Lifecycle document](Agentic_Coding_Lifecycle.md).

#### status State Machine

```
pending → running → pass → (orchestrator advances to next step)
                  → failing → (orchestrator retries or routes)
                  → timeout → (orchestrator notifies human)
                  → needs_human → (wait for human instruction)
```

#### Valid reason Values

`null` (general failure/success) · `constitution_violation` · `needs_clarification` · `nfr_missing` · `scope_warning` · `test_timeout`

### 2. HANDOFF.md — Executor-to-Executor Handoff Notes

Written at the end of each executor session, read at the start of the next session. **Overwritten each time, not accumulated**—this is a key difference from PROJECT_MEMORY.md.

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

Maintains the existing design in the [Templates document](Agentic_Coding_Templates.md). Orchestrator doesn't touch this file. Only adjustment: remove state machine responsibility (handled by STATE.json), return to pure project context.

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
    next_on_pass: update-memory
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

  update-memory:
    next_on_pass: done
    next_on_fail: update-memory
    max_attempts: 2
    timeout_min: 3
    requires_human: false
    claude_reads:
      - PROJECT_MEMORY.md
      - .ai/STATE.json            # Test results
    claude_writes:
      - PROJECT_MEMORY.md
```

### Component Test Location

Component Test (Playwright component testing) is defined in the [Lifecycle document](Agentic_Coding_Lifecycle.md) as a step after Implementation and before Verification. In the Step rules table, Component Test **is not a standalone step**—it's included in the `impl` step's `post_check` (for frontend projects) or as one of the `verify` step's Correctness checks.

Reason: Component Test execution timing differs from backend unit/integration tests (requires frontend components to be ready), but in automation workflows, it naturally follows impl completion. Projects can integrate `npx playwright test --project=ct` in `impl.post_check` for frontend projects.

### Relationship Between Rules Table and Lifecycle

The rule table's step sequence corresponds to the micro-waterfall loop in the [Lifecycle document](Agentic_Coding_Lifecycle.md). The `claude_reads` field defines what files the executor should load at each step, corresponding to the Framework's "load on demand" principle. `post_check` corresponds to AST Linting integration in Lifecycle (`go vet` + `golangci-lint`); frontend projects can extend it to `eslint . && tsc --noEmit && npx playwright test --project=ct`.

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
| update-memory | Read STATE.json test results, update MEMORY's DONE/TESTS/LOG/NEXT. Clear or update NOW |

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
| status | enum | `pass` / `failing` / `needs_human` |
| reason | string? | Failure reason code (same valid values as STATE.json reason) |
| summary | string | One-sentence summary of this run |

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

## Multi-Executor Collaboration Mode

So far, this protocol assumes each step has only one executor. When Story `[P]` parallel tags or `[L]` complexity require multiple executors working simultaneously, protocol extension is needed. This section defines **abstract multi-executor collaboration mode**, not bound to any specific tool.

### Three-Layer Architecture

```
Human
  ↕ Natural language
External Orchestrator (cross-Story / cross-project scheduling)
  ↕ Three-file protocol
Story-Level Coordinator (Story task breakdown and executor coordination)
  ↕ Scoped Context + Task distribution
Executor group (actual execution: write BDD / SDD / code / test)
```

In single-executor mode (`[S]` / no `[P]` in `[M]`), Coordinator and Executor are the same session—degrades to current two-layer architecture. Only `[M]+[P]` or `[L]` enables three-layer.

### Complexity-Based Dispatch Mode

Orchestrator before dispatching decides execution mode based on Story's Complexity and `[P]` tag:

| Complexity | `[P]` Tag | Dispatch Mode | Notes |
|------------|-----------|--------------|-------|
| `[S]` | — | `single` | Single executor, Team coordination cost > benefit |
| `[M]` | No `[P]` | `single` | Sequential tasks, no parallelism needed |
| `[M]` | Has `[P]` | `team` | Clear parallel task breakdown |
| `[L]` | — | `team` | Cross-module, recommend multi-executor |

Can be configured in Step rules table:

```yaml
dispatch_mode:
  S: single
  M: auto       # Check `[P]` count, enable team only if ≥ 2
  L: team
```

### Scoped Context Loading (Dynamic Context Loading)

In single-executor mode, `claude_reads` is per-step (what to read each step). In multi-executor mode, Coordinator needs to assemble **context subset within scope** for each executor—not load everything, load per task.

Rules table extends `team_roles` field, defining context scope per role:

```yaml
impl:
  # Single-executor mode still uses claude_reads
  claude_reads:
    - docs/sdd.md
    - docs/api/openapi.yaml
    - .ai/HANDOFF.md

  # Multi-executor mode uses team_roles (optional)
  team_roles:
    backend:
      claude_reads:
        - docs/sdd.md
        - docs/api/openapi.yaml
        - "internal/**/*.go"
      claude_writes:
        - "*.go"
    frontend:
      claude_reads:
        - docs/api/openapi.yaml
        - "src/components/**"
      claude_writes:
        - "*.ts"
        - "*.tsx"
    test:
      claude_reads:
        - docs/bdd/US-{story}.md
        - docs/api/openapi.yaml
        - docs/nfr.md
      claude_writes:
        - "*_test.go"
        - "*.spec.ts"
    verify:
      claude_reads:
        - docs/bdd/US-{story}.md
        - docs/deltas/US-{story}.md
        - docs/api/openapi.yaml
        - docs/constitution.md
      claude_writes: []
```

**Note:** `team_roles` is reference for Coordinator assembling spawn prompt, not a hard constraint. Coordinator can adjust context given to executor based on actual task needs.

### Role-Based Context Isolation

Multi-executor mode naturally provides context isolation—different executors are independent context windows. Framework level should ensure:

| Role | Can Read | Cannot Read | Reason |
|------|----------|------------|--------|
| impl executor | SDD, contracts, HANDOFF | Other impl executor's code (unless shared module) | Avoid file conflict |
| test executor | BDD, contracts, NFR, test output | impl source code | Verify independence—test derives expectations from BDD, not reverse-engineer from code |
| verify executor | BDD, SDD, contracts, Constitution, test output | impl intermediate artifacts | Consistency check needs global view |

This solves the "Test/Impl context isolation" problem in Refinement—multi-executor mode naturally isolates, framework just needs to define role boundaries.

### Coordinator ↔ Executor Communication

Communication mode between Coordinator and Executors depends on specific tool capabilities. Framework only defines **what information needs to be passed**, not the mechanism:

| Event | Direction | Content | Purpose |
|-------|-----------|---------|---------|
| task_assigned | Coordinator → Executor | `{task_id, role, scoped_context, instruction}` (scoped_context = list of files from team_roles[role].claude_reads) | Task assignment |
| task_done | Executor → Coordinator | `{task_id, status, files_changed, summary}` | Report completion |
| blocker | Executor → Coordinator | `{task_id, reason, description}` | Report stuck |
| conflict | Executor → Coordinator | `{files, description}` | Report file ownership conflict |

Specific tool implementation: Agent Teams use mailbox, subagent use return value, CLI multi-session use file-based message queue. Framework doesn't prescribe.

### Per-Task HANDOFF

Single-executor mode: HANDOFF.md overwrites each time. Multi-executor mode: when multiple executors work simultaneously, need finer-grained handoff:

- **Intra-session** (same round within team): use tool's own communication mechanism (mailbox / shared task list), no HANDOFF needed
- **Cross-session** (team ends, next session continues): Coordinator writes **consolidated HANDOFF** before team ends, summarizing all executor progress

```markdown
# HANDOFF — US-007 impl (multi-executor session)

## Executor Progress
- backend: ✅ CouponRepository + DiscountEngine done
- frontend: 🔄 Coupon component 50%, DatePicker has timezone issue
- test: ✅ unit tests done, integration test awaiting frontend

## File Conflict Log
- None

## Next session notes
- frontend DatePicker timezone issue needs resolving first
- integration test depends on frontend completion
```

### Token Cost Impact

Multi-executor mode trades more tokens for faster completion. Rough estimate:

| Mode | Single Story Token Est. | Speed | Use Case |
|------|------------------------|-------|----------|
| Single executor | 15,000-40,000 | 1x | Daily dev, `[S]`/`[M]` |
| Multi executor (3) | 40,000-100,000 | ~2-3x faster | Rush, `[L]`, clear `[P]` tags |

Decision: only enable team mode when token budget is ample and want more Stories completed per day.

---

## Reference Implementation: OpenClaw × Claude Code

Below is concrete implementation reference of this protocol in OpenClaw + Claude Code architecture. Other orchestrator × executor combinations can follow this pattern.

### Architecture

```
Human (WhatsApp / Telegram / ...)
  ↕ Natural language
OpenClaw (orchestrator · Gemini Flash · minimal token)
  ↕ Three-file protocol
Claude Code (executor · Opus/Sonnet · main token cost)
  ↕ Project files (BDD / SDD / contracts / Memory)
Codebase
```

### Role Mapping

| Protocol Role | Implementation | Token Cost |
|---------------|----------------|-----------|
| Orchestrator | OpenClaw + Gemini Flash | ≈ 100-200 tokens/interaction (only parse language + assemble reply) |
| Executor | Claude Code (Opus/Sonnet) | Main cost, correlates with Story complexity |
| Communication Channel | WhatsApp / Telegram | — |
| Hook | claude-code-hooks (notify-agi.sh) | — |

### OpenClaw Dispatch Implementation

OpenClaw's dispatch logic corresponds to the "Dispatch Logic" section. Specific implementation via OpenClaw's agent runtime calling Claude Code CLI:

1. OpenClaw receives human message (WhatsApp)
2. Gemini Flash parses intent: "continue A" → project=cart-app, action=continue
3. Execute `dispatch(project)` deterministic logic (zero LLM tokens)
4. Start Claude Code session via `dispatch-claude-code.sh`
5. Claude Code completes, `notify-agi.sh` hook updates STATE.json and notifies OpenClaw
6. OpenClaw uses Gemini Flash to assemble human-readable progress report

### WhatsApp Conversation Example

```
You: Continue A
Secretary: Received. Project A executing US-005 impl (attempt 3)

(3 minutes later)

Secretary: US-005 impl complete ✓ All tests pass (44/44), entering verify

(1 minute later)

Secretary: US-005 verify pass ✓ Memory updated.
           Next is US-006 checkout flow, continue?

You: Continue

Secretary: Writing US-006 BDD scenarios

(2 minutes later)

Secretary: US-006 BDD complete, need your review:
           - Scenario 1: Payment method selection
           - Scenario 2: Credit card verification failure
           - Scenario 3: Clear cart after checkout
           One clarification needed: third-party payment gateway timeout duration?

You: 30 seconds, others OK

Secretary: Received, continuing.

(10 minutes later, scaffold + impl + verify auto-complete)

Secretary: US-006 all complete ✓
           Next is US-007 order history, continue?

You: Stop for today

Secretary: OK. Project A progress:
           ✅ US-001 ~ US-006
           ⏭ Next US-007
           Say "continue A" tomorrow to resume.
```

---

## OpenClaw Adapter Spec (Reference Design)

This section defines how OpenClaw as orchestrator interfaces with this protocol. Other orchestrators (Telegram Bot, CLI tool, etc.) can follow this pattern to design their own adapter.

### Adapter Responsibility

Adapter is the bridge between orchestrator and three-file protocol. Its responsibilities are:

1. **Intent Parsing**: Parse human natural language instructions to `{project, action, params}` structure
2. **State Management**: Read/write STATE.json, execute dispatch logic
3. **Executor Invocation**: Start executor session via CLI or API
4. **Result Reporting**: Convert STATE.json state changes to human-readable messages

### Interface Definition

```typescript
interface OrchestratorAdapter {
  // Intent Parsing (requires LLM, low token)
  parseIntent(message: string): {
    project: string;
    action: 'continue' | 'status' | 'retry' | 'skip' | 'abort';
    params?: Record<string, string>;
  };

  // State Management (zero LLM tokens)
  readState(projectRoot: string): State;
  writeState(projectRoot: string, state: State): void;
  dispatch(projectRoot: string): DispatchResult;

  // Executor Invocation (trigger executor, itself no LLM token)
  invokeExecutor(projectRoot: string, prompt: string): ExecutorHandle;

  // Result Reporting (requires LLM, low token)
  formatReport(state: State, action: string): string;
}

type DispatchResult =
  | { type: 'dispatched'; step: string; attempt: number }
  | { type: 'blocked'; reason: string }
  | { type: 'needs_human'; message: string }
  | { type: 'done'; summary: string };
```

### OpenClaw-Specific Implementation Details

| Component | OpenClaw Implementation | Generic Adapter Alternative |
|-----------|------------------------|------------------------------|
| Intent Parsing | Gemini Flash (≈ 100 tokens) | Any lightweight LLM or regex |
| Communication Channel | WhatsApp / Telegram | CLI / Slack / Discord / Web UI |
| Executor | Claude Code CLI (`claude -p`) | Any LLM coding agent |
| Hook | `notify-agi.sh` (claude-code-hooks) | Any post-execution callback |

### Initialization Flow

```bash
# 1. Initialize .ai/ structure at project root
mkdir -p .ai
echo '{"project":"<name>","story":null,"step":"bdd","attempt":1,"max_attempts":3,"status":"pending","reason":null,"dispatched_at":null,"completed_at":null,"timeout_min":5,"tests":null,"failing_tests":[],"lint_pass":null,"files_changed":[],"blocked_by":[],"human_note":null}' > .ai/STATE.json

# 2. Ensure project has PROJECT_CONTEXT.md and PROJECT_MEMORY.md
# 3. Ensure framework files readable by executor (reference in CLAUDE.md or place in .ai/)
# 4. Configure hook: STATE.json auto-updates after executor completion
```

---

## Reference Implementation: Claude Code Agent Teams (Experimental)

> ⚠️ **Experimental Feature**: Agent Teams currently experimental in Claude Code (requires manual `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`), has known limits. This section defines exploration direction, not stable protocol.

This section maps abstract concepts from "Multi-Executor Collaboration Mode" above to concrete Claude Code Agent Teams tools. Can stack with OpenClaw × Claude Code two-layer architecture—OpenClaw handles cross-Story scheduling, Agent Teams handles Story-level parallel task execution.

### Three-Layer Architecture Mapping

```
Human (WhatsApp / Telegram / ...)
  ↕ Natural language
OpenClaw (L1 orchestrator · Gemini Flash · cross-Story scheduling)
  ↕ Three-file protocol
Claude Code Lead (L2 coordinator · delegate mode · Story-level scheduling)
  ↕ mailbox + shared task list
Claude Code Teammates (L3 executors · actually write code/test/doc)
```

| Layer | Role | Responsibility | Token Characteristics |
|-------|------|-----------------|----------------------|
| L1 | OpenClaw | Cross-Story / cross-project scheduling | Very low (Gemini Flash) |
| L2 | Claude Code Lead | Story task breakdown, teammate coordination | Moderate (coordination tokens) |
| L3 | Claude Code Teammates | Write BDD / SDD / code / test | High (main cost) |

### Lead Behavior Rules

Lead should enable **delegate mode** (Shift+Tab) to ensure only orchestrating, not coding:

1. Read BDD scenario `[P]` tags, identify parallelizable tasks
2. Assemble **scoped spawn prompt** for each teammate—only give context subset that role needs
3. Monitor progress via mailbox, don't implement yourself
4. After all teammates complete, synthesize results
5. Update STATE.json (status, tests, files_changed) and HANDOFF.md (consolidated format)

### Spawn Prompt Example

```
You are the backend executor for cart-app project US-007.

Please read the following files:
- docs/sdd.md (focus on DiscountEngine and CartService modules)
- docs/api/openapi.yaml
- .ai/HANDOFF.md

Your tasks:
1. Implement CouponRepository CRUD (internal/coupon/repository.go)
2. Implement DiscountEngine discount calculation (internal/discount/engine.go)
3. Run go vet && golangci-lint run to confirm pass

After completion:
- Write status and summary to .ai/executor-result
- Update .ai/HANDOFF.md for backend progress
- Don't modify frontend files (src/ is frontend teammate's scope)
```

### Hook Integration

Agent Teams provide two hooks available for quality control:

| Hook | Trigger | Framework Use |
|------|---------|---------------|
| `TeammateIdle` | Teammate about to idle | Check for incomplete `[P]` tasks, reassign if any |
| `TaskCompleted` | Task marked complete | Run post_check (linting), fail task completion if fail |

```bash
# .claude/hooks/TaskCompleted.sh (pseudocode)
TASK_FILES=$(jq -r '.files_changed[]' /tmp/task-result.json)
# Run linting
cd "$PROJECT_ROOT" && go vet ./... && golangci-lint run
if [ $? -ne 0 ]; then
  echo "Linting failed, please fix before completing"
  exit 2  # Block task completion, feedback back to teammate
fi
```

### Complete Dispatch Flow

```
1. Human → OpenClaw: "continue A"
2. OpenClaw → read STATE.json → judge dispatch_mode
   - [S] / [M] no [P]: start single Claude Code session (existing flow)
   - [M]+[P] / [L]: start Claude Code and instruct team creation
3. Claude Code Lead starts → read BDD + Task List → enter delegate mode
4. Lead spawn teammates → assemble scoped prompt for each teammate
5. Teammates work in parallel → mailbox reports → Lead monitors
6. Lead confirm all complete → update STATE.json + consolidated HANDOFF.md
7. Hook → notify OpenClaw
8. OpenClaw → read STATE → dispatch next step or report to human
```

### Known Limitations and Mitigations

| Limitation | Source | Impact | Mitigation |
|-----------|--------|--------|-----------|
| No session resumption | Agent Teams known limit | Team crash, teammates disappear, Lead message fails | Each teammate writes mini-HANDOFF on task completion; Lead rebuilds context from consolidated HANDOFF on recovery |
| File conflicts | Two teammates modify same file | Later write overwrites earlier | `team_roles.claude_writes` defines file ownership boundary; `[P]` tags ensure parallel tasks don't touch same file |
| Task status lag | Agent Teams known limit | Teammate completes but doesn't mark, dependent tasks blocked | Lead periodically check-in; `TaskCompleted` hook as fallback |
| Lead doing work himself | Agent Teams known behavior | Lead writes code instead of delegate | Spawn prompt explicitly instruct delegate mode; Shift+Tab on startup |
| Token explosion | Each teammate is independent instance | Cost grows linearly with teammate count | Complexity-based dispatch (only `[M]+[P]` / `[L]` use teams) |
| One team per session | Agent Teams known limit | One Lead can only manage one team | One Story one team session; cross-Story managed by OpenClaw |

### Recommended Experiment Steps

This reference implementation doesn't recommend all-in-one. Recommended experiment path:

1. **Phase 1**: Manually create Agent Team on one `[M]+[P]` Story (not via OpenClaw), verify scoped spawn prompt + delegate mode effect
2. **Phase 2**: Add `TaskCompleted` hook for auto linting gate, verify quality control
3. **Phase 3**: Integrate OpenClaw dispatch, let OpenClaw auto-decide team based on Complexity
4. **Phase 4**: After accumulating experience, upgrade stable patterns from "experimental reference implementation" to "official protocol"

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
