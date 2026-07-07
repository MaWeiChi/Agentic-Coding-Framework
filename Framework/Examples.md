# Agentic Coding Examples

**One small capability, followed through two Stories — every artifact shown complete (FB-025)**

Templates show fragments; this document shows the real thing. One capability (`CART`)
across two Stories: US-007 introduces discount codes; US-012 replaces the flat discount
with tiered rates and removes gift-wrap. You see (1) a finished three-section delta file
exactly as it looks at the Review Checkpoint, and (2) the capability spec exactly as it
looks after both deltas have merged — including a tombstone and an exempted Requirement.

---

## 1. A complete delta file — `docs/deltas/US-012.md` (in flight)

This is the whole file at Step 4 (Review Checkpoint), all three top-level sections.
On Verify pass, sections 1–2 merge, section 3 is skipped, and the file moves to
`docs/deltas/archive/2026-06-13-US-012.md` (FB-015/016).

```markdown
## Behavior Delta — US-012: Tiered Discounts

### ADDED Requirements

### Requirement: Discount rate scales with cart subtotal [R-CART-004]
The system SHALL apply the highest tier whose threshold the cart subtotal meets.

#### Scenario: subtotal crosses a tier boundary (Test Level: integration)
- Given tiers are {50: 5%, 100: 10%} and the cart subtotal is 99.00
- When the customer adds an item priced 1.00
- Then the applied discount rate SHALL change from 5% to 10%

#### Scenario: no tier met (Test Level: integration)
- Given tiers are {50: 5%, 100: 10%} and the cart subtotal is 30.00
- When the order total is calculated
- Then no discount SHALL be applied

**Parameters**:
| Parameter | Type | Unit | Range | Default | Example | R/W | Notes |
|-----------|------|------|-------|---------|---------|-----|-------|
| tierThresholds | number | currency | 0 - (none) | 50, 100 | 50 | RW | Ascending; duplicate thresholds rejected |
| tierRates | number | % | 0 - 90 | 5, 10 | 10 | RW | Paired 1:1 with tierThresholds |

**Error Cases**: thresholds not ascending → reject config; rate > 90 → reject config

### MODIFIED Requirements

### Requirement: Discount codes apply at checkout [R-CART-001]
The system SHALL apply a valid discount code's rate after tier discounts are applied.
(Previous behavior: code rate applied to the raw subtotal — tiering did not exist.)

#### Scenario: code stacks on tier discount (Test Level: integration)
- Given the cart qualifies for a 10% tier discount and a valid code SAVE5 (5%)
- When the order total is calculated
- Then the code SHALL apply to the tier-discounted amount (not the raw subtotal)

### REMOVED Requirements
- [R-CART-002] Gift-wrap option — product decision 2026-06: gift-wrap moves to the
  fulfilment service; cart no longer owns it

## SDD Delta — US-012: Tiered Discounts

### Non-Goals
- No currency conversion; tiers are in the store currency only
- No per-customer tier overrides

### ADDED
#### Module: TierEngine
- **Purpose:** resolve the applicable tier for a subtotal
- **Interface:** `resolve(subtotal Money) (rate Percent, ok bool)`
- **Data model:** `tiers []Tier{Threshold Money, Rate Percent}` — owned here (Source of Truth)

### MODIFIED
#### Module: DiscountEngine
- **Change:** applies code rate after TierEngine's rate
- **Reason:** R-CART-001 modified — codes now stack on tiers
- **Impact:** CartService.total() call order; 2 integration tests re-pointed

### REMOVED
#### Module: GiftWrap
- Removed with R-CART-002; fulfilment service owns gift-wrap now

## Review Disclosure — US-012: Tiered Discounts

### Assumptions Made
| # | Assumption | Basis |
|---|-----------|-------|
| 1 | Code rate stacks multiplicatively (not additively) on tier rate | Finance glossary defines "combined discount" as sequential application |

### Source Mapping
| Source Item | Handling | Note |
|-------------|----------|------|
| Story: tiered discount rates | Converted → R-CART-004 | |
| Story: retire gift-wrap | Converted → REMOVED R-CART-002 | |
| Story: per-customer overrides | Deferred | Out of scope; recorded in NEXT |

### Cross-Story Conflict Scan: None found
```

Note the last line: an empty subsection collapses to one line (FB-024) — never an
empty table.

---

## 2. The capability spec after both merges — `docs/specs/cart.md`

US-007 merged first (added R-CART-001..003), then US-012 (added R-CART-004, modified
R-CART-001, removed R-CART-002). This is the accumulated current truth:

```markdown
# Spec: Cart

## Purpose
Cart assembly, discount application, and order-total calculation for the storefront.

## Requirements

### Requirement: Discount codes apply at checkout [R-CART-001]
The system SHALL apply a valid discount code's rate after tier discounts are applied.

#### Scenario: valid code reduces the total (Test Level: integration)
- Given a cart with subtotal 100.00 and a valid code SAVE5 (5%)
- When the order total is calculated
- Then the total SHALL be reduced by the code rate

#### Scenario: code stacks on tier discount (Test Level: integration)
- Given the cart qualifies for a 10% tier discount and a valid code SAVE5 (5%)
- When the order total is calculated
- Then the code SHALL apply to the tier-discounted amount (not the raw subtotal)

**Error Cases**: expired code → reject with reason; unknown code → reject with reason

### Requirement: Discount code length and charset are bounded [R-CART-003]
The system SHALL accept discount codes only within the configured bounds.

Scenarios: Not needed — pure parameter rule; the Parameters table + Error Cases
below fully define it, and its tests derive from them (`assertion_type: parameter`).

**Parameters**:
| Parameter | Type | Unit | Range | Default | Example | R/W | Notes |
|-----------|------|------|-------|---------|---------|-----|-------|
| codeLength | integer | chars | 4 - 32 | 12 | 8 | RW | Boundary tests derive from Range |
| codeCharset | enum | - | alnum \| alnum-dash | alnum | alnum | RW | |

**Error Cases**: length out of range → reject; character outside charset → reject

### Requirement: Discount rate scales with cart subtotal [R-CART-004]
The system SHALL apply the highest tier whose threshold the cart subtotal meets.

#### Scenario: subtotal crosses a tier boundary (Test Level: integration)
- Given tiers are {50: 5%, 100: 10%} and the cart subtotal is 99.00
- When the customer adds an item priced 1.00
- Then the applied discount rate SHALL change from 5% to 10%

#### Scenario: no tier met (Test Level: integration)
- Given tiers are {50: 5%, 100: 10%} and the cart subtotal is 30.00
- When the order total is calculated
- Then no discount SHALL be applied

**Parameters**:
| Parameter | Type | Unit | Range | Default | Example | R/W | Notes |
|-----------|------|------|-------|---------|---------|-----|-------|
| tierThresholds | number | currency | 0 - (none) | 50, 100 | 50 | RW | Ascending; duplicate thresholds rejected |
| tierRates | number | % | 0 - 90 | 5, 10 | 10 | RW | Paired 1:1 with tierThresholds |

**Error Cases**: thresholds not ascending → reject config; rate > 90 → reject config

## Removed
- [R-CART-002] Gift-wrap option — removed by US-012 (2026-06-13): fulfilment service owns gift-wrap
```

Things to notice:

- **R-CART-002 is gone from the body but tombstoned** — the ID is never reused, and the
  next NNN for CART is 5 (max over body + tombstones + active deltas, FB-021). Its tests
  (`Spec: R-CART-002`) were deleted in US-012.
- **R-CART-003 shows the exempted form in situ** (FB-013/019): no `#### Scenario:` blocks;
  the `Scenarios: Not needed — <reason>` line sits where they would be; its Completeness
  coverage comes from parameter-derived table-driven tests.
- **R-CART-001 carries US-012's modified text** — the spec holds current truth only;
  the previous behavior lives in the archived US-012 delta and git history.

---

## 3. The traceability chain, concretely

A test scaffolded for R-CART-004's first scenario:

```go
// cart_tier_test.go
// Spec: R-CART-004 — Discount rate scales with cart subtotal
// Scenario: subtotal crosses a tier boundary | Test Level: integration | assertion_type: behavior
func TestCart_GivenSubtotal99_WhenItemAdded_ThenTierRateBecomes10(t *testing.T) { ... }
```

And R-CART-003's parameter expansion:

```go
// cart_code_test.go
// Spec: R-CART-003 — Discount code length and charset are bounded
// Parameters: codeLength | assertion_type: parameter
func TestCartCodeLength(t *testing.T) { /* table-driven: 3,4,32,33 from Range 4-32 */ }
```

Verify's Completeness check greps these `Spec:` headers: every touched ID must have one
(exempted IDs via their parameter tests), and no test may carry an ID absent from the
spec + active deltas (orphan check, FB-021).

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2026-06-13 | Initial (FB-025): complete US-012 delta file (three sections, collapse rule shown), cart.md spec after two merges (tombstone + exempted Requirement in situ), traceability chain with Spec: headers |
