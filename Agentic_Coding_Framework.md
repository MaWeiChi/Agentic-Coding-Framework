# Agentic Coding Framework

**Project Context Infrastructure for AI-Assisted Development**

Discussion Summary | February 2026

---

## Related Documents

| Document | Content | Agent Load Timing |
|----------|---------|------------------|
| This Document | Framework Foundation: Layered Definition, Core Principles, Process | Read Every Conversation |
| [Agentic_Coding_Lifecycle.md](Agentic_Coding_Lifecycle.md) | Operating Mechanism: Iteration Model, Test Strategy, CI/CD Interface | Load When Planning Iteration or Setting Up CI |
| [Agentic_Coding_Templates.md](Agentic_Coding_Templates.md) | Framework Details: Document Templates for Each Layer, Writing Guidelines, Examples | Load When Writing BDD/SDD/Contract/Memory |
| [Agentic_Coding_Protocol.md](Agentic_Coding_Protocol.md) | Communication Protocol: State Management and Automation Between Orchestrator ↔ Executor | Load When Setting Up Automation or Integrating Orchestrator |
| PROJECT_MEMORY.md (Project Level) | Dynamic State Tracking: Progress, Tasks, Test Status, Git Verification | Read Every Conversation (Paired With Project Summary) |

---

## Core Concept

In the context of Agentic Coding, tokens are cost. Establishing good "context infrastructure" for the project early on can significantly reduce repeated explanations in each subsequent conversation, lowering overall development costs.

The essence of this framework is forcing projects to make implicit knowledge explicit. If the project itself is unclear to humans reading it, agents won't understand it either. Therefore, this framework simultaneously serves AI and human team members' onboarding needs.

---

## Framework Layers

### Layer One: Project Summary

Use a few sentences to let agents quickly locate core project information. It's recommended to place this in the project root directory (such as `CLAUDE.md` or `PROJECT_CONTEXT.md`), and agents should read it once each time a conversation is opened.

- **Why** — Project Purpose: What problem does it solve?
- **Who** — Users: Who is it for?
- **What** — Deliverable: What is the final output?

### Dynamic State Layer: PROJECT_MEMORY.md

Project Summary records stable, unchanging Why / Who / What, while PROJECT_MEMORY.md records continuously changing "where we are now, what's next." Both should be read together each conversation by agents.

Memory is a file independent of any specific AI tool, placed in the project root directory. It includes a git commit verification mechanism that allows agents to detect unrecorded changes when switching between tools and automatically sync. Update timing is defined in the [Lifecycle Document](Agentic_Coding_Lifecycle.md), and template definitions are in the [Templates Document](Agentic_Coding_Templates.md).

### Layer Two: BDD (Behavior-Driven Development)

Describes user behavior and expected results using Given / When / Then format. Particularly useful for agents because it simultaneously serves as both requirements specification and acceptance criteria—agents can directly verify their code against BDD scenarios after writing.

Coarser granularity, corresponding to user scenarios. BDD scenarios use RFC 2119 keywords (SHALL/MUST/SHOULD/MAY) to distinguish requirement strength, and include test level tags (`@unit`, `@integration`, `@component`, `@e2e`, `@perf`, `@load`). Performance and security tags support NFR ID syntax (such as `@perf(PERF-01)`, `@secure(SEC-01)`), and agents look up the NFR table during Test Scaffolding to get thresholds. When requirements are unclear, agents mark `[NEEDS CLARIFICATION]` to pause that scenario pending Review Checkpoint clarification. Details see the test strategy section in the [Lifecycle Document](Agentic_Coding_Lifecycle.md) and BDD/NFR templates in the [Templates Document](Agentic_Coding_Templates.md).

### Layer Three: SDD (Software Design Document)

Defines architectural decisions, technology selection, and module boundaries. Prevents agents from having to "guess" what framework you want to use or how data flows.

BDD scenarios are decomposed into required modules and interfaces, all recorded in the SDD. Incremental updates for each Story use **Delta Spec** format (ADDED / MODIFIED / REMOVED), making change scope clear for review. Details see the SDD template in the [Templates Document](Agentic_Coding_Templates.md).

### Interface Layer: OpenAPI / AsyncAPI Contract

For frontend-backend separated projects, specific interface definitions allow agents to implement without guessing what the interface looks like when handling front-end and back-end. REST APIs use OpenAPI format, event-driven interfaces (WebSocket, MQTT, etc.) use AsyncAPI format.

### Review Checkpoint (Human Review)

A clear review point before entering implementation. At this point, BDD, SDD, and API contracts have all been produced, and humans can intervene to confirm the direction is correct. This is the lowest-cost phase for changes—once implementation begins, the cost of going back to modify the SDD becomes much higher.

