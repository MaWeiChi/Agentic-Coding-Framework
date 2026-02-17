# Agentic Coding Templates

**Templates, writing guidelines, and examples for each layer of documentation**

This document supplements the framework details of [Agentic Coding Framework](Framework.md). Agents load this as a reference when writing BDD, SDD, API contracts, Memory, and other documents.

---

## Related Documents

| Document | Content | When Agent Should Load |
|------|------|---------------|
| [Framework.md](Framework.md) | Framework body: layered definitions, core principles, workflow | Required reading for every session |
| [Lifecycle.md](Lifecycle.md) | Operating mechanisms: iterative model, testing strategy, CI/CD interface | Load when planning iterations or setting up CI |
| This document | Framework details: document templates for each layer, writing guidelines, examples | Load when writing BDD/SDD/contracts/Memory |
| [Protocol.md](Protocol.md) | Communication protocol: orchestrator ↔ executor state management and automation | Load when setting up automation or integrating orchestrator |

---

## PROJECT_MEMORY.md Template

### Positioning

PROJECT_MEMORY.md is a **dynamic state tracking document** for the project, placed in the project root. Any AI tool (Claude Code, Cursor, Windsurf, Copilot, etc.) should read this file when starting to continue from where the previous development session left off.

Division of labor with project summary: the project summary (first layer) records stable information about Why / Who / What; Memory records continuously changing information about "where we are now" and "what's next."

### Git Commit Validation Mechanism

Memory records the git commit hash at the time of last update. The agent should perform the following validation when starting:

```
1. Read last_commit_hash from Memory
2. Run git log --oneline to get the latest commit
3. Compare:
   - Match → Memory is current, proceed directly
   - Mismatch → There are unrecorded changes in between (human or other AI tool)
     → Run git log <last_commit_hash>..HEAD to see differences
     → Run git diff <last_commit_hash>..HEAD to see change details
     → Update relevant sections of Memory before starting work
```

This mechanism keeps Memory consistent across tool usage. Whether a human manually modified code or another AI tool made changes, the next agent to take over can detect and synchronize with the changes.

### Full Mode Template

Design principle: **minimum tokens, maximum information density.** Only hot sections that the agent needs every turn live in PROJECT_MEMORY. Historical/static data (DONE, LOG) lives in `.ai/history.md` to avoid system-reminder re-send cost.

Structure uses a three-phase hierarchical loading approach:
1. **HTML comment** (first line): machine marker, agent completes git validation in one line
2. **NOW + NEXT** (first 10 lines): agent can start work just from reading this section
3. **Remaining sections**: complete state, read only when needed

Section names use English uppercase abbreviations to compress tokens and help agents locate content using keywords.

```markdown
# PROJECT_MEMORY
<!-- commit:a1b2c3d | branch:main | dirty:no -->

## NOW
US-005 Shopping Cart Feature | phase:implementation | Backend API done, frontend component WIP | blocker:none

## NEXT
1. Complete shopping cart frontend component (BDD US-005)
2. Shopping cart component test
3. Safari WebP image issue
4. US-006 Checkout flow BDD

## TESTS
unit:42/42 ✅ | intg:18/18 ✅ | comp:12/12 ✅ | e2e:⏸ | perf:⏸

## ISSUES
- [Med] Safari WebP display anomaly (02-14)

## SYNC
- Product model → OpenAPI spec + frontend type
- Authentication logic → middleware test + E2E login
- DB schema → migration + SDD data model
```

### Lite Mode Template

Minimal PROJECT_MEMORY for Lite mode (~5 lines). Even one-off tasks benefit from this in case follow-up sessions occur.

```markdown
# PROJECT_MEMORY
<!-- commit:a1b2c3d | branch:main | dirty:no -->

## NOW
Fix login timeout bug | phase:implementation | blocker:none

## NEXT
1. Add retry logic for auth service
```

### .ai/history.md Template

Append-only archive for DONE stories, LOG entries, and session handoff history. Agent reads this only at session start if needed — it is NOT auto-resent every turn.

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

Key rules: Append-only. Never delete or rewrite entries. Each Story completion and each session end appends one block.

### Section Explanation (Full Mode)

| Section | Location | Purpose | Authoritative Source | Update Frequency |
|---------|----------|---------|----------|----------|
| `<!-- -->` | Memory | Git status, fast machine validation | git (fact) | Every commit |
| `NOW` | Memory | Current task, phase, blockers | Human intent priority | Every session |
| `NEXT` | Memory | Backlog priority order | Human intent priority | When story completes |
| `TESTS` | Memory | Passing test counts by level | CI / tests (fact) | After every test run |
| `ISSUES` | Memory | Unresolved problems | Mixed (agent can add, doesn't delete human's) | Anytime |
| `SYNC` | Memory | Cross-update reminders (change A requires change B) | Human knowledge priority | Add when discovered |
| `DONE` | .ai/history.md | Completed features + test coverage summary | git + tests (fact) | When story completes |
| `LOG` | .ai/history.md | Commit history entries | git (fact) | When story completes |

### Writing Principles

**Conciseness first**: Memory is a quick reference tool for agents, not a complete document. Each section should point to the essentials; details should be left in the corresponding documents (BDD, SDD, test reports).

**Agent-executable**: Descriptions of "next steps" should be concrete enough for agents to take direct action, avoiding vague descriptions. Good example: "Complete shopping cart frontend component (per BDD scenario US-005)." Bad example: "Continue developing shopping cart."

**Git as anchor**: Every time Memory is updated, the current git commit hash must be recorded synchronously. This is the foundation for cross-tool validation.

