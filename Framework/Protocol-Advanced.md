# Agentic Coding Protocol — Advanced Topics

**Multi-Executor Collaboration, Reference Implementations, and Experimental Features**

This document contains advanced protocol extensions split from [Protocol.md](Protocol.md). Most projects do not need these features — start with single-executor mode and upgrade when you need multi-Story parallelism or multi-executor collaboration.

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

ACO's `buildPrompt()` auto-generates structured spawn prompts from `DEFAULT_TEAM_ROLES` when `agent_teams: true`. Example output for the impl step:

```
=== AGENT TEAMS — PARALLEL EXECUTION ===
You are the TEAM LEAD. Create an agent team to parallelize this step.

### Teammate: backend
- Reads: docs/sdd.md, docs/api/openapi.yaml, internal/**/*.go
- Writes: *.go
- Spawn prompt: "You are the backend agent for story US-007.
  Your job is to implement the backend portion of this story.
  Read these files for context: docs/sdd.md, docs/api/openapi.yaml, internal/**/*.go.
  You may ONLY modify files matching: *.go.
  Do NOT touch files outside your scope.
  When done, send a message to the team lead with a summary of changes."

### Teammate: frontend
- Reads: docs/api/openapi.yaml, src/components/**
- Writes: *.ts, *.tsx
- Spawn prompt: ...

### Teammate: test
- Reads: docs/bdd/US-007.md, docs/api/openapi.yaml, docs/nfr.md
- Writes: *_test.go, *.spec.ts
- Spawn prompt: ...

TEAM LEAD INSTRUCTIONS:
1. Spawn all teammates using agent teams (NOT subagents)
2. Wait for ALL teammates to complete
3. Review results; if any teammate failed, report failing in HANDOFF.md
4. Merge all results into a single HANDOFF.md
5. Do NOT implement yourself — delegate to teammates
==========================================
```

To customize roles per project, override `DEFAULT_TEAM_ROLES` in `.ai/step-rules.yaml` (future).

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