### Layer Four: TDD (Test-Driven Development)

Divided into two clear steps:

**Test Scaffolding (Red Light):** Based on BDD scenario tags and API contracts, first produce corresponding level test file skeletons. At this point, there is no implementation code; all tests fail. The value of this step is proving the agent understands the requirements.

**Implementation (Green Light):** Agents read SDD, API contracts, and failing test logs, writing minimal code to pass tests, then refactor. Each round, agents can run tests themselves to verify without human intervention, which is the most token-efficient place.

**Verify (Quality Gate):** After Implementation completes and before updating Memory, agents automatically execute three-point verification—Completeness (all BDD scenarios have tests, all Delta Specs are implemented), Correctness (tests pass, NFRs meet threshold), Coherence (SDD merged with Delta, API contracts consistent with implementation, Constitution not violated). All three must pass before proceeding. Details see the Verify step in the [Lifecycle Document](Agentic_Coding_Lifecycle.md).

---

## Optional Extensions

### ADR (Architecture Decision Records)

SDD records "what the current architecture looks like," ADR records "why we chose A instead of B." Prevents agents from "helpfully refactoring" and breaking designs with specific reasons. Can be incorporated into SDD, not necessarily requiring a separate file.

Best timing to generate: When you make a controversial decision, record it on the spot.

### DDD Strategic Design (Domain-Driven Design Strategic Design)

Triggered when projects involve multiple business domains where the same term represents different concepts in different modules. Located after the project summary and before BDD, used to define agent work boundaries.

Recommend lightweight DDD with three levels progressing from shallow to deep:

- **Level 1 (Recommended):** Bounded Context—Split the system into independent modules, each Context with its own API contract and folder structure. Solves agent context overflow issues; agents only need to read current Context content.
- **Level 2 (Recommended):** Ubiquitous Language—Establish a `glossary.md` common language table, forcing agents to consult it when naming variables and fields. Solves concept confusion issues, such as "User in Sales Context is called Customer, User in Shipping Context is called Recipient."
- **Level 3 (Optional):** Aggregate Root—Mark aggregate roots in SDD, constraining agents to operate data only through aggregate roots, improving encapsulation.

Trigger conditions: Project has cross-domain name conflicts, single Context Window can't fit the entire codebase, or multiple agents need to each handle one module. Single-domain projects can skip.

DDD document location uses progressive splitting strategy: Small projects incorporated into SDD, medium/large projects separated into `docs/ddd/` directory. Specific format and templates detailed in DDD format guidelines in the [Templates Document](Agentic_Coding_Templates.md).

### Constitution (Project Constitution)

Defines architectural principles that cannot be violated in the project—hard constraints that hold across all Stories, all agents, always. Difference from ADR: ADR records historical decision context, Constitution extracts eternal immutable rules. Agents should check Constitution before making any design decisions.

Applicable timing: When project has clear architectural red lines (such as "prohibit direct cross-module DB access" "all services must be stateless"). Recommend defining 3-5 core principles at Bootstrap. Each principle in Constitution is RFC 2119 SHALL level. Specific templates detailed in Constitution template in the [Templates Document](Agentic_Coding_Templates.md).

### NFR (Non-Functional Requirements)

Performance, security, availability constraints. Agents by default write "functionally correct" code but won't proactively consider these non-functional constraints.

Recommend adding them when actually encountering problems during development; no need to pursue completeness at the start. Each NFR has a unique ID (such as `PERF-01`, `SEC-01`), BDD scenarios reference through `@perf(PERF-01)` syntax, and agents look up the NFR table during Test Scaffolding to get thresholds. The NFR table is the single source of truth for thresholds. Specific templates detailed in NFR template in the [Templates Document](Agentic_Coding_Templates.md).

### Complexity Tracking (Story Complexity Tracking)

Each Story is marked with complexity level (`[S]` Simple / `[M]` Medium / `[L]` Complex), helping Sprint planning assess workload and letting agents know expected implementation depth and Review intensity. Complex Stories require Delta Spec + ADR + Deep Review; Simple Stories can be implemented directly. Specific definitions detailed in Story task format guidelines in the [Templates Document](Agentic_Coding_Templates.md).

---

## New Projects vs. Existing Projects

Regardless of project age, all eventually converge to the same set of documents as the agent's working foundation. The only difference is the output path.

### New Project Flow

Define upfront, proactively construct context for agents.