**Human-machine co-authoring**: Agents automatically update routine changes; humans manually edit priority adjustments, strategy changes, and other decisions agents cannot make. When conflicts occur, distinguish the authoritative source by "fact vs. intent": factual sections (git status, test status, change records) defer to git/tests; intent sections (current task, next steps, sync reminders) defer to humans. Agents can always "add" but never "override" or "delete" human edits. The complete conflict resolution strategy is defined in the [Lifecycle document](Lifecycle.md)'s Memory update rules.

---

## CLAUDE.md / Project Entry Document Template

### Positioning

Place in the project root as the first document agents read for every conversation. Since it's used across tools, it's recommended to use a universal name `PROJECT_CONTEXT.md`, with each tool pointing to it in its own way (Claude Code can `@include` it in CLAUDE.md or reference it directly).

### Template

```markdown
# <Project Name>

## Project Summary

- **Why** — <What problem does this solve>
- **Who** — <Target users>
- **What** — <What form is the final product>

## Technology Stack

- **Frontend**: <framework, language>
- **Backend**: <framework, language>
- **Database**: <database type and name>
- **Infrastructure**: <deployment method>

## Project Structure

<Concise directory structure, annotating directories agents most frequently work with>

## Development Conventions

- Git branch strategy: <explanation>
- Commit conventions: <explanation>
- Naming conventions: <explanation>

## Agent Guidelines

- Agentic Coding Mode: full
- Read `PROJECT_MEMORY.md` before each session to understand the current project state
- Follow the BDD → SDD → TDD development workflow (see Agentic Coding Framework for details)
- Update `PROJECT_MEMORY.md` when each story ends
- Don't refactor design decisions without ADR documentation of the reasoning
```

**Lite Mode variant** (≤10 lines):
```markdown
# <Project Name>
- **What**: <one-line description>
- **Stack**: <language, framework>
- Agentic Coding Mode: lite
```

### Writing Principles

**Stability first**: This document should change very little after bootstrap. Information that changes frequently (progress, tasks, status) goes in Memory, not here.

**Token-friendly**: Minimize its proportion of the agent's context window, leaving more space for actual code.

---

## BDD Scenario Template

### Positioning

One or a set of BDD scenario files per User Story, placed in `docs/bdd/` or `features/` directory.

### Template

```gherkin
# Story: <US-XXX> <Story Title>

## Preconditions (Shared)
# If multiple scenarios share the same preconditions, describe them collectively here.

@unit @integration
Scenario: <Behavior description for the happy path>
  Given <System or user initial state>
  When <User action or system event>
  Then <Expected result or state change>
  And <Additional verification points>

@unit
Scenario: <Behavior description for boundary condition or error path>
  Given <Initial state>
  When <Action that triggers boundary condition>
  Then <Expected error handling behavior>

@e2e
Scenario: <Complete user flow>
  Given <User is on some page or state>
  When <Series of operation steps>
  Then <Final expected result>

@perf(PERF-02) @secure(SEC-01)
Scenario: <Performance or security related scenario>
  Given <Load condition or security premise>
  When <Trigger action>
  Then <Expected result (consult NFR table for specific thresholds)>
```

### Writing Principles

**One scenario verifies one thing**: Avoid stuffing too many Thens into a single scenario. If a scenario has more than three Thens, consider splitting it.

**Tags are mandatory**: Each scenario must have at least one test level tag. This drives Test Scaffolding generation; scenarios without tags won't get automated tests generated. Tags come in two syntaxes: simple tags (`@unit`, `@e2e`) define test levels; tags with IDs (`@perf(PERF-01)`, `@secure(SEC-01)`) define test levels and reference specific thresholds from the NFR table.

**RFC 2119 keyword strength**: Use RFC 2119 keywords in BDD scenarios to distinguish requirement strength. This lets agents judge which are non-negotiable hard requirements and which are advisory.

| Keyword | Meaning | Agent Behavior |
|--------|---------|-----------|
| `SHALL` / `MUST` | Non-negotiable hard requirement | Must implement; missing causes test failure |
| `SHOULD` | Strongly recommended unless good reason otherwise | Implement by default; skipping requires documenting reason in ADR |
| `MAY` | Optional feature | Agent can decide whether to implement |

Example:
```gherkin
@unit
Scenario: Password strength validation
  Given User is on the registration page
  When Entering password
  Then Password SHALL be at least 8 characters
  And Password SHOULD contain mixed case
  And Password MAY support special character hint
```

**[NEEDS CLARIFICATION] tag**: When requirement descriptions are ambiguous or lack sufficient detail, agents must tag `[NEEDS CLARIFICATION]` rather than guessing. After tagging, pause subsequent steps for that scenario (SDD/TDD) and wait for humans to clarify during the next Review Checkpoint.

```gherkin
@unit
Scenario: Product search results sorting
  Given User searches for "phone"
  When Search results return
  Then Results SHALL be sorted by relevance [NEEDS CLARIFICATION: relevance calculation method undefined—TF-IDF? Sales-weighted? Manual recommendation?]
```

Agent handling rules:
- When encountering `[NEEDS CLARIFICATION]` in scenarios, Test Scaffolding still generates the skeleton but marks tests as `t.Skip("NEEDS CLARIFICATION")` rather than `t.Fatal("Not implemented")`
- Add pending clarification items to Memory's `ISSUES` section
- During Review Checkpoint when human clarifies, remove the tag and complete the scenario

**Given describes state, When describes action, Then describes result**: Avoid putting operations in Given, expected results in When.

**Use domain language**: Use business language in scenario descriptions, not technical terminology. "User submits order" not "POST /api/orders."

