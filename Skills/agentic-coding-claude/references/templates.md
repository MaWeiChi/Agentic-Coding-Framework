# Document Templates Reference

Condensed templates and writing guidelines for each framework document type. Use this
when producing any framework document.

For extended examples, see the full framework documentation at the project repository.

---

## PROJECT_MEMORY.md (Full Mode Only)

Only hot sections that the agent needs every turn. DONE and LOG live in `.ai/history.md`
to avoid system-reminder re-send cost.

```markdown
# PROJECT_MEMORY
<!-- commit:a1b2c3d | branch:main | dirty:no -->

## NOW
US-005 Shopping Cart Feature | phase:implementation | Backend API done, frontend WIP | blocker:none

## NEXT
1. Complete shopping cart frontend (BDD US-005)
2. Shopping cart component test
3. US-006 Checkout flow BDD

## TESTS
unit:42/42 ✅ | intg:18/18 ✅ | comp:12/12 ✅ | e2e:⏸ | perf:⏸

## ISSUES
- [Med] Safari WebP display anomaly (02-14)

## SYNC
- Product model → OpenAPI spec + frontend type
```

**Key rules:** Conciseness first. Agent-executable next steps. Git as anchor. Agents
can always append, never overwrite or delete human edits. Use minimal Edit (replace
only the changed section), not full-file Write. SYNC is **append-only** — never modify
or delete existing entries, only add new ones. When a sync relationship becomes obsolete
(e.g., module deleted), mark the entry with `[deprecated]` rather than removing it.

---

## .ai/history.md

Append-only archive for DONE stories, LOG entries, and session handoff history.
Agent reads this only at session start if needed — it is NOT auto-resent every turn.

```markdown
# Project History

## US-001 User registration — 02-13
status: complete
tests: unit:12 intg:6 comp:4
commit: f1a2b3c
changes: [auth module, user model, registration API]

## US-003 Product list — 02-14
status: complete
tests: unit:18 intg:8
commit: e4f5g6h
changes: [product module, list component]

## Session: US-005 (02-15)
status: in-progress
step: implementation
summary: Backend API done, frontend WIP
unresolved: Shopping cart state management approach TBD
next: Complete frontend cart component
```

**Key rules:** Append-only. Never delete or rewrite entries. Each Story completion
and each session end appends one block.

---

## .ai/HANDOFF.md (Full Mode Only)

Latest-entry-only: overwritten each session. Historical records archived in
`.ai/history.md`. Hybrid format — YAML front matter for machine parsing (hook →
STATE.json), markdown body for next executor session context.

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

## What was done this session
- <Concrete changes made>

## Not yet resolved
- <Failing tests, open questions>

## Next session should note
- <Warnings, gotchas, don't-touch areas>
```

**Key rules:** Overwrite entirely each session — never append. YAML front matter
fields must match STATE.json schema. Markdown body is freeform but keep it
actionable (what's done, what's stuck, what to watch out for).

---

## PROJECT_CONTEXT.md (CLAUDE.md)

```markdown
# <Project Name>

## Project Summary
- **Why** — <Problem solved>
- **Who** — <Target users>
- **What** — <Final deliverable>

## Technology Stack
- **Frontend**: <framework, language>
- **Backend**: <framework, language>
- **Database**: <type>
- **Infrastructure**: <deployment>

## Project Structure
<Concise directory tree, annotate most-used directories>

## Development Conventions
- Git branch strategy: ...
- Commit conventions: ...

## Agent Guidelines
- Agentic Coding Mode: full
- Read PROJECT_MEMORY.md before each session
- Follow BDD → SDD → TDD workflow
- Update PROJECT_MEMORY.md when story ends
- Don't refactor without ADR
```

**Lite Mode variant** (≤10 lines):
```markdown
# <Project Name>
- **What**: <one-line description>
- **Stack**: <language, framework>
- Agentic Coding Mode: lite
```

**Lite Mode PROJECT_MEMORY** (~5 lines):
```markdown
# PROJECT_MEMORY
<!-- commit:a1b2c3d | branch:main | dirty:no -->