| Step | Description |
|------|-------------|
| Project Summary | Define Who / What / Why |
| BDD | Write user behavior scenarios |
| SDD | Define architecture and module division |
| OpenAPI / WS | Establish front-end/back-end interface contracts |
| **Review Checkpoint** | **Human review confirms correct direction** |
| Test Scaffolding | Produce test skeletons (all red lights) |
| Implementation | Implement to pass tests → Refactor |

### Existing Project Flow

Extract backwards, reverse-engineer documents from existing codebase.

| Step | Description |
|------|-------------|
| Scan Codebase | Agent reads project structure, key files |
| Reverse-Engineer Documents | Produce project summary + BDD + SDD |
| Manual Correction | You confirm and supplement implicit knowledge |
| Add Characterization Tests | Describe existing behavior, establish baseline |
| Normal Flow | Subsequent new features enter BDD → SDD → TDD |

Additional considerations for existing projects: Some implicit architectural decisions or technical debt are unreadable from code by agents and need manual addition to SDD, preventing agents from "helpfully refactoring" and breaking designs.

---

## Core Principles

| Principle | Explanation |
|-----------|-------------|
| More stable information fixed earlier | Agents don't need repeated inference; each conversation only processes differences |
| Load on demand | Frequently used information in CLAUDE.md, occasionally needed in separate files |
| Dual reporting | Simultaneously serve AI agents and human team members |
| ADR / NFR / DDD can be iteratively supplemented | No need to pursue completeness at start; supplement when hitting issues |
| Scale determines depth | Small CRUD needs only four layers; distributed systems need more documents |
| Don't guess, mark uncertainties | When encountering ambiguity, mark `[NEEDS CLARIFICATION]`, don't self-infer requirements |
| Incremental not rewrite | SDD updates use Delta Spec format, avoiding full rewrites losing decisions |

---

## Considerations for Gemini's "Agentic Waterfall" Proposal

The discussion referenced Gemini's proposed role division (Product Manager Agent, Architect Agent, QA Agent, Coder Agent) solution. After evaluation, the conclusion:

**Absorbed portions:** Review Checkpoint concept (incorporated into framework), Test Scaffolding first (incorporated into TDD phase).

**Independent Issue:** Role division (Agent Teams). This framework defines "what documents the project needs, what order to produce them," independent of whether ultimately executed by one agent or multiple agents. The framework is the work blueprint; agent teams are the execution structure; both can be discussed independently and don't conflict when combined. Self-correction loop is essentially the TDD cycle itself; no additional framework needed.

---

## Topics for Future Discussion

The following topics can be explored more deeply in subsequent discussions:

**Framework Details (Incorporated into [Templates Document](Agentic_Coding_Templates.md)):**
- ~~Specific templates and examples for each layer~~ (v0.8, all Templates templates)
- ~~Best practices for writing BDD scenarios~~ (v0.8, includes RFC 2119, Scenario Outline, Anti-Pattern)
- ~~Minimum necessary information for SDD~~ (v0.8, includes Delta Spec, Source of Truth, Mermaid guidance)
- ~~CLAUDE.md structure design~~ (v0.8, PROJECT_CONTEXT.md template)
- ~~Reverse engineering process for existing projects~~ (v0.8, six-step reverse engineering)
- ~~How agents automatically derive TDD test cases from BDD and SDD~~ (v0.8, Test Scaffolding template + tag-driven)

**Iteration Mechanism and Development Lifecycle (Incorporated into [Lifecycle Document](Agentic_Coding_Lifecycle.md)):**
- ~~Execution granularity: micro-level waterfall cycles per User Story~~ (v0.4)
- ~~Incremental update strategy for SDD and API contracts~~ (v0.4)
- ~~Macro agile vs. micro waterfall operation~~ (v0.5)
- ~~Story dependency handling strategy~~ (v0.5)
- ~~E2E test strategy~~ (v0.6)
- ~~CI/CD and framework interface~~ (v0.7)
- ~~DevOps trust boundary~~ (v0.7)
- ~~How to connect above process with this framework into complete development lifecycle~~ (v0.8, Lifecycle document defines complete micro waterfall cycle)