**Declarative first**: Prefer declarative Given/When/Then that describe "what state" and "what result," avoiding UI operation details (which button to click, which field to enter). Declarative scenarios don't break when the UI changes. Good example: "When user submits form with invalid email." Bad example: "When user clicks email field and types abc then presses submit button."

**Scenario Outline (parameterized scenarios)**: When the same behavior needs to be verified with multiple input/output combinations, use Scenario Outline with Examples table instead of copying multiple Scenarios. One Outline replaces N repeated scenarios, saving tokens and covering more boundary conditions.

```gherkin
@unit
Scenario Outline: Password strength validation
  Given User is on the registration page
  When Entering password "<password>"
  Then Display validation result "<result>"

  Examples:
    | password     | result           |
    | abc          | At least 8 characters       |
    | abcdefgh     | Need to contain numbers      |
    | Abcdefg1     | Pass             |
```

**Non-Goals (optional but recommended)**: List things explicitly not included in this story in the BDD file opening or corresponding Delta Spec. Agents check during Implementation whether changes touch Non-Goals and tag with `[SCOPE WARNING]` if they do.

**Common BDD anti-patterns agents make**:

| Anti-pattern | Problem | Correct Approach |
|--------|------|---------|
| Imperative scenarios | Written as UI operation steps, breaks when UI changes | Use declarative description of behavior and results |
| Data transfer between scenarios | Data created in Scenario A used in Scenario B | Each scenario is independent; Given creates preconditions itself |
| Incidental Details | Given stuffed with details unrelated to verification | Given describes only the minimum preconditions affecting Then results |
| Multiple Thens | One scenario verifies too many things | One scenario verifies one thing; Then not more than three items |

---

## SDD Template

### Positioning

One SDD covers the entire project's architectural design, updated incrementally with each Story. Place in `docs/sdd.md` or `docs/design/` directory.

### Template

```markdown
# Software Design Document — <Project Name>

## System Architecture

<Architecture diagram or text description: frontend/backend separation, data flow, deployment topology>

## Module Division

### <Module Name A>

- **Responsibility**: <What this module is responsible for>
- **External Interface**: <What APIs or functions it provides>
- **Dependencies**: <Which other modules it depends on>
- **Data Model**: <Core data structures>

### <Module Name B>

...

## Data Model

<DB schema design including table names, fields, relationships>

## Technical Decisions (ADR can be incorporated here)

### <Decision Title>
- **Decision**: <What was chosen>
- **Rationale**: <Why this choice>
- **Alternatives**: <Considered but not chosen>
- **Date**: <Decision date>

## Cross-Module Interaction

<How modules communicate: synchronous API calls, event-driven, shared DB, etc.>
```

### Delta Spec Incremental Update Format

When a Story causes SDD changes, use the Delta Spec format to record changes rather than directly overwriting. This lets humans quickly see "what changed this time" during Review Checkpoint, and helps agents communicate the scope of changes to each other.

```markdown
## Delta: US-007 Shopping Cart Discount Feature

### Non-Goals (Optional but Recommended)
- This story doesn't handle bulk import of coupons
- Doesn't consider multi-currency discount calculations
- Doesn't modify existing CartService.AddItem() interface

### ADDED
- Module: `DiscountEngine` (Responsibility: calculate discount logic)
- Data Model: `Coupon` table (code, type, value, expires_at)

### MODIFIED
- Module `CartService`: add `applyCoupon(cartId, code)` method
- Data Model `Order`: add `discount_amount` field

### REMOVED
- (None)
```

**Non-Goals section**: List what this story explicitly doesn't do. Agents should check during Implementation whether their changes touch Non-Goals scope and tag with `[SCOPE WARNING]` if they do. Non-Goals is the most efficient strategy to prevent scope creep—eliminating upfront saves far more tokens than fixing afterward.

Delta Spec lifecycle:
1. **Generated**: Each story's SDD incremental update generates a Delta Spec simultaneously
2. **Reviewed**: Humans review Delta Spec during Review Checkpoint to confirm change scope
3. **Merged**: After review approval, Delta content merges into SDD main document
4. **Archived**: Delta file moves to `docs/deltas/` or deleted (per project preference)

### [NEEDS CLARIFICATION] Tag (applies to SDD)

SDD likewise supports `[NEEDS CLARIFICATION]` tags. When agents encounter design decisions they can't determine during SDD incremental updates, tag them and continue with other story work rather than blocking the entire story on a single uncertainty point.

```markdown
### Module: DiscountEngine
- **Responsibility**: Calculate various discounts
- **Discount Priority**: [NEEDS CLARIFICATION: Coupon stacking rules—take best? Apply sequentially? Mutually exclusive?]
- **Dependencies**: CartService, CouponRepository
```

### Writing Principles

**Clear module boundaries**: Each module has clearly defined "responsibility" and "external interface," making it easy to determine the scope of incremental updates for Stories.

**ADR on the fly**: When making controversial technical decisions, record them on the spot in the "Technical Decisions" section. No need to supplement later.

**Incremental-friendly**: New Stories only add or modify sections for affected modules; no need to rewrite the whole document. It's recommended to annotate at the start of each module section which stories introduce/modify it to track the source.

**RFC 2119 keywords**: Constraint descriptions in SDD similarly use RFC 2119 keywords. For example, "module communication SHALL use event-driven" indicates a must-follow requirement, "MAY use Redis cache" indicates optional.

**Data Model is the sole Source of Truth**: The data model section of SDD is the authoritative source for all data structure definitions. API contract `components/schemas` are derived from SDD, DDD Glossary type constraints are derived from SDD. When conflicts appear, SDD data model is authoritative. Agents should check whether contracts and Glossary need corresponding updates when modifying data models.