## NOW
Fix login timeout bug | phase:implementation | blocker:none

## NEXT
1. Add retry logic for auth service
```

**Key rule:** This changes very little after bootstrap. Frequent-change info goes in Memory.

---

## BDD Scenarios

```gherkin
# Story: US-XXX <Title>

@unit @integration
Scenario: <Happy path behavior>
  Given <Initial state>
  When <User action>
  Then <Expected result>

@unit
Scenario: <Error path>
  Given <State>
  When <Boundary trigger>
  Then <Error handling>

@perf(PERF-01)
Scenario Outline: <Parameterized>
  Given <Precondition>
  When <Action> with "<param>"
  Then <Result> "<expected>"

  Examples:
    | param | expected |
    | ...   | ...      |
```

**Key rules:**

- One scenario verifies one thing (max 3 Thens)
- Tags are mandatory (`@unit`, `@integration`, `@component`, `@e2e`, `@perf(ID)`, `@secure(ID)`)
- RFC 2119 keywords: SHALL/MUST = hard requirement, SHOULD = recommended, MAY = optional
- `[NEEDS CLARIFICATION]` when ambiguous — don't guess
- Declarative style (describe state/result, not UI steps)
- Use Scenario Outline for parameterized cases
- Include Non-Goals section

**Anti-patterns to avoid:**

| Anti-pattern | Fix |
|-------------|-----|
| Imperative scenarios (UI steps) | Declarative behavior descriptions |
| Data shared between scenarios | Each scenario sets up its own Given |
| Incidental details in Given | Only minimum preconditions affecting Then |
| Multiple unrelated Thens | Split into separate scenarios |

---

## SDD Delta Spec

```markdown
## Delta: US-XXX <Story Title>

### Non-Goals
- <What this story explicitly doesn't do>

### ADDED
- Module: `NewModule` (Responsibility: ...)
- Data Model: `NewTable` (fields...)

### MODIFIED
- Module `ExistingModule`: add `newMethod()` method
- Data Model `ExistingTable`: add `new_field`

### REMOVED
- (None)
```

**Key rules:**

- Never rewrite entire SDD — only Delta
- Data Model in SDD is the single Source of Truth
- Include Non-Goals to prevent scope creep
- RFC 2119 keywords for constraints
- System Context: describe external system relationships too
- Use Mermaid diagrams where helpful (graph, erDiagram, sequenceDiagram)

---

## API Contract (OpenAPI / AsyncAPI)

- REST: OpenAPI 3.1 (or 3.0.3), in `docs/api/openapi.yaml`
- Events: AsyncAPI 3.0, in `docs/api/asyncapi.yaml`
- Contract first: define before implementing
- Incremental updates only
- All payloads must have complete schema definitions

---

## NFR (Non-Functional Requirements)

```markdown
# Non-Functional Requirements