**Agent Protocol (Incorporated into [Protocol Document](Agentic_Coding_Protocol.md)):**
- ~~Load rules: which layer files agents can load at different stages~~ (v0.14, Step conversion rule table `claude_reads`)
- ~~Handoff rules: state passing and handoff between agents~~ (v0.14, three-file protocol STATE.json + HANDOFF.md + PROJECT_MEMORY.md)
- ~~Reference implementation: OpenClaw × Claude Code~~ (v0.14, includes Dispatch logic, Hook mechanism, Reason-Based Routing)
- ~~Output rules: Diff-Only Output (only output changes, don't repeat entire files), prioritize structured format~~ (v0.16, Executor output rules + HANDOFF.md hybrid format)
- ~~Agent Teams role definition and division (multi-executor collaboration)~~ (v0.15, Multi-Executor collaboration mode + Claude Code Agent Teams experimental reference implementation)

**Project Level (Not incorporated into framework, recorded in individual project SDD):**
- Specific CI/CD pipeline configuration (GitHub Actions YAML, Dockerfile, etc.)

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2026-02-13 | Initial version: Establish four-layer core framework (Project Summary → BDD → SDD → TDD), confirm dual pathways for new/existing projects, define optional extensions (ADR / NFR) |
| v0.2 | 2026-02-13 | Incorporate Gemini "Agentic Waterfall" recommendations: Add Review Checkpoint, divide TDD into Test Scaffolding + Implementation |
| v0.3 | 2026-02-13 | Clarify role division (Agent Teams) as independent issue; incorporate Gemini "macro agile / micro waterfall" perspective, list as future discussion topics; correct project summary to Why / Who / What |
| v0.4 | 2026-02-13 | Add "Execution Granularity and Iteration Model": Define one-time Bootstrap + User Story micro waterfall cycle, clarify SDD and API contracts as incremental updates not rewrites |
| v0.5 | 2026-02-13 | Expand "Execution Granularity and Iteration Model": Add two-layer macro agile × micro waterfall structure explanation, Story dependency handling strategies (technical / functional / dynamic discovery), internal interface definition during Bootstrap, vertical slice heuristic rules |
| v0.6 | 2026-02-13 | Add "Test Strategy": BDD scenario tags (@unit / @integration / @component / @e2e / @perf), five-layer test pyramid definition, test timing and micro waterfall integration, Go backend + Playwright frontend toolchain |
| v0.7 | 2026-02-13 | Add "CI/CD and Framework Interface": BDD tag-driven CI trigger timing, Agent trust boundary (responsible up to image push, not intervening in deployment), CD difference handling principles for different project types |
| v0.8 | 2026-02-13 | Split documents: Move operating mechanism to Lifecycle document, framework details to Templates document; main document simplified to framework foundation + cross-references |
| v0.9 | 2026-02-13 | Add optional extension "DDD Strategic Design": Lightweight three-level (Bounded Context / Ubiquitous Language / Aggregate Root), positioned as conditionally triggered, enabled when projects involve multiple business domains |
| v0.10 | 2026-02-13 | Package as Cowork Skill (Chinese version): SKILL.md + references/framework.md + references/lifecycle.md (repackage after Templates completion) |
| v0.11 | 2026-02-13 | Add "Dynamic State Layer: PROJECT_MEMORY.md": Positioned as independent cross-tool state tracking file separate from specific AI tools, includes git commit verification mechanism; update related document tables |
| v0.12 | 2026-02-13 | Expand BDD tags to support NFR ID syntax; Add ID system explanation to NFR; Add progressive splitting strategy and Templates reference to DDD; Rename interface layer to OpenAPI / AsyncAPI |
| v0.13 | 2026-02-13 | Absorb OpenSpec / Spec Kit design: Add RFC 2119 keyword strength levels + [NEEDS CLARIFICATION] marking to BDD; Add Delta Spec incremental update format to SDD; Add Verify quality gate to TDD; Add optional extensions Constitution (Project Constitution) + Complexity Tracking (Story Complexity Tracking) |
| v0.14 | 2026-02-13 | Add fourth core document [Agentic_Coding_Protocol.md](Agentic_Coding_Protocol.md): Orchestrator × Executor communication protocol, three-file protocol (STATE.json / HANDOFF.md / PROJECT_MEMORY.md), Step conversion rule table, Dispatch logic, Hook mechanism, Reason-Based Routing, OpenClaw × Claude Code reference implementation |
| v0.15 | 2026-02-14 | Protocol adds Multi-Executor collaboration mode (three-layer architecture, Complexity-Based Dispatch, Scoped Context, Role-Based isolation, Per-Task HANDOFF) + Claude Code Agent Teams experimental reference implementation; four refinement items formally incorporated (dynamic context loading, Test/Impl isolation, Agent subscription mechanism, handoff format) |
| v0.16 | 2026-02-14 | Protocol adds Executor output rules (Diff-Only principle, prioritize structured format, per-step output strategy); HANDOFF.md upgraded to hybrid format (YAML front matter + Markdown body) |
| v0.17 | 2026-02-14 | Apply Windsurf Round 2 Review: All "topics for future discussion" items crossed off (6 framework detail items + Lifecycle integration); Protocol upgraded to v0.6 (Hook YAML parsing, Dispatch Prompt hybrid format, team_roles completion, STATE.json schema update) |