**System Context description**: The system architecture section should describe not just internal module division but also relationships with external systems (third-party APIs, external databases, message queues, etc.). Visualization with Mermaid `graph` is recommended.

**Mermaid diagram guidance**: Choose appropriate diagram types per scenario—system architecture uses `graph`, data models use `erDiagram`, complex interaction flows use `sequenceDiagram`. Diagrams should be accompanied by text explanations and shouldn't stand alone for information transmission.

---

## API Contract Template

### Positioning

Interface definition for frontend/backend separation projects. REST APIs use OpenAPI 3.0+ format (recommend 3.1, supporting full JSON Schema 2020-12 compatibility), placed in `docs/api/openapi.yaml`; event-driven interfaces (WebSocket, MQTT, etc.) use AsyncAPI 3.0 format, placed in `docs/api/asyncapi.yaml`.

### REST API (OpenAPI Summary)

```yaml
openapi: "3.1.0"   # 3.1 recommended; 3.0.3 also acceptable
info:
  title: <Project Name> API
  version: 0.1.0

paths:
  /api/<resource>:
    get:
      summary: <Brief description>
      tags: [<Module Name>]
      parameters:
        - name: <param>
          in: query
          schema:
            type: string
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/<ResponseModel>'
        '400':
          description: Parameter error
        '401':
          description: Unauthorized

components:
  schemas:
    <Model>:
      type: object
      required: [<field1>, <field2>]
      properties:
        <field1>:
          type: string
          description: <Explanation>
```

### Event-Driven API (AsyncAPI Summary)

```yaml
asyncapi: 3.0.0
info:
  title: <Project Name> WebSocket API
  version: 0.1.0

servers:
  production:
    host: <host>
    protocol: ws
    description: WebSocket server

channels:
  joinRoom:
    address: /ws
    messages:
      joinRoom:
        $ref: '#/components/messages/JoinRoom'
    description: Client joins room

  roomUpdate:
    address: /ws
    messages:
      roomUpdate:
        $ref: '#/components/messages/RoomUpdate'
    description: Server pushes room status

operations:
  sendJoinRoom:
    action: send
    channel:
      $ref: '#/channels/joinRoom'
    summary: Client requests to join room

  receiveRoomUpdate:
    action: receive
    channel:
      $ref: '#/channels/roomUpdate'
    summary: Receive room status update

components:
  messages:
    JoinRoom:
      payload:
        type: object
        required: [roomId]
        properties:
          roomId:
            type: string
            description: Room ID

    RoomUpdate:
      payload:
        type: object
        required: [users, status]
        properties:
          users:
            type: array
            items:
              $ref: '#/components/schemas/User'
          status:
            type: string
            description: Room status

  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
```

### Writing Principles

**Contract first**: Define the API contract first, then both frontend and backend implement against that contract. Agents don't need to "guess" what the interface looks like.

**REST uses OpenAPI, events use AsyncAPI**: Both are machine-readable standard formats that agents can directly parse and generate corresponding type definitions and test skeletons from. Avoid markdown tables to describe APIs—structured formats can be consumed by the tool chain (code generator, mock server, validator).

**Incremental updates**: New Stories only add new endpoints / channels or modify affected parts; don't rewrite the entire contract.

**Payload must be defined**: Whether REST response or WebSocket message, complete data structures must be included. This is key to whether frontend agents can implement independently.

---

## NFR Template

### Positioning

NFR (Non-Functional Requirements) define performance, security, reliability, and other non-functional constraints. Agents by default write "functionally correct" code but won't proactively consider these constraints. The NFR document gives agents explicit thresholds when generating `@perf` / `@load` tests.

Place in `docs/nfr.md` or incorporate into SDD. It's recommended to define the 3 most critical NFRs early (API latency, error rate, authentication), letting agents develop the habit of "adding NFR tests with features," then expand later.

### NFR ID System

Each NFR has a unique ID, which is the connection point between BDD scenarios and NFRs. BDD scenarios reference NFR IDs through `@perf(PERF-01)` syntax. During Test Scaffolding, agents consult the table to get thresholds, tools, and scope, directly generating corresponding test scripts.

The NFR table is the **single source of truth** for thresholds. Inline overriding thresholds in BDD scenarios is not allowed (like `@perf(p95=2000ms)`), to prevent performance standards being scattered across multiple BDD files. If special scenarios need different thresholds, add an independent ID in the NFR table.

### Template