## Performance
| ID | Description | Metric | Threshold | Scope | Tool | Priority |
|:---|:---|:---|:---|:---|:---|:---|
| PERF-01 | API response | p95 latency | < 200ms | /api/v1/* | k6 | P0 |

## Security
| ID | Description | Rule | Scope | Tool | Notes |
|:---|:---|:---|:---|:---|:---|
| SEC-01 | Auth | JWT Bearer | All non-/public/* | Integration Test | Verify 401/403 |
```

**Key rules:** Every entry has an ID. NFR table is the single source of truth for
thresholds — don't override in BDD. Scope must be precise (regex/path). Tool must be
specified. Start with 3 entries, expand as needed.

---

## Test Scaffolding

### Go Backend (testify)

```go
// Generated from: BDD US-XXX — <Scenario>
// Tags: @unit

func TestXxx_GivenCondition_WhenAction_ThenResult(t *testing.T) {
    // Given — require (precondition, stop on fail)
    cart, err := NewCart(userID)
    require.NoError(t, err)

    // When
    err = cart.AddItem(productID, 1)

    // Then — assert (verify, report all)
    assert.NoError(t, err)
    assert.Equal(t, 1, cart.ItemCount())
}
```

**Table-Driven** (for Scenario Outline):
```go
tests := []struct {
    name     string
    input    string
    expected string
}{
    {"case1", "abc", "too short"},
    {"case2", "Abcdefg1", "pass"},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        assert.Equal(t, tt.expected, Validate(tt.input))
    })
}
```

### Playwright Component Test

```typescript
// Tags: @component
test('<BDD scenario description>', async ({ mount }) => {
  const component = await mount(<Component />);
  // assertions
  test.fail(); // RED phase
});
```

### Playwright E2E Test

```typescript
// Tags: @e2e — runs at milestone, not per Story
test.describe('<User Flow>', () => {
  test('<BDD scenario>', async ({ page }) => {
    // full user journey
    test.fail(); // RED phase
  });
});
```

**Key rules:**

- BDD traceable: note source scenario at top of each test file
- Names from scenarios: `Given_When_Then` naming
- All red: every test must fail initially
- `require` for Given (stop on fail), `assert` for Then (report all)
- Extract helpers when 2+ tests share setup or 3+ share assertions

---

## Constitution

```markdown
# Project Constitution
> These principles always apply across all stories and agents.

1. **API-First**: All module communication SHALL use defined contracts; no direct cross-module DB access.
2. **Stateless Services**: Backend services SHALL be stateless.
3. **Auth Everywhere**: All non-/public/* routes SHALL verify JWT (SEC-01).
```

**Key rules:** Only immutable principles. All SHALL/MUST level. Link to NFR IDs.
Modifying Constitution requires ADR.

---

## DDD (When Multi-Domain)

**Level 1 — Bounded Context Map:** Mermaid graph + Context definitions table
(responsibility, type, path, contract)

**Level 2 — Glossary:** Ubiquitous language table with per-Context definitions +
type/constraint + example values. Agents MUST follow this for naming.

**Level 3 — Aggregate Root:** Embedded in SDD with `[DDD Tactical Constraint]` blocks.
Mark invariants and access restrictions.

**Domain Event Registry:** Central table of all cross-Context events (sender, receiver,
payload, trigger timing). Sync with AsyncAPI contract.

**Subdomain types:** Core (highest coverage, Delta + ADR required), Supporting (standard
coverage), Generic (prefer existing solutions).

---

## Review Checkpoint

```markdown
# Review Checkpoint — US-XXX <Title>

## Change Summary
- BDD: N scenarios (N @unit, N @integration, N @e2e)
- Delta: N ADDED, N MODIFIED, N REMOVED
- Contract: N new endpoints, N modified

## Pending Clarification
| # | Source | Issue | Suggestion |
|---|--------|-------|-----------|
| 1 | BDD #3 | [NEEDS CLARIFICATION] ... | Suggest ... |

## Non-Goals Confirmation
- This story doesn't handle: ...

## Review Conclusion
- [ ] BDD direction correct
- [ ] Delta scope reasonable
- [ ] Contract changes non-breaking
- [ ] Clarifications addressed
```

---

## Story Task Format

**Complexity markers** after Story title:
- `[S]` Simple: single module, < 3 files, implement directly
- `[M]` Medium: cross-module, 3-8 files, needs Delta Spec
- `[L]` Complex: architecture change, > 8 files, needs Delta + ADR + deep review

**`[P]` Parallel marking** for independent sub-tasks:
```markdown
1. [ ] Define data model + migration
2. [P] Repository CRUD + unit test
3. [P] Engine logic + unit test
4. [ ] Service integration (depends on #2, #3)
```
