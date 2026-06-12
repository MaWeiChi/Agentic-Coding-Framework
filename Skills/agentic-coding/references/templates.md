# Document Templates Reference

> Derived from: Templates v0.13 (2026-06-11)

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
- Team Size: 1
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

## Behavior Spec / Behavior Delta

Current behavior truth lives in `docs/specs/<capability>.md`. Each Story contributes a
**Behavior Delta** inside `docs/deltas/US-{id}.md`; it merges into the specs when Verify
passes. No `.feature` files (Gherkin is opt-in only when the stack executes it).

```markdown
## Behavior Delta — US-XXX <Story Title>

### ADDED Requirements

### Requirement: <short behavior statement> [R-<CAP>-NNN]
The system SHALL <behavior>.

#### Scenario: <branch label> (Test Level: integration)
- Given <initial state>
- When <user action>
- Then <expected result>

#### Scenario: <other branch> (Test Level: e2e) @perf(PERF-01)
- Given <precondition>
- When <action>
- Then <result>

**Parameters**: (only if configurable values exist)
| Parameter | Type | Unit | Range | Default | Example | R/W | Notes |
|-----------|------|------|-------|---------|---------|-----|-------|

**Error Cases**: <invalid input / permission / missing resource / concurrency>

### MODIFIED Requirements
<Restate full updated Requirement; note previous behavior in one line>

### REMOVED Requirements
- [R-<CAP>-NNN] <reason>
```

**Key rules:**

- One Requirement ID = one independently verifiable behavior = one test; IDs stable across Stories
- Specs hold externally observable behavior only — unit-level GWT is test names in code
- `Test Level` mandatory per scenario (`integration`, `component`, `e2e`); NFR tags (`@perf(ID)`, `@secure(ID)`) attach to the Scenario label
- One scenario verifies one thing (max 3 Thens); label scenarios by product-semantic branches, not boundary values
- **Scenario exemption:** pure parameter/range requirements → Parameters table + Error Cases, write `Scenarios: Not needed — <reason>`
- RFC 2119 keywords: SHALL/MUST = hard requirement, SHOULD = recommended, MAY = optional
- `[NEEDS CLARIFICATION: TBD-N — <answerable question>]` when ambiguous — don't guess; if the source gives a defensible hint, extract a candidate and disclose it in Assumptions Made instead
- No API details (endpoints, status codes, JSON fields) in scenarios — optional `API Reference: METHOD /path` line for traceability
- Event requirements state Trigger, NOT-Triggered condition, and message format + variables
- Declarative style (describe state/result, not UI steps)
- Include Non-Goals section

**Parameters table rules:**

- Counter (increment-only): Range `0 - (none)`, wrap/saturate in Notes; Gauge (point-in-time): real bound (`0-100`); UpDownCounter: `0 - <max>` or `0 - (none)`
- Never write type ceilings (`2^63-1`) as Range — use `0 - (none)`
- Device-dependent ceilings split into `xxxUsage` (Range `0 - (limit)`) + `xxxLimit`
- Type is requirement-level only (`integer`, `number`, `string`, `boolean`, `enum`) — no OpenAPI formats
- Boundary tests derive mechanically from Range/Error Cases via table-driven tests (replaces Scenario Outline)

**Anti-patterns to avoid:**

| Anti-pattern | Fix |
|-------------|-----|
| Imperative scenarios (UI steps) | Declarative behavior descriptions |
| Data shared between scenarios | Each scenario sets up its own Given |
| Incidental details in Given | Only minimum preconditions affecting Then |
| Multiple unrelated Thens | Split into separate scenarios |
| Boundary enumeration in scenarios | Parameters table + table-driven tests |
| Forced GWT on parameter rules | Scenario exemption: table + Error Cases |
| Unit-level scenarios in spec | Unit GWT lives as test names in code |

---

## SDD Delta Spec

Appended to the same `docs/deltas/US-{id}.md` file as the Behavior Delta.

```markdown
## SDD Delta — US-XXX <Story Title>

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
thresholds — don't override in scenarios. Scope must be precise (regex/path). Tool must
be specified. Start with 3 entries, expand as needed.

---

## Test Scaffolding

### Go Backend (testify)

```go
// Spec: R-CART-001 — <Requirement statement>
// Scenario: <branch label> | Test Level: integration | assertion_type: behavior

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

**Table-Driven** (derived from the Parameters table — Range boundaries + Error Cases as cases; `assertion_type: parameter`):
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
// Spec: R-CART-002 — <Requirement statement>
// Scenario: <branch label> | Test Level: component | assertion_type: behavior
test('<scenario description>', async ({ mount }) => {
  const component = await mount(<Component />);
  // assertions
  test.fail(); // RED phase
});
```

### Playwright E2E Test

```typescript
// Spec: R-CART-005 — <Requirement statement>
// Scenario: <flow label> | Test Level: e2e | assertion_type: behavior — runs at milestone, not per Story
test.describe('<User Flow>', () => {
  test('<scenario>', async ({ page }) => {
    // full user journey
    test.fail(); // RED phase
  });
});
```

**Key rules:**

- Requirement-ID traceable: machine-readable `Spec:` header at top of each test file (id, scenario label, Test Level, assertion_type)
- Names from scenarios: `Given_When_Then` naming
- Unit tests are not scaffolded from the spec — they accompany implementation with BDD-style names
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

**Pre-review self-check first** (don't send a review request that fails the mechanical pass):
- Mechanical: Requirement ID format, delta template compliance, `Test Level` on every scenario, no API details in scenarios
- Semantic: scenario executability, boundary sanity, Error Case coverage, cross-Story conflict, source coverage

```markdown
# Review Checkpoint — US-XXX <Title>

## Change Summary
- Behavior Delta: N ADDED, N MODIFIED, N REMOVED Requirements (N scenarios: N integration, N component, N e2e)
- SDD Delta: N ADDED, N MODIFIED, N REMOVED
- Contract: N new endpoints, N modified

## Assumptions Made
| # | Assumption | Basis |
|---|-----------|-------|
| 1 | <what was inferred> | <why it's defensible> |

## Pending Clarification
| # | Source | Issue | Suggestion |
|---|--------|-------|-----------|
| 1 | R-CART-012 | [NEEDS CLARIFICATION: TBD-1 — <answerable question>] | Suggest ... |

## Source Mapping
| Source Item | Handling | Note |
|-------------|----------|------|
| <story item> | Converted → R-XXX-NNN / Deferred | <reason if deferred> |

## Cross-Story Conflict Scan
- <conflicts/redundancy against existing specs — or "None found">

## Non-Goals Confirmation
- This story doesn't handle: ...

## Review Conclusion
- [ ] Behavior Delta direction correct
- [ ] Assumptions Made acceptable
- [ ] SDD Delta scope reasonable
- [ ] Contract changes non-breaking
- [ ] Clarifications addressed
```

Reviewer entry point: Assumptions Made → Pending Clarification → spot-check the deltas.

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