```markdown
# Non-Functional Requirements (NFR)

## Performance (Performance)

| ID | Description | Metric | Threshold | Scope/Regex | Tool | Priority |
|:---|:---|:---|:---|:---|:---|:---|
| `PERF-01` | Fast API response | p95 latency | < 200ms | `/api/v1/*` (exclude `/api/v1/report/*`) | k6 | P0 |
| `PERF-02` | Search high concurrency | VUs, error rate | 1000 users, 0 errors | `/api/v1/search` | k6 | P0 |
| `PERF-03` | Page load speed | LCP | < 2.5s | `/*` (public pages) | Lighthouse CI | P1 |
| `PERF-04` | Report generation (heavy) | p95 latency | < 2000ms | `/api/v1/report/*` | k6 | P1 |

## Security (Security)

| ID | Description | Validation Rule | Scope/Regex | Tool | Notes |
|:---|:---|:---|:---|:---|:---|
| `SEC-01` | Authentication | Bearer Token (JWT) | All non-`/public/*` routes | Integration Test | Must verify 401/403 |
| `SEC-02` | Input sanitization | No XSS / SQL Injection | All POST/PUT body | OWASP ZAP / SonarQube | CI phase scanning |

## Reliability (Reliability)

| ID | Description | Metric | Target | Measurement | Notes |
|:---|:---|:---|:---|:---|:---|
| `REL-01` | System availability | Uptime | 99.5% | Monitoring Alert | Excludes planned maintenance |
| `REL-02` | Error rate | HTTP 5xx rate | < 0.1% | CI + Monitoring | Verify after each deployment |
```

### Agent Execution Flow

```
1. Agent reads BDD scenario, sees @perf(PERF-01) @secure(SEC-01)
2. Consult NFR table:
   - PERF-01 → p95 < 200ms, tool k6, scope /api/v1/*
   - SEC-01  → JWT Bearer Token, verify 401/403
3. Test Scaffolding:
   - Generate k6 script with p95 < 200ms in thresholds
   - Generate Integration Test verifying unauthorized returns 401
4. If current endpoint not in PERF-01 scope (e.g., /api/v1/report/annual)
   → Auto-match PERF-04 (p95 < 2000ms)
```

### Layered Granularity

NFR table defines **global baseline** (Global Defaults). When special scenarios need different standards, don't override in BDD; instead add a new ID in NFR table with clear scope (like `PERF-04` specifically for report generation).

This ensures: performance standards can always be reviewed in one document, agents don't need to scan all BDD files to know "how fast should this API be."

### Writing Principles

**Every entry has an ID**: ID is the connection between BDD ↔ NFR. NFRs without IDs can't be referenced by BDD scenarios, effectively don't exist.

**Scope must be precise**: Use regex or path patterns to define applicable scope, avoiding vague descriptions like "all APIs." Exclusion rules (like "exclude `/report/*`") should be explicit.

**Tool must be specified**: Agents need to know what tool generates test scripts. Specifying `k6`, `Lighthouse CI`, `OWASP ZAP` directly affects the structure of code agents produce.

**Start small then expand**: 3 entries are enough initially (latency, error rate, auth). Add as performance issues arise; don't pursue completeness upfront.

---

## Test Scaffolding Template

### Positioning

Test skeletons generated from BDD scenario tags, with all initial test states being failing (red).

### Template (Go Backend Unit/Integration)

```go
// <module>_test.go
// Generated from: BDD US-XXX — <Scenario Description>
// Tags: @unit

func TestXxx_GivenCondition_WhenAction_ThenResult(t *testing.T) {
	// Given: <Copy precondition from BDD scenario>
	// TODO: setup

	// When: <Copy action from BDD scenario>
	// TODO: execute

	// Then: <Copy expected result from BDD scenario>
	t.Fatal("Not implemented — RED phase")
}
```

### Template (Playwright Component Test)

```typescript
// <component>.spec.ts
// Generated from: BDD US-XXX — <Scenario Description>
// Tags: @component

import { test, expect } from '@playwright/experimental-ct-react';
import { ComponentName } from './ComponentName';

test('<Behavior description copied from BDD scenario>', async ({ mount }) => {
  // Given: <Preconditions>
  // TODO: setup props and context

  // When: <Action>
  const component = await mount(<ComponentName />);
  // TODO: simulate user action

  // Then: <Expected results>
  // TODO: add assertions
  test.fail(); // RED phase
});
```

### testify Pattern Integration (Go Backend)

Test skeletons for Go backends should clearly distinguish `require` (preconditions) from `assert` (verification):

```go
func TestCart_GivenEmptyCart_WhenAddItem_ThenHasOneItem(t *testing.T) {
    // Given — use require (precondition, stop immediately if fails)
    cart, err := NewCart(userID)
    require.NoError(t, err)
    require.NotNil(t, cart)

    // When
    err = cart.AddItem(productID, 1)

    // Then — use assert (verification, report all failures at end)
    assert.NoError(t, err)
    assert.Equal(t, 1, cart.ItemCount())
}
```

**Table-Driven Tests** (corresponds to BDD Scenario Outline):

```go
func TestPasswordStrength(t *testing.T) {
    // Generated from: BDD US-002 — Scenario Outline: Password strength validation
    tests := []struct {
        name     string
        password string
        expected string
    }{
        {"too short", "abc", "At least 8 characters"},
        {"no digits", "abcdefgh", "Need to contain numbers"},
        {"valid", "Abcdefg1", "Pass"},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := ValidatePassword(tt.password)
            assert.Equal(t, tt.expected, result)
        })
    }
}
```

**Suite Pattern** (corresponds to BDD Background shared preconditions):

```go
type CartTestSuite struct {
    suite.Suite
    cart *Cart
    db   *TestDB
}

func (s *CartTestSuite) SetupTest() {
    s.db = NewTestDB(s.T())
    s.cart, _ = NewCart(s.db, testUserID)
}

func (s *CartTestSuite) TearDownTest() {
    s.db.Cleanup()
}

func TestCartSuite(t *testing.T) {
    suite.Run(t, new(CartTestSuite))
}
```

### Template (Playwright Full E2E Test)

```typescript
// e2e/<flow-name>.spec.ts
// Generated from: BDD US-XXX — <Complete user flow description>
// Tags: @e2e
// Milestone: <Milestone Name>

import { test, expect } from '@playwright/test';

test.describe('<User Flow Name>', () => {
  test.beforeEach(async ({ page }) => {
    // Given: Shared preconditions (like login, navigate to start page)
    // TODO: setup
  });

  test('<Behavior description copied from BDD scenario>', async ({ page }) => {
    // Given: <Preconditions>
    // TODO: navigate to starting page

    // When: <Series of operation steps>
    // TODO: simulate user journey

    // Then: <Final expected result>
    // TODO: add assertions
    test.fail(); // RED phase
  });
});
```

E2E tests run when crossing Story milestones (not per Story), covering complete user flows. Difference from Component Tests: E2E requires both frontend and backend to be ready, traversing real APIs and DB.

### Writing Principles

**BDD scenarios traceable**: Each test file opening should note the source BDD scenario number and tags, establishing bidirectional tracing.

**Naming from scenarios**: Test function names use Given/When/Then combinations; don't invent test names independently.

**All red lights**: All tests must fail after skeleton generation. If tests unexpectedly pass, the test isn't specific enough.

**require vs assert**: Preconditions in Given blocks use `require` (stop immediately if fail, don't waste time on subsequent steps); verification in Then blocks use `assert` (check everything then report all failures once).

**Extract Helper Functions**: When two or more tests share identical Given setup, extract to `setupXxx(t *testing.T)` helper. When three or more tests share identical assertion patterns, extract to `assertXxx(t *testing.T, ...)` helper. Helper names are derived from BDD scenario descriptions (like `setupCartWithItems`, `assertOrderTotal`).

---

## DDD Format Guide

### Positioning

DDD (Domain-Driven Design) is an optional extension to the [Framework](Framework.md), triggered when the project involves multiple business domains. This section defines concrete document formats for three levels.

### Gradual Splitting Strategy

DDD document locations evolve with project scale; no need to separate into directories from the start:

| Project Scale | Determination Criteria | Location | Rationale |
|----------|----------|----------|------|
| Small / MVP | < 3 Contexts, code < 5000 lines | Embedded in `SDD.md` as sections | Agent reads complete picture in one pass, fewer file reads |
| Large / Complex | ≥ 3 Contexts, or multiple agents in parallel | Separate `docs/ddd/` directory | Prevents SDD exceeding context window; agents only load current Context |

Splitting is triggered when: SDD length causes agent context window to not fit the complete document, or multiple agents each own a Context.

### Level 1 — Bounded Context Map

Define each Context's boundary, responsibility, and communication. Text + Mermaid diagrams let agents both parse structure and understand dependencies.

```markdown
# Bounded Context Map

## Visualization of Relationships

~~~mermaid
graph TD
    Sales[Sales Context] -->|OrderPlaced Event| Shipping[Shipping Context]
    Sales -->|PaymentAuthorized Event| Billing[Billing Context]

    subgraph "Core Domain"
        Sales
    end

    subgraph "Supporting Domain"
        Shipping
        Billing
    end
~~~

## Context Definitions

| Context | Responsibility | Type | Path | External Contract | Notes |
|---------|------|------|------|----------|------|
| Sales | Product catalog, shopping cart, checkout | **Core** | `/src/sales/` | `docs/api/sales-openapi.yaml` | Core business, high change frequency |
| Shipping | Inventory deduction, shipment generation | **Supporting** | `/src/shipping/` | `docs/api/shipping-openapi.yaml` | Triggered by Sales events |
| Billing | Payment processing, invoicing | **Supporting** | `/src/billing/` | `docs/api/billing-openapi.yaml` | Triggered by Sales events |
| Auth | Authentication, authorization | **Generic** | `/src/auth/` | `docs/api/auth-openapi.yaml` | Prefer existing solutions |

### Subdomain Types and Agent Behavior Rules

| Type | Explanation | Agent Behavior |
|------|------|-----------|
| **Core** | Project's core competence, high change | Highest test coverage, Delta Spec + ADR mandatory, deep review |
| **Supporting** | Supports core business, medium change | Standard test coverage, Delta Spec mandatory |
| **Generic** | Generic functionality, low change | Prefer existing solutions (library / service), minimal test coverage okay |

## Interaction Patterns (Integration Patterns)

| Upstream | Downstream | Relationship Type | Interface | Pattern |
|------|------|----------|------|------|
| Sales | Shipping | Customer-Supplier | Event: `OrderPlaced` | ACL (Anti-Corruption Layer), async |
| Sales | Billing | Customer-Supplier | Event: `PaymentAuthorized` | ACL, async |
| Frontend | Sales | — | REST API | OHS (Open Host Service) |
```

### Level 2 — Glossary (Ubiquitous Language)

Ubiquitous language table that forces agents to consult when naming variables and fields. Add "type/constraint" column so agents don't need to guess when outputting DB Schema and API DTOs.

```markdown
# Ubiquitous Language (Glossary & Data Dictionary)

> Instruction: All agents must strictly follow this table when naming variables, database fields, API parameters. Using synonyms is prohibited.

| Term | Sales Context Definition | Shipping Context Definition | Type/Constraint | Example Value |
|------|-------------------|----------------------|-----------|--------|
| User | `Customer` (order placer) | `Recipient` (receiver) | UUID (v4) | `550e8400-e29b...` |
| Order | `SalesOrder` (with amount details) | `ShippingOrder` (with weight and volume) | String `ORD-{Timestamp}` | `ORD-2026021301` |
| Address | Billing address (Billing) | Delivery address (Delivery) | JSON Structure | `{ "zip": "100", ... }` |
| Item | Product (with price snapshot) | Package contents (with volume) | Array | — |
```

### Level 3 — Aggregate Root (embedded in SDD)

Aggregate Root belongs to tactical design, embedded directly in SDD module sections. Mark blocks with `[DDD Tactical Constraint]` so agents immediately recognize immutable rules and access restrictions.

```markdown
## Module: Sales Context

### Core Entities

> **[DDD Tactical Constraint]**
> - **Aggregate Root:** `Order`
> - **Invariant:** Order total amount must equal sum of details; once Order is Confirmed, details cannot be modified.

#### Order (Aggregate Root)
- **Attributes:**
  - `id`: UUID
  - `status`: Enum (DRAFT, CONFIRMED, SHIPPED)
  - `items`: List<OrderItem>
- **Methods:**
  - `addItem(product, quantity)`: Must check inventory
  - `confirm()`: Trigger `OrderPlaced` event

#### OrderItem (Local Entity)
- **Access:** Only accessible through `Order`; prohibited from direct Repository queries.
```

### Domain Event Registry (Optional, applies to event-driven architecture)

When the project uses event-driven cross-Context communication, it's recommended to maintain a central Domain Event list in the DDD document. This lets agents know what events exist in the system without searching across multiple files.

```markdown
## Domain Event Registry

| Event | Sender | Receiver | Payload | Trigger Timing |
|-------|--------|--------|---------|---------|
| `OrderPlaced` | Sales | Shipping, Billing | `{orderId, items, totalAmount}` | After order confirmation |
| `PaymentAuthorized` | Billing | Sales | `{orderId, transactionId}` | After successful payment |
| `ShipmentCreated` | Shipping | Sales | `{orderId, trackingNumber}` | After shipment creation |
```

Event Registry is a high-level summary of AsyncAPI contract. When agents incrementally update SDD, if they add or modify cross-Context events, they should synchronously update this table.

### Writing Principles

**Context Map is global**: Whether in SDD or separate directory, Context Map and Glossary are shared references for all agents. Every agent should consult before starting work to confirm which Context they're in.

**Glossary is naming enforcement**: Agents must not invent synonyms. "Sales Context's User is called Customer" means Customer, not Buyer, Client, or Purchaser.

**Aggregate Root constraints mark implementation boundaries**: Blocks marked `[DDD Tactical Constraint]` must be respected when implementing; agents can't circumvent Aggregate Root to operate on child entities directly.

**Mermaid and tables complement each other**: Mermaid lets agents quickly grasp dependency topology; tables provide precise path, contract, and type details. Both are necessary; neither alone is sufficient.

---

## Constitution Template (Project Constitution)

### Positioning

Constitution defines **immutable architectural principles** of the project. Difference from ADR: ADR records historical context of "why A not B"; Constitution extracts hard constraints that apply across all Stories and always. Agents should check Constitution before any design decisions to ensure no violations.

Place in `docs/constitution.md` or embed in project entry document. Recommend starting with 3-5 entries, expanding as project evolves.

### Template

```markdown
# Project Constitution

> The following principles always apply across all stories and all agents. Violating any is a bug, regardless of functional correctness.

## Architectural Principles

1. **API-First**: All module communication SHALL happen through defined API contracts; direct cross-module database access is prohibited.
2. **Stateless Services**: Backend services SHALL be stateless; state SHALL be stored in database or Redis.
3. **Event-Driven Decoupling**: Cross-Bounded Context communication SHALL use events; synchronous RPC is prohibited.

## Security Principles

4. **Auth Everywhere**: All non-`/public/*` routes SHALL verify JWT Token (corresponds to SEC-01).
5. **Input Validation**: All external input SHALL be sanitized (corresponds to SEC-02).

## Quality Principles

6. **Test Coverage Gate**: New features SHALL include corresponding test coverage at appropriate level; CI coverage must not drop below current baseline.
7. **No Silent Failures**: All errors SHALL be logged and return appropriate HTTP status codes.
```

### Writing Principles

**Only immutable principles**: Constitution is not a coding style guide. Only include principles that, if violated, cause architectural issues. "Should use camelCase" doesn't belong here; "no cross-module direct DB access" does.

**Use SHALL / MUST**: Every principle in Constitution is RFC 2119 SHALL level. If a principle is SHOULD, it shouldn't be in Constitution—put it in SDD writing guidelines instead.

**Link to NFR IDs**: Security and performance related principles should reference corresponding NFR IDs, establishing bidirectional tracing.

**Evolves but not easily changed**: Modifying Constitution entries counts as architectural change and should have corresponding ADR documentation of change reasoning.

---

## Review Checkpoint Template

### Positioning

Review Checkpoint is the human review point before implementation in micro waterfall. Orchestrator (or agent) produces structured Review summary at this step, letting humans quickly judge if the direction is correct.

### Template

```markdown
# Review Checkpoint — US-XXX <Story Title>

## Change Summary
- **BDD Scenario Count**: N (N @unit, N @integration, N @e2e)
- **Delta Spec**: N ADDED, N MODIFIED, N REMOVED
- **Contract Changes**: N new endpoints, N modified

## Pending Clarification Items
| # | Source | Issue | Suggestion |
|---|------|------|------|
| 1 | BDD scenario 3 | [NEEDS CLARIFICATION] Relevance sorting method undefined | Suggest TF-IDF |
| 2 | SDD Delta | [NEEDS CLARIFICATION] Multiple coupon stacking rules | Suggest take best |

## Non-Goals Confirmation
- This story doesn't handle: <list>
- Is the above scope correct?

## Risks and Considerations
- <Identified risks or dependencies>

## Review Conclusion
- [ ] BDD scenarios direction is correct
- [ ] Delta Spec scope is reasonable
- [ ] Contract changes are non-breaking
- [ ] Pending clarifications addressed
```

### Writing Principles

**Scannable**: Humans should grasp the Review focus in 30 seconds. List pending clarifications in tables, not long descriptions.

**Comes with suggestions**: Each `[NEEDS CLARIFICATION]` item includes agent's suggested solution; human only needs to confirm or correct, not think from scratch.

**Review conclusion is checklist**: Humans can just check; reduces cognitive load of reviewing.

---

## Story Task Format Guide

### [P] Parallel Marking

When a Story's implementation can be split into multiple independent subtasks, mark parallelizable items with `[P]`. This is especially useful in multi-agent collaboration or human-machine division—`[P]` marked tasks can proceed simultaneously; unmarked tasks must follow sequence.

```markdown
## US-007 Shopping Cart Discount Feature — Tasks

1. [ ] Define Coupon data model + migration
2. [P] CouponRepository CRUD implementation + unit test
3. [P] DiscountEngine discount calculation logic + unit test
4. [ ] CartService.applyCoupon() integration + integration test
5. [ ] Frontend discount code input component + component test
```

Tasks #2 and #3 are marked `[P]`, meaning they're independent and can proceed simultaneously. Task #4 depends on completion of #2 and #3, so it's not marked `[P]`.

### Complexity Tracking

Each Story can be annotated with complexity level, helping humans estimate effort during Sprint planning and letting agents know expected implementation depth.

| Level | Marker | Expected Scope | Agent Behavior |
|------|------|----------|-----------|
| Simple | `[S]` | Single module change, < 3 files | Implement directly, minimal review |
| Medium | `[M]` | Cross-module, 3-8 files | Needs Delta Spec, standard review |
| Complex | `[L]` | Architectural change, > 8 files | Needs Delta Spec + ADR, deep review |

Marker goes after Story title: `US-007 Shopping Cart Discount Feature [M]`

---

## Legacy Project Reverse Engineering Process

### Positioning

Reverse generate documents required by the framework from existing codebase, letting subsequent development enter the normal BDD → SDD → TDD workflow.

### Steps

```
1. Scan project structure
   - Agent reads directory tree, package.json / go.mod configs
   - Produce initial technology stack description

2. Reverse generate project summary
   - Infer Why / Who / What from README and main code entry
   - Human reviews and supplements

3. Reverse generate SDD
   - Agent scans main modules, routes, data models
   - Produce module division and data model drafts
   - Human supplements implicit architectural decisions (record in ADR)

4. Initialize PROJECT_MEMORY.md
   - Record current git commit hash
   - Set NOW and NEXT
   - Create .ai/history.md (empty)

5. Normal flow
   - Subsequent new features enter BDD → SDD → TDD workflow
   - Each Story uses Step 0 (Safety Net Check) to add characterization
     tests for functions being modified, if they lack coverage
```

**Note:** Characterization tests are NOT written all at once during Bootstrap. Use the "touch it, test it" approach — only add characterization tests when a Story touches uncovered code. See Step 0 in the [Lifecycle Document](Lifecycle.md).

### Considerations

**Don't miss implicit knowledge**: Some architectural decisions can't be read from code. For example, "polling instead of WebSocket is used because target devices don't support it." Such information must be manually added to SDD by humans.

**Characterization Test ≠ Ideal Behavior**: If existing behavior has bugs, Characterization Tests still describe existing behavior. Bug fixes become subsequent stories.

---

## Changelog

| Version | Date | Changes |
|------|------|----------|
| v0.1 | 2026-02-13 | Initial: establish all templates (PROJECT_MEMORY, project entry, BDD, SDD, API contracts, Test Scaffolding, legacy project reverse engineering process) |
| v0.2 | 2026-02-13 | WebSocket contract updated to AsyncAPI 3.0 format |
| v0.3 | 2026-02-13 | Add NFR template (including ID system, agent execution flow, layered granularity); BDD tag expansion supports ID syntax `@perf(PERF-01)` |
| v0.4 | 2026-02-13 | Add DDD format guide (gradual splitting strategy, Level 1 Context Map with Mermaid, Level 2 Glossary with type constraints, Level 3 Aggregate Root embedded in SDD); Memory conflict resolution strategy references Lifecycle |
| v0.5 | 2026-02-13 | Redesign Memory template: compressed format (62% token savings), HTML comment machine marker, three-phase hierarchical loading, English uppercase section names; add Section explanation table (including authoritative source and update frequency) |
| v0.6 | 2026-02-13 | Adopt OpenSpec / Spec Kit design: BDD adds RFC 2119 keyword strength + [NEEDS CLARIFICATION] marking; SDD adds Delta Spec incremental update format + [NEEDS CLARIFICATION] marking + RFC 2119 keywords; add Constitution template (project constitution); add [P] parallel marking + Complexity Tracking (Story task format guide) |
| v0.7 | 2026-02-13 | Apply refinement checklist 13 items: BDD adds Scenario Outline template, declarative style guidance, Non-Goals section, anti-pattern list; SDD adds Source of Truth principle, System Context description, Mermaid diagram guidance, Delta Spec Non-Goals; Test adds testify require/assert distinction, Table-Driven template, Suite template, Helper Function extraction principle; DDD adds Subdomain type classification (Core/Supporting/Generic) + agent behavior rules, Domain Event Registry |
| v0.8 | 2026-02-13 | Apply Windsurf Review: add Review Checkpoint structured template (P1); recommend API contract upgrade to OpenAPI 3.1 (P2); add Playwright Full E2E Test template (P2) |
| v0.9 | 2026-02-16 | Field feedback: PROJECT_MEMORY slimmed (DONE/LOG → .ai/history.md); add Full/Lite mode templates; add .ai/history.md template; CLAUDE.md template adds mode line + Lite variant; Legacy reverse engineering removes one-time characterization tests, replaced by per-Story Step 0 |
