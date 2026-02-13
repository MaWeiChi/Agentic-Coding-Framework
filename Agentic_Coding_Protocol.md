# Agentic Coding Protocol

**Orchestrator × Executor 通訊協議與自動化流程**

本文件是 [Agentic Coding Framework](Agentic_Coding_Framework.md) 的第四份核心文件，定義 orchestrator 與 executor 之間如何溝通、狀態如何傳遞、步驟如何自動推進。

---

## 相關文件

| 文件 | 內容 | Agent 載入時機 |
|------|------|---------------|
| [Agentic_Coding_Framework.md](Agentic_Coding_Framework.md) | 框架本體：分層定義、核心原則、流程 | 每次對話必讀 |
| [Agentic_Coding_Lifecycle.md](Agentic_Coding_Lifecycle.md) | 運作機制：迭代模型、測試策略、CI/CD 接口 | 規劃迭代或設定 CI 時載入 |
| [Agentic_Coding_Templates.md](Agentic_Coding_Templates.md) | 框架細節：各層文件模板、撰寫指南、範例 | 撰寫 BDD/SDD/契約/Memory 時載入 |
| 本文件 | 通訊協議：orchestrator ↔ executor 的狀態管理與自動化 | 設定自動化流程或整合 orchestrator 時載入 |

---

## 架構模型：Orchestrator × Executor

框架的前三份文件定義了「要做什麼」和「怎麼做」，但沒有說明「誰驅動誰」。當開發流程由自動化 orchestrator 驅動時，需要一套明確的通訊協議。

### 角色分工

| 角色 | 職責 | 不做什麼 |
|------|------|---------|
| **Orchestrator** | 理解人類指令、讀 STATE 判斷下一步、dispatch executor、回報進度 | 不讀專案文件、不理解程式碼、不做設計決策 |
| **Executor** | 讀專案文件、寫 BDD/SDD/code/test、跑測試、更新 Memory | 不排程、不通知人類、不判斷「下一個 Story 做哪個」 |
| **人類** | 設定優先順序、Review、釐清需求、處理 blocker | 不介入 executor 的具體實作 |

### 設計原則：廉價調度 × 昂貴執行

Orchestrator 的設計目標是**零推理、零 LLM token**（或極低 token）。所有判斷邏輯都是確定性程式碼——查表、比對、模板填充。Executor 承擔主要的 token 開銷，負責需要理解力的工作。

這個模型的好處：

- **成本可預測**：orchestrator 的開銷固定（程式碼執行），executor 的開銷與 Story 複雜度正相關
- **不浪費高能力模型**：orchestrator 不需要理解程式碼，不浪費高價模型的推理能力在「讀 JSON、決定下一步」上
- **故障隔離**：orchestrator 與 executor 是獨立 session，一個 crash 不影響另一個的狀態

---

## 漸進式採用：從手動到全自動

本協議設計為三個階段漸進採用。不需要等全自動化完成才能開始使用——手動模式下，框架的所有文件產出（BDD / SDD / TDD / DDD）價值已經在了。

### Level 0：人類當 Orchestrator（今天可用）

最簡單的模式：你就是 orchestrator。透過通訊頻道（WhatsApp / Telegram / CLI）對 OpenClaw 下達每一步指令，OpenClaw 單純轉發給 Claude Code 執行。

**前提：** 專案的 CLAUDE.md 或 PROJECT_CONTEXT.md 中引用框架文件，讓 executor 知道要按什麼流程走。

#### 開新專案

```
你: 幫我用 agentic coding framework 建立 todo-app 專案，
    Go 後端 + React 前端。先做 Bootstrap（專案摘要 + SDD 骨架 + Constitution）
```

Executor 產出：
- `PROJECT_CONTEXT.md`（Why / Who / What + 技術棧 + 專案結構）
- `docs/sdd.md`（模組劃分 + 資料模型骨架）
- `docs/constitution.md`（3-5 條核心架構原則）
- `PROJECT_MEMORY.md`（初始狀態）
- 目錄結構（`docs/bdd/`、`docs/deltas/`、`docs/api/`）

#### 在既有專案加入功能

```
你: A 專案加入購物車功能，先寫 BDD
```
→ executor 讀 PROJECT_MEMORY.md + SDD，產出 `docs/bdd/US-007.md`

```
你: OK，繼續 SDD Delta 和契約
```
→ executor 產出 `docs/deltas/US-007.md` + 更新 `docs/api/openapi.yaml`

```
你: 我看過了，繼續 scaffold + impl
```
→ executor 產出測試骨架（紅燈）→ 寫 code 讓測試通過 → refactor

```
你: 繼續 verify + update memory
```
→ executor 執行三重驗證 → 更新 PROJECT_MEMORY.md

#### 在執行中的專案補充規格或測試

```
你: A 專案的 US-003 商品列表缺少 DDD Glossary，幫我補
```
→ executor 讀 SDD + BDD，產出 `docs/ddd/glossary.md`

```
你: A 專案補充 NFR，搜尋 API 要 p95 < 200ms
```
→ executor 更新 `docs/nfr.md`（加入 PERF-01）+ 在對應 BDD 加 `@perf(PERF-01)` 標記

```
你: A 專案 US-005 漏了 integration test，補上
```
→ executor 讀 BDD 場景 + 契約，在 Test Scaffolding 追加 `@integration` 層級的測試

#### Level 0 的限制

| 你需要自己做的 | 全自動化後由 orchestrator 做 |
|--------------|---------------------------|
| 記得每個專案做到哪一步 | STATE.json 自動追蹤 |
| 決定何時進入下一步 | Step 規則表自動推進 |
| 判斷失敗要重試還是回頭 | Reason-Based Routing 自動判斷 |
| 手動說「繼續」 | Orchestrator 自動 dispatch 下一步 |
| 記得多專案間切換 | Per-project STATE.json 各自獨立 |

### Level 1：半自動（需實作 STATE.json 適配器）

Executor 完成後 hook 自動寫 STATE.json，但 orchestrator 不自動推進。你仍然手動說「繼續」，但 orchestrator 會讀 STATE.json 告訴你上次做到哪、下一步是什麼、失敗了幾次。

**需要實作：** hook → STATE.json 適配器（≈ 100 行）

### Level 2：全自動（需實作 Orchestrator 狀態機）

你只需要說「繼續 A」，orchestrator 自動推進微觀瀑布的每一步，只在 review checkpoint 和 blocker 時暫停等你。

**需要實作：** Orchestrator 狀態機（≈ 300 行）+ Step 規則表載入器（≈ 50 行）+ .ai/ 初始化工具（≈ 100 行）+ Timeout Poller（≈ 50 行）

**Timeout Polling**：Level 2 不能只靠 hook 被動等結果——如果 executor crash 沒有觸發 hook，orchestrator 需要主動偵測。建議實作一個 poller：

```javascript
// 每 N 秒（建議 30s）檢查一次
function pollTimeout(project) {
  const state = readJSON(`${project}/.ai/STATE.json`);
  if (state.status !== 'running') return;

  const elapsed = (now() - state.dispatched_at) / 60000;
  const rules = STEP_RULES[state.step];

  if (elapsed > rules.timeout_min) {
    state.status = 'timeout';
    writeJSON(`${project}/.ai/STATE.json`, state);
    notify(user, `${state.story} 的 ${state.step} 超時（${Math.round(elapsed)} 分鐘）`);
  }
}
```

### Token Budget 參考表

以下為各步驟的 token 預估參考，幫助專案評估成本。數值基於中等複雜度 Story（[M]，3-8 檔案），實際消耗與 Story 複雜度正相關。

| Step | Executor 讀取 token | Executor 產出 token | 說明 |
|------|--------------------:|--------------------:|------|
| bdd | ≈ 2,000-4,000 | ≈ 500-1,500 | 讀 Memory + Context，產出場景 |
| sdd-delta | ≈ 3,000-6,000 | ≈ 800-2,000 | 讀 BDD + 現有 SDD，產出 Delta |
| contract | ≈ 2,000-4,000 | ≈ 500-1,000 | 讀 Delta + 現有契約，更新 YAML |
| review | 0 | 0 | 人類審查，不消耗 executor token |
| scaffold | ≈ 2,000-4,000 | ≈ 1,000-3,000 | 讀 BDD + 契約，產出測試骨架 |
| impl | ≈ 4,000-10,000 | ≈ 2,000-8,000 | 最高消耗，含多次迭代 |
| verify | ≈ 3,000-6,000 | ≈ 200-500 | 讀多份文件比對，產出少 |
| update-memory | ≈ 1,000-2,000 | ≈ 200-500 | 讀 Memory + STATE，更新 Memory |
| **單 Story 合計** | | | **≈ 15,000-40,000 tokens** |

Orchestrator token（Gemini Flash 或類似）：每次交互 ≈ 100-200 tokens，一個 Story 約 5-10 次交互，合計 ≈ 500-2,000 tokens。

Multi-Executor 模式的 token 預估見「Multi-Executor 協作模式 → Token 成本影響」段落。

---

## 通訊協議：三檔案

Orchestrator 與 executor 之間不直接通訊，而是透過檔案系統的三份檔案交換資訊。這個設計讓協議與任何特定工具解耦——不論 orchestrator 是什麼、executor 是什麼，只要會讀寫這三份檔案就能協作。Level 0 手動模式下不需要 STATE.json，executor 直接讀寫專案文件即可。

```
{project_root}/
  .ai/
    STATE.json          ← 雙向：hook 寫結果，orchestrator 寫指令
    HANDOFF.md          ← 單向：executor session → 下一個 session
  PROJECT_MEMORY.md     ← executor 的世界（orchestrator 不碰）
```

### 1. STATE.json — Orchestrator 的工作單

Orchestrator 只看這個檔案。**程式解析，零 LLM token。**

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

#### 欄位規格

| 欄位 | 型別 | 寫入者 | 說明 |
|------|------|--------|------|
| project | string | orchestrator | 專案識別碼 |
| story | string | orchestrator | 當前 User Story ID |
| step | enum | orchestrator / hook | 當前微觀瀑布步驟 |
| attempt | int | orchestrator | 當前步驟的嘗試次數 |
| max_attempts | int | Step 規則表 | 最大嘗試次數 |
| status | enum | hook | `pending` / `running` / `pass` / `failing` / `needs_human` / `timeout` |
| reason | string? | hook | 失敗原因碼（見 Reason-Based Routing） |
| dispatched_at | ISO8601 | orchestrator | dispatch 時間戳 |
| completed_at | ISO8601? | hook | 完成時間戳 |
| timeout_min | int | Step 規則表 | 超時分鐘數 |
| tests | object? | hook | 測試結果摘要 |
| failing_tests | string[]? | hook | 失敗的測試名稱 |
| lint_pass | bool? | hook | linting 結果 |
| files_changed | string[]? | hook | 本次變更的檔案 |
| blocked_by | string[]? | orchestrator | 本 Story 依賴但尚未完成的 Story ID（如 `["US-003"]`） |
| human_note | string? | orchestrator | 人類的指示（從通訊頻道轉錄） |

#### step 有效值

`bdd` · `sdd-delta` · `contract` · `review` · `scaffold` · `impl` · `verify` · `update-memory` · `done`

這些步驟對應 [Lifecycle 文件](Agentic_Coding_Lifecycle.md) 的微觀瀑布循環。

#### status 狀態機

```
pending → running → pass → (orchestrator 推進到下一步)
                  → failing → (orchestrator 重試或 routing)
                  → timeout → (orchestrator 通知人類)
                  → needs_human → (等待人類指示)
```

#### reason 有效值

`null`（一般失敗/成功）· `constitution_violation` · `needs_clarification` · `nfr_missing` · `scope_warning` · `test_timeout`

### 2. HANDOFF.md — Executor 之間的交接便條

每個 executor session 結束時寫，下一個 session 開始時讀。**每次覆寫，不累積**——這是它與 PROJECT_MEMORY.md 的關鍵差異。

#### 混合格式：結構化 Header + 自由格式 Body

HANDOFF.md 採用**混合格式**設計。前半段是結構化 YAML front matter，讓 hook 和 orchestrator 機器解析（零 LLM token）；後半段是自由格式 markdown，讓下一個 executor session 讀取細節 context。

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

## 這次做了什麼
- 修改 DiscountEngine.ApplyCoupon() 加入 coupon 過期檢查
- 修改 CartService 把 timezone 統一為 UTC

## 還沒解決的
- TestApplyCoupon: 過期 coupon 在 UTC+8 的邊界條件還沒處理
- TestRemoveExpired: batch delete SQL 的 WHERE 條件需要改用 < 而非 <=

## 下一個 session 應該注意
- 不要動 CartService.AddItem()，那個是好的
- coupon 的 expires_at 在 DB 是 UTC，前端傳來的可能是 local time
```

#### YAML Front Matter 欄位

| 欄位 | 型別 | 讀者 | 說明 |
|------|------|------|------|
| story | string | hook / orchestrator | 當前 Story ID |
| step | enum | hook / orchestrator | 當前步驟（同 STATE.json 的 step） |
| attempt | int | hook / orchestrator | 第幾次嘗試 |
| status | enum | hook | `pass` / `failing` / `needs_human` |
| reason | string? | hook | 失敗原因碼（同 STATE.json） |
| files_changed | string[] | hook / orchestrator | 本次變更的檔案 |
| tests_pass / tests_fail / tests_skip | int | hook | 測試結果數值 |

Hook 解析 YAML front matter 更新 STATE.json，**不需要 grep markdown body**。這解決了 executor-result 之前想解決的同一個問題——但 HANDOFF.md 本身就承擔了結構化回報的職責，不需要額外的檔案。

#### 與 executor-result 的關係

| 方式 | 機器可讀部分 | 人類/LLM 可讀部分 | 檔案數 |
|------|-------------|------------------|--------|
| HANDOFF.md（混合格式） | YAML front matter | Markdown body | 1 |
| executor-result + HANDOFF.md | executor-result | HANDOFF.md | 2 |

兩種方式都可行。混合格式的優勢是單一檔案、減少 executor 的產出負擔；雙檔案的優勢是職責更分離。專案可依偏好選擇，hook 應兩種都支援。

#### 為什麼獨立成檔案

| 考量 | HANDOFF.md | PROJECT_MEMORY.md |
|------|-----------|-------------------|
| 生命週期 | 每個 session 覆寫 | 整個專案的長期記錄 |
| 粒度 | 單次 step 的細節 | Story 級別的摘要 |
| 讀者 | hook（YAML）+ 下一個 executor（body） | 任何 session 的啟動 context |
| 膨脹風險 | 無（每次覆寫） | 有（需要人工清理） |

### 3. PROJECT_MEMORY.md — Executor 的世界

維持 [Templates 文件](Agentic_Coding_Templates.md) 現有設計。Orchestrator 不碰此文件。唯一調整：拿掉狀態機職責（由 STATE.json 承擔），回歸純專案上下文。

---

## Executor 輸出規則

Executor 的產出應遵循「最小輸出、結構優先」原則，降低下游（hook、orchestrator、下一個 session）的解析成本。

### 產出分類與格式要求

| 產出類別 | 格式 | 輸出策略 | 說明 |
|---------|------|---------|------|
| **文件**（BDD、Delta Spec、契約） | 對應格式（Gherkin / Markdown / YAML） | 寫入 `claude_writes` 指定路徑 | 由 git 追蹤 diff |
| **Code** | 原始碼 | 寫入 `claude_writes` 指定路徑 | 由 git 追蹤 diff |
| **狀態回報** | HANDOFF.md YAML front matter 或 executor-result | 結構化，hook 機器解析 | 零 LLM token 解析 |
| **交接 context** | HANDOFF.md markdown body | 自由格式，下一個 session 讀 | 描述做了什麼、卡在哪 |

### Diff-Only 原則

Executor 在修改既有文件時，**只修改受影響的段落，不重寫整份文件**。這是框架「增量而非重寫」核心原則在輸出層的體現。

| 步驟 | Diff-Only 行為 | 反模式 |
|------|---------------|--------|
| sdd-delta | 產出獨立的 Delta Spec 檔案，不改動 SDD 主文件 | 重寫整份 SDD |
| contract | 只增刪受影響的 endpoint / channel | 重新生成整份 openapi.yaml |
| impl | 只修改受影響的函式和檔案 | 為了「整潔」重構不相關的 code |
| update-memory | 只更新有變化的 section | 重寫整份 PROJECT_MEMORY.md |
| verify（合併 Delta）| 將 Delta 的 ADDED/MODIFIED/REMOVED 對應段落合併進 SDD | 用 Delta 內容覆蓋整份 SDD |

### 結構化格式優先

Executor 在產出 **機器消費** 的內容時，應優先使用結構化格式：

- API 契約：OpenAPI / AsyncAPI YAML（不用 markdown 表格描述 API）
- 測試結果：JSON 格式（`go test -json`）→ hook 解析寫入 STATE.json
- 狀態回報：HANDOFF.md YAML front matter 或 executor-result
- Delta Spec：固定的 ADDED / MODIFIED / REMOVED 結構

Executor 在產出 **人類/LLM 消費** 的內容時，可使用自然語言：

- HANDOFF.md body（交接 context）
- BDD 場景的 Given/When/Then（業務語言）
- SDD 的模組描述（架構說明）

### Dispatch Prompt 中的輸出指示

每個 step 的 dispatch prompt 應明確告訴 executor 輸出要求。在現有的 `step_instruction` 末尾加入：

```
輸出規則：
- 只修改受影響的文件和段落，不重寫不相關的內容
- 完成後更新 .ai/HANDOFF.md（含 YAML front matter）
- 如果觸及 Non-Goals 範圍，在 HANDOFF.md 的 reason 欄位標記 scope_warning
```

---

## Step 轉換規則表

Orchestrator 的程式碼查這張表決定下一步。**確定性，零推理。**

```yaml
steps:
  bdd:
    next_on_pass: sdd-delta
    next_on_fail: bdd
    max_attempts: 3
    timeout_min: 5
    requires_human: false
    claude_reads:
      - PROJECT_CONTEXT.md      # 專案摘要
      - PROJECT_MEMORY.md       # NOW + NEXT
      - .ai/HANDOFF.md          # 前次交接（如有）
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
      - docs/bdd/US-{story}.md   # 本次 BDD
      - docs/sdd.md               # 現有 SDD（受影響模組）
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
      - docs/sdd.md               # 受影響模組
      - docs/deltas/US-{story}.md  # 本次 Delta
      - docs/api/openapi.yaml     # 現有契約
      - .ai/HANDOFF.md
    claude_writes:
      - docs/api/openapi.yaml

  review:
    next_on_pass: scaffold
    on_fail:
      default: bdd                    # 方向錯了，回到 BDD
      needs_clarification: bdd        # 需求不清 → 重寫 BDD
      constitution_violation: sdd-delta # 架構問題 → 重新設計
      scope_warning: sdd-delta         # 範圍問題 → 調整 Delta
    requires_human: true          # orchestrator 發訊息等人類
    claude_reads: []              # executor 不參與
    claude_writes: []

  scaffold:
    next_on_pass: impl
    next_on_fail: scaffold
    max_attempts: 2
    timeout_min: 5
    requires_human: false
    claude_reads:
      - docs/bdd/US-{story}.md    # 本次 BDD（含標記）
      - docs/nfr.md               # NFR 閾值
      - docs/api/openapi.yaml     # 契約
      - .ai/HANDOFF.md
    claude_writes:
      - "*_test.go"
      - "*.spec.ts"

  impl:
    next_on_pass: verify
    on_fail:
      default: impl                    # 重試
      constitution_violation: sdd-delta # 架構違反 → 回到設計
      needs_clarification: review       # 需要人類
      scope_warning: review             # 觸及 Non-Goals
    max_attempts: 5
    timeout_min: 10
    requires_human: false
    claude_reads:
      - docs/sdd.md                # 受影響模組
      - docs/api/openapi.yaml     # 契約
      - .ai/HANDOFF.md            # 上次嘗試的交接
    claude_writes:
      - "*.go"
      - "*.ts"
    post_check: "go vet ./... && golangci-lint run"

  verify:
    next_on_pass: update-memory
    on_fail:
      default: impl                # 回到 impl
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
      - .ai/STATE.json            # 測試結果
    claude_writes:
      - PROJECT_MEMORY.md
```

### Component Test 的位置

Component Test（Playwright component testing）在 [Lifecycle 文件](Agentic_Coding_Lifecycle.md) 中定義為 Implementation 後、Verify 前的步驟。在 Step 規則表中，Component Test **不獨立成一個 step**——它被包含在 `impl` 步驟的 `post_check` 中（前端專案）或作為 `verify` 的 Correctness 檢查項之一。

原因：Component Test 的執行時機與後端 unit/integration test 不同（需要前端元件就緒），但在自動化流程中，它自然跟隨 impl 完成後執行。專案可在 `impl.post_check` 中加入 `npx playwright test --project=ct` 來整合。

### 規則表與 Lifecycle 的關係

規則表的 step 順序對應 [Lifecycle 文件](Agentic_Coding_Lifecycle.md) 的微觀瀑布循環。`claude_reads` 欄位定義了 executor 在每個步驟應載入的文件，對應 Framework 的「按需載入」原則。`post_check` 對應 Lifecycle 中 AST Linting 的整合（`go vet` + `golangci-lint`），前端專案可擴展為 `eslint . && tsc --noEmit && npx playwright test --project=ct`。

### 自訂規則表

每個專案可在 `.ai/step-rules.yaml` 中覆寫預設值。常見的自訂場景：

- 前端專案的 `post_check` 改為 `eslint . && tsc --noEmit`
- 簡單 CRUD 專案降低 `max_attempts`
- 高安全性專案在 `verify` 加入 security scan

---

## Dispatch 邏輯

Orchestrator 收到人類指令後，執行以下確定性邏輯。**零 LLM token——純程式碼。**

```javascript
function dispatch(project) {
  const state = readJSON(`${project}/.ai/STATE.json`);
  const rules = STEP_RULES[state.step];

  // 超時檢查
  if (state.status === 'running') {
    const elapsed = (now() - state.dispatched_at) / 60000;
    if (elapsed > rules.timeout_min) {
      state.status = 'timeout';
      notify(user, `${state.story} 的 ${state.step} 超時了`);
      return;
    }
    notify(user, `${state.story} 還在跑（${state.step}）`);
    return;
  }

  // 需要人類
  if (rules.requires_human && state.status !== 'pass') {
    state.status = 'needs_human';
    notify(user, formatReviewRequest(state));
    return;
  }

  // 成功 → 下一步
  if (state.status === 'pass') {
    state.step = rules.next_on_pass;
    state.attempt = 1;
    state.status = 'pending';
    state.human_note = null;
  }
  // 失敗 → 重試或 routing
  else if (state.status === 'failing') {
    if (state.attempt >= rules.max_attempts) {
      notify(user, `${state.story} 在 ${state.step} 卡住了（${state.attempt} 次）`);
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

  // 組裝 dispatch prompt（模板填充，零 LLM）
  const prompt = buildPrompt(state, rules);

  // 更新 STATE 並 dispatch
  state.status = 'running';
  state.dispatched_at = now();
  state.completed_at = null;
  writeJSON(`${project}/.ai/STATE.json`, state);

  dispatchExecutor(project, prompt);
}
```

---

## Dispatch Prompt 模板

每個 step 的 prompt 是模板填充，不需要 orchestrator 即興組裝。

```
你正在執行 {story} 的 {step_display_name}。
{if attempt > 1}（第 {attempt} 次嘗試，上限 {max_attempts} 次）{endif}

請依序讀取以下文件：
{for file in claude_reads}
- {file}
{endfor}

{if human_note}
=== 人類指示 ===
{human_note}
==================
{endif}

{step_instruction}

完成後：
1. 更新 .ai/HANDOFF.md：
   - YAML front matter：填入 story, step, attempt, status, reason, files_changed, tests 數值
   - Markdown body：記錄做了什麼、還沒解決的、下一個 session 注意事項
2. 如果需求不清，YAML front matter 的 reason 填 needs_clarification
3. 如果違反 Constitution，YAML front matter 的 reason 填 constitution_violation
```

### Step 固定指令（step_instruction）

| Step | 指令 |
|------|------|
| bdd | 根據 MEMORY 的 NOW/NEXT，撰寫本 Story 的 BDD 場景。使用 RFC 2119 用語，標記測試層級。不清楚的標記 `[NEEDS CLARIFICATION]` |
| sdd-delta | 根據 BDD 場景，分析受影響的模組，產出 Delta Spec（ADDED/MODIFIED/REMOVED） |
| contract | 根據 Delta Spec，更新 OpenAPI/AsyncAPI 契約中受影響的 endpoint/event |
| scaffold | 根據 BDD 場景標記和 NFR 表格，產出對應層級的測試骨架。所有測試必須失敗（紅燈） |
| impl | 讀取失敗的測試，寫最少量的 code 讓測試通過，然後 refactor |
| verify | 執行三重檢查：Completeness（BDD 全部有測試、Delta 全部實作）、Correctness（測試通過、NFR 達標）、Coherence（SDD 已合併 Delta、契約一致、Constitution 未違反） |
| update-memory | 讀取 STATE.json 的測試結果，更新 MEMORY 的 DONE/TESTS/LOG/NEXT。清除或更新 NOW |

---

## Hook 機制

Executor 完成（或失敗）後，hook 自動執行，將結果寫回 STATE.json 並通知 orchestrator。

### Hook 的職責

```bash
#!/bin/bash
# post-execution hook（虛擬碼）
PROJECT_ROOT="$1"
STATE_FILE="$PROJECT_ROOT/.ai/STATE.json"
STEP=$(jq -r '.step' "$STATE_FILE")

# 1. 跑測試（如果是需要測試的 step）
if [[ "$STEP" =~ ^(scaffold|impl|verify)$ ]]; then
  TEST_OUTPUT=$(cd "$PROJECT_ROOT" && go test ./... -json 2>&1)
  PASS=$(echo "$TEST_OUTPUT" | grep -c '"Action":"pass"')
  FAIL=$(echo "$TEST_OUTPUT" | grep -c '"Action":"fail"')
  SKIP=$(echo "$TEST_OUTPUT" | grep -c '"Action":"skip"')
fi

# 2. 跑 post_check（如果 step 規則有定義）
if [[ -n "$POST_CHECK" ]]; then
  LINT_RESULT=$(cd "$PROJECT_ROOT" && eval "$POST_CHECK" 2>&1)
  LINT_PASS=$?
fi

# 3. 讀 executor 的 reason 標記（優先從 YAML front matter 解析）
HANDOFF_FILE="$PROJECT_ROOT/.ai/HANDOFF.md"
if head -1 "$HANDOFF_FILE" | grep -q '^---$'; then
  # 混合格式：從 YAML front matter 解析 reason
  REASON=$(sed -n '/^---$/,/^---$/p' "$HANDOFF_FILE" | grep '^reason:' | awk '{print $2}')
  STATUS_FROM_HANDOFF=$(sed -n '/^---$/,/^---$/p' "$HANDOFF_FILE" | grep '^status:' | awk '{print $2}')
else
  # Fallback：舊格式，grep markdown body
  REASON=$(grep -o 'NEEDS CLARIFICATION\|CONSTITUTION VIOLATION\|SCOPE WARNING' \
           "$HANDOFF_FILE" | head -1)
fi

# 4. 更新 STATE.json
#    寫入 status, reason, tests, failing_tests, lint_pass,
#    files_changed, completed_at

# 5. 通知 orchestrator
notify_orchestrator "$STATE_FILE"
```

### .ai/executor-result 檔案（建議採用）

Dispatch prompt 中要求 executor 在完成時寫一個結構化檔案，讓 hook 能可靠地提取 reason 和狀態。**建議所有專案採用**——相比 grep HANDOFF.md，結構化檔案更不容易誤判。

```
# .ai/executor-result
status: pass
reason: null
summary: ApplyCoupon 的 timezone 問題已修復，改用 UTC 統一比較
```

| 欄位 | 型別 | 說明 |
|------|------|------|
| status | enum | `pass` / `failing` / `needs_human` |
| reason | string? | 失敗原因碼（同 STATE.json 的 reason 有效值） |
| summary | string | 一句話摘要本次執行結果 |

Hook 讀取優先順序：`.ai/executor-result` → fallback 到 grep HANDOFF.md。未採用 executor-result 的專案仍可正常運作，但 reason 提取的可靠性較低。

---

## Reason-Based Routing

傳統的二元判斷（pass/fail）不夠用。Executor 失敗時，失敗的原因決定了下一步該往哪走。

### 問題

如果 impl 失敗一律重試，會出現這些情況：

- **Constitution 違反**：executor 的實作方向違反了架構原則，重試多少次都不會好 → 應該回到 sdd-delta 重新設計
- **需求不清**：executor 發現 BDD 場景有歧義，自己猜了一個方向但測試沒過 → 應該回到 review 讓人類釐清
- **Scope 膨脹**：executor 改到了 Non-Goals 範圍的 code → 應該回到 review 確認是否真的要動

### 解法

Step 規則表的 `on_fail` 欄位支援 reason-based routing：

```yaml
impl:
  on_fail:
    default: impl                    # 一般失敗 → 重試
    constitution_violation: sdd-delta # 架構違反 → 回到設計
    needs_clarification: review       # 需求不清 → 回到人類
    scope_warning: review             # 觸及 Non-Goals → 確認
```

Reason 由 hook 從 HANDOFF.md 或 executor-result 提取，寫入 STATE.json 的 `reason` 欄位。Orchestrator 查表決定下一步，不需要理解 reason 的語意。

---

## 已知問題與解法

### 問題 1：STATE ↔ MEMORY 同步漂移

**風險：** hook 更新 STATE 為 pass，但 executor 在 MEMORY 中寫了過時的描述。

**解法：** MEMORY 的 NOW section 不由 executor 在 impl/verify 步驟中直接寫。在 `update-memory` step 中，executor 根據 STATE.json 的事實（測試結果、files_changed）生成 NOW 內容，確保兩者一致。

### 問題 2：Session 中斷沒有 Hook

**風險：** executor crash、API 斷線，hook 未執行。STATE 停在 `running`。

**解法：** STATE.json 記錄 `dispatched_at` + `timeout_min`。Orchestrator 在收到人類指令時檢查：如果 `status: running` 且超過 timeout，標記 `status: timeout`，通知人類。

### 問題 3：Fail Session 的上下文傳遞

**風險：** executor 改了檔案但測試沒全過，下一個 retry session 不知道上次做了什麼。

**解法：** HANDOFF.md。每個 session（不論成敗）都必須寫交接便條。dispatch prompt 中的 `claude_reads` 永遠包含 HANDOFF.md。

### 問題 4：Review 的人類意見落點

**風險：** 人類在通訊頻道回覆修改意見，但 executor 看不到。

**解法：** Orchestrator 將人類訊息摘要寫入 `STATE.json.human_note`。dispatch prompt 模板有 `{if human_note}` 區塊，帶入下一個 session。

### 問題 5：多專案並行

**風險：** 同時有 A、B 專案在跑，dispatch 衝突。

**解法：** Per-project STATE.json（`{project_root}/.ai/STATE.json`）。Orchestrator 在 dispatch 前檢查目標專案的 status 是否為 `running`。如果是，拒絕 dispatch 並通知人類。

### 問題 6：Step Routing 例外

**風險：** impl 失敗不一定要重試——可能是 Constitution 違反、需求不清、或觸及 Non-Goals。

**解法：** Reason-Based Routing（見上方段落）。

### 問題 7：多 Story 並行（進階）

**風險：** 目前 STATE.json 是 per-project 單檔，一次只能追蹤一個 Story。多個 Story 需要並行時（如多 agent 協作），單檔成為瓶頸。

**解法（可選）：** 改為 per-story STATE 檔案：

```
.ai/
  states/
    US-005.json    ← Story 各自獨立
    US-006.json
  HANDOFF.md       ← 仍為最新 session 的交接
```

Orchestrator 的 dispatch 邏輯改為掃描 `.ai/states/` 目錄，對每個 `status: pending` 的 Story 獨立 dispatch。`blocked_by` 欄位在此模式下特別重要——orchestrator 在 dispatch 前檢查被依賴的 Story 是否已完成。

**注意：** 這是進階模式，大多數專案用單檔 STATE.json 即可。只有在確實需要多 Story 並行時才啟用。

---

## Multi-Executor 協作模式

到目前為止，本協議假設每個 step 只有一個 executor。當 Story 的 `[P]` 並行標記或 `[L]` 複雜度需要多個 executor 同時工作時，需要擴展協議。本段落定義**抽象的多 executor 協作模式**，不綁定任何特定工具。

### 三層架構

```
人類
  ↕ 自然語言
外部 Orchestrator（跨 Story / 跨專案調度）
  ↕ 三檔案協議
Story-Level Coordinator（Story 內任務分解與 executor 協調）
  ↕ Scoped Context + Task 分配
Executor 群（實際執行：寫 BDD / SDD / code / test）
```

在單 executor 模式（`[S]` / 無 `[P]` 的 `[M]`）下，Coordinator 和 Executor 是同一個 session——退化為現有的二層架構。只有 `[M]+[P]` 或 `[L]` 才啟用三層。

### Complexity-Based Dispatch Mode

Orchestrator 在 dispatch 前根據 Story 的 Complexity 和 `[P]` 標記決定執行模式：

| 複雜度 | `[P]` 標記 | Dispatch Mode | 說明 |
|--------|-----------|--------------|------|
| `[S]` | — | `single` | 單 executor，Team 協調成本 > 收益 |
| `[M]` | 無 `[P]` | `single` | 順序任務，無需並行 |
| `[M]` | 有 `[P]` | `team` | 有明確的並行任務拆分 |
| `[L]` | — | `team` | 跨模組，建議多 executor 協作 |

可在 Step 規則表中配置：

```yaml
dispatch_mode:
  S: single
  M: auto       # 檢查 [P] 標記數量，≥ 2 個才啟用 team
  L: team
```

### Scoped Context Loading（動態 context 載入）

單 executor 模式下，`claude_reads` 是 per-step（每個步驟讀什麼）。多 executor 模式下，Coordinator 需要為每個 executor 組裝**範圍內的 context 子集**——不是全部載入，而是按任務載入。

規則表擴展 `team_roles` 欄位，定義不同角色的 context 範圍：

```yaml
impl:
  # 單 executor 模式仍用 claude_reads
  claude_reads:
    - docs/sdd.md
    - docs/api/openapi.yaml
    - .ai/HANDOFF.md

  # 多 executor 模式用 team_roles（可選）
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

**注意：** `team_roles` 是 Coordinator 組裝 spawn prompt 的參考，不是硬性限制。Coordinator 可根據 task 實際需要調整給 executor 的 context。

### Role-Based Context 隔離

多 executor 模式天然提供 context 隔離——不同 executor 是獨立的 context window。框架層面應確保：

| 角色 | 可讀 | 不可讀 | 理由 |
|------|------|--------|------|
| impl executor | SDD、契約、HANDOFF | 其他 impl executor 的 code（除非共用模組） | 避免 file conflict |
| test executor | BDD、契約、NFR、測試輸出 | impl 的原始碼 | 驗證獨立性——test 從 BDD 推導期望，不從 code 反推 |
| verify executor | BDD、SDD、契約、Constitution、測試輸出 | impl 過程中的中間產物 | 一致性檢查需要全局視角 |

這解決了原本 Refinement 中「Test/Impl context 隔離」的問題——多 executor 模式下天然隔離，框架只需定義角色邊界。

### Coordinator ↔ Executor 通訊

Coordinator 和 Executors 之間的通訊模式取決於具體工具的能力。框架只定義**需要傳遞的資訊**，不定義傳遞機制：

| 事件 | 方向 | 內容 | 用途 |
|------|------|------|------|
| task_assigned | Coordinator → Executor | `{task_id, role, scoped_context, instruction}` | 分配任務（`scoped_context` = `team_roles[role].claude_reads` 解析出的檔案列表） |
| task_done | Executor → Coordinator | `{task_id, status, files_changed, summary}` | 回報完成 |
| blocker | Executor → Coordinator | `{task_id, reason, description}` | 回報卡住 |
| conflict | Executor → Coordinator | `{files, description}` | 發現 file ownership 衝突 |

具體工具的實作方式：Agent Teams 用 mailbox、subagent 用 return value、CLI 多 session 用 file-based message queue。框架不規定。

### Per-Task HANDOFF

單 executor 模式下，HANDOFF.md 每次覆寫。多 executor 模式下，多個 executor 同時工作時需要更細粒度的交接：

- **Intra-session**（同一輪 team 內）：透過工具自身的通訊機制（mailbox / shared task list），不需要 HANDOFF
- **Cross-session**（team 結束後下次接續）：Coordinator 在 team 結束前寫一份 **consolidated HANDOFF**，匯總所有 executor 的進度

```markdown
# HANDOFF — US-007 impl (multi-executor session)

## Executor 進度
- backend: ✅ CouponRepository + DiscountEngine done
- frontend: 🔄 折扣碼元件 50%, DatePicker 有 timezone 問題
- test: ✅ unit tests done, integration test 等 frontend

## 檔案衝突紀錄
- 無

## 下次 session 注意
- frontend 的 DatePicker timezone 問題需要先解決
- integration test 依賴 frontend 完成
```

### Token 成本影響

多 executor 模式用更多 token 換更快完成。粗估：

| 模式 | 單 Story Token 預估 | 速度 | 適用場景 |
|------|--------------------:|-----:|---------|
| 單 executor | 15,000-40,000 | 1x | 日常開發、`[S]`/`[M]` |
| 多 executor (3 個) | 40,000-100,000 | ~2-3x 快 | 趕進度、`[L]`、明確 `[P]` 標記 |

決策建議：Token 預算寬裕且希望一天完成更多 Story 時才啟用 team mode。

---

## 參考實作：OpenClaw × Claude Code

以下是本協議在 OpenClaw + Claude Code 架構下的具體實作參考。其他 orchestrator × executor 組合可參照此模式。

### 架構

```
人類 (WhatsApp / Telegram / ...)
  ↕ 自然語言
OpenClaw (orchestrator · Gemini Flash · 極低 token)
  ↕ 三檔案協議
Claude Code (executor · Opus/Sonnet · 主要 token 開銷)
  ↕ 專案文件（BDD / SDD / 契約 / Memory）
Codebase
```

### 角色對應

| 協議角色 | 實作 | Token 開銷 |
|----------|------|-----------|
| Orchestrator | OpenClaw + Gemini Flash | ≈ 100-200 tokens/交互（只解析自然語言 + 組裝回覆） |
| Executor | Claude Code (Opus/Sonnet) | 主要開銷，與 Story 複雜度正相關 |
| 通訊頻道 | WhatsApp / Telegram | — |
| Hook | claude-code-hooks（notify-agi.sh） | — |

### OpenClaw 的 Dispatch 實作

OpenClaw 的 dispatch 邏輯對應本文件的「Dispatch 邏輯」段落。具體實作透過 OpenClaw 的 agent runtime 調用 Claude Code CLI：

1. OpenClaw 收到人類訊息（WhatsApp）
2. Gemini Flash 解析意圖：「繼續 A」→ project=cart-app, action=continue
3. 執行 `dispatch(project)` 確定性邏輯（零 LLM token）
4. 透過 `dispatch-claude-code.sh` 啟動 Claude Code session
5. Claude Code 完成後，`notify-agi.sh` hook 更新 STATE.json 並通知 OpenClaw
6. OpenClaw 用 Gemini Flash 組裝人類可讀的進度回報

### WhatsApp 對話範例

```
你: 繼續 A
秘書: 收到。A 專案正在執行 US-005 的實作（第 3 次嘗試）

（3 分鐘後）

秘書: US-005 實作完成 ✓ 測試全過（44/44），進入驗證

（1 分鐘後）

秘書: US-005 驗證通過 ✓ 記憶已更新。
       下一個是 US-006 結帳流程，要繼續嗎？

你: 繼續

秘書: 正在寫 US-006 的 BDD 場景

（2 分鐘後）

秘書: US-006 BDD 完成，需要你 review：
       - 場景 1: 選擇付款方式
       - 場景 2: 信用卡驗證失敗
       - 場景 3: 結帳後清空購物車
       有一個待釐清：第三方金流的 timeout 要設多久？

你: 30 秒，其他 OK

秘書: 收到，繼續。

（10 分鐘後，scaffold + impl + verify 自動完成）

秘書: US-006 全部完成 ✓
       下一個是 US-007 訂單歷史，要繼續嗎？

你: 今天先到這裡

秘書: 好的。A 專案目前進度：
       ✅ US-001 ~ US-006
       ⏭ 下一個 US-007
       明天說「繼續 A」就會接著做。
```

---

## OpenClaw Adapter Spec（參考設計）

本段落定義 OpenClaw 作為 orchestrator 時，如何與本協議對接。其他 orchestrator（Telegram Bot、CLI 工具等）可參照此模式設計自己的 adapter。

### Adapter 的職責

Adapter 是 orchestrator 與三檔案協議之間的橋接層。它的責任是：

1. **Intent Parsing**：將人類的自然語言指令解析為 `{project, action, params}` 結構
2. **State Management**：讀寫 STATE.json，執行 dispatch 邏輯
3. **Executor Invocation**：透過 CLI 或 API 啟動 executor session
4. **Result Reporting**：將 STATE.json 的狀態變化轉為人類可讀的訊息

### 介面定義

```typescript
interface OrchestratorAdapter {
  // Intent Parsing（需要 LLM，低 token）
  parseIntent(message: string): {
    project: string;
    action: 'continue' | 'status' | 'retry' | 'skip' | 'abort';
    params?: Record<string, string>;
  };

  // State Management（零 LLM token）
  readState(projectRoot: string): State;
  writeState(projectRoot: string, state: State): void;
  dispatch(projectRoot: string): DispatchResult;

  // Executor Invocation（觸發 executor，本身不消耗 LLM token）
  invokeExecutor(projectRoot: string, prompt: string): ExecutorHandle;

  // Result Reporting（需要 LLM，低 token）
  formatReport(state: State, action: string): string;
}

type DispatchResult =
  | { type: 'dispatched'; step: string; attempt: number }
  | { type: 'blocked'; reason: string }
  | { type: 'needs_human'; message: string }
  | { type: 'done'; summary: string };
```

### OpenClaw 特有的實作細節

| 元件 | OpenClaw 實作 | 通用 Adapter 可替換為 |
|------|--------------|---------------------|
| Intent Parsing | Gemini Flash（≈ 100 tokens） | 任何輕量 LLM 或正則表達式 |
| 通訊頻道 | WhatsApp / Telegram | CLI / Slack / Discord / Web UI |
| Executor | Claude Code CLI (`claude -p`) | 任何 LLM coding agent |
| Hook | `notify-agi.sh`（claude-code-hooks） | 任何 post-execution callback |

### 初始化流程

```bash
# 1. 在專案根目錄初始化 .ai/ 結構
mkdir -p .ai
echo '{"project":"<name>","story":null,"step":"bdd","attempt":1,"max_attempts":3,"status":"pending","reason":null,"dispatched_at":null,"completed_at":null,"timeout_min":5,"tests":null,"failing_tests":[],"lint_pass":null,"files_changed":[],"blocked_by":[],"human_note":null}' > .ai/STATE.json

# 2. 確保專案有 PROJECT_CONTEXT.md 和 PROJECT_MEMORY.md
# 3. 確保框架文件可被 executor 讀取（CLAUDE.md 中引用或 .ai/ 中放置）
# 4. 配置 hook：executor 完成後自動更新 STATE.json
```

---

## 參考實作：Claude Code Agent Teams（實驗性）

> ⚠️ **實驗性功能**：Agent Teams 目前是 Claude Code 的 experimental feature（需手動啟用 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`），有已知限制。本段落定義的是探索方向，不是穩定協議。

本段落將上方「Multi-Executor 協作模式」的抽象概念對應到 Claude Code Agent Teams 的具體工具。與 OpenClaw × Claude Code 的二層架構可疊加使用——OpenClaw 做跨 Story 調度，Agent Teams 做 Story 內的並行任務執行。

### 三層架構對應

```
人類 (WhatsApp / Telegram / ...)
  ↕ 自然語言
OpenClaw (L1 orchestrator · Gemini Flash · 跨 Story 調度)
  ↕ 三檔案協議
Claude Code Lead (L2 coordinator · delegate mode · Story 內調度)
  ↕ mailbox + shared task list
Claude Code Teammates (L3 executors · 實際寫 code/test/doc)
```

| 層 | 角色 | 職責 | Token 特性 |
|----|------|------|-----------|
| L1 | OpenClaw | 跨 Story / 跨專案調度 | 極低（Gemini Flash） |
| L2 | Claude Code Lead | Story 內任務分解、teammate 協調 | 中等（協調 token） |
| L3 | Claude Code Teammates | 寫 BDD / SDD / code / test | 高（主要開銷） |

### Lead 的行為規則

Lead 應啟用 **delegate mode**（Shift+Tab），確保只做協調不寫 code：

1. 讀取 BDD 場景的 `[P]` 標記，識別可並行的 tasks
2. 為每個 teammate 組裝 **scoped spawn prompt**——只給該 role 需要的 `claude_reads` 子集
3. 透過 mailbox 監控進度，不自己動手實作
4. 所有 teammates 完成後，synthesize 結果
5. 更新 STATE.json（status、tests、files_changed）和 HANDOFF.md（consolidated 格式）

### Spawn Prompt 範例

```
你是 cart-app 專案 US-007 的 backend executor。

請讀取以下文件：
- docs/sdd.md（只關注 DiscountEngine 和 CartService 模組）
- docs/api/openapi.yaml
- .ai/HANDOFF.md

你的任務：
1. 實作 CouponRepository CRUD（internal/coupon/repository.go）
2. 實作 DiscountEngine 折扣計算邏輯（internal/discount/engine.go）
3. 跑 go vet && golangci-lint run 確認通過

完成後：
- 在 .ai/executor-result 寫入 status 和 summary
- 更新 .ai/HANDOFF.md 的 backend 進度
- 不要動前端檔案（src/ 目錄是 frontend teammate 的範圍）
```

### Hook 整合

Agent Teams 提供兩個 hook 可用於品質管控：

| Hook | 觸發時機 | 框架用途 |
|------|---------|---------|
| `TeammateIdle` | teammate 即將閒置 | 檢查是否有未完成的 `[P]` task，有的話重新分配 |
| `TaskCompleted` | task 被標記完成 | 跑 post_check（linting），失敗則 exit code 2 阻止完成 |

```bash
# .claude/hooks/TaskCompleted.sh（虛擬碼）
TASK_FILES=$(jq -r '.files_changed[]' /tmp/task-result.json)
# 跑 linting
cd "$PROJECT_ROOT" && go vet ./... && golangci-lint run
if [ $? -ne 0 ]; then
  echo "Linting failed, please fix before completing"
  exit 2  # 阻止 task 完成，feedback 回 teammate
fi
```

### 完整 Dispatch 流程

```
1. 人類 → OpenClaw:「繼續 A」
2. OpenClaw → 讀 STATE.json → 判斷 dispatch_mode
   - [S] / [M] 無 [P]: 啟動單一 Claude Code session（現有流程）
   - [M]+[P] / [L]: 啟動 Claude Code 並指示建立 Agent Team
3. Claude Code Lead 啟動 → 讀 BDD + Task List → 進入 delegate mode
4. Lead spawn teammates → 為每個 teammate 組裝 scoped prompt
5. Teammates 並行工作 → mailbox 回報 → Lead 監控
6. Lead 確認全部完成 → update STATE.json + consolidated HANDOFF.md
7. Hook → 通知 OpenClaw
8. OpenClaw → 讀 STATE → dispatch 下一步或回報人類
```

### 已知限制與緩解

| 限制 | 來源 | 影響 | 緩解策略 |
|------|------|------|---------|
| No session resumption | Agent Teams 已知限制 | Team crash 後 teammates 消失，Lead 嘗試 message 失敗 | 每個 teammate 完成 task 後立即寫 mini-HANDOFF；crash 恢復時 Lead 讀 consolidated HANDOFF 重建 context |
| File conflicts | 兩個 teammates 改同一檔案 | 後寫的覆蓋先寫的 | `team_roles.claude_writes` 定義 file ownership boundary；`[P]` 標記確保並行 tasks 不觸及同一檔案 |
| Task status lag | Agent Teams 已知限制 | Teammate 完成但沒標記，dependent tasks 被阻塞 | Lead 定時 check-in；`TaskCompleted` hook 作為 fallback |
| Lead 自己動手 | Agent Teams 已知行為 | Lead 寫 code 而不是 delegate | Spawn prompt 明確指示 delegate mode；啟動時按 Shift+Tab |
| Token 爆炸 | 每個 teammate 是獨立 instance | 成本隨 teammate 數量線性增長 | Complexity-based dispatch（只有 `[M]+[P]` / `[L]` 才用 teams） |
| One team per session | Agent Teams 已知限制 | 一個 Lead 只能管一個 team | 一個 Story 一個 team session；跨 Story 由 OpenClaw 管理 |

### 建議的實驗步驟

本參考實作不建議一步到位。建議的實驗路徑：

1. **Phase 1**：在一個 `[M]+[P]` Story 上手動建立 Agent Team（不透過 OpenClaw），驗證 scoped spawn prompt + delegate mode 的效果
2. **Phase 2**：加入 `TaskCompleted` hook 做自動 linting gate，驗證品質管控
3. **Phase 3**：整合 OpenClaw dispatch，讓 OpenClaw 根據 Complexity 自動決定是否啟用 team
4. **Phase 4**：累積經驗後，將穩定的模式從「實驗性參考實作」升級為「正式協議」

---

## Changelog

| 版本 | 日期 | 變更 |
|------|------|------|
| v0.1 | 2026-02-13 | 初版：定義 Orchestrator × Executor 架構模型、三檔案通訊協議（STATE.json / HANDOFF.md / PROJECT_MEMORY.md）、Step 轉換規則表、Dispatch 邏輯、Hook 機制、Reason-Based Routing、六個已知問題與解法、OpenClaw × Claude Code 參考實作 |
| v0.2 | 2026-02-13 | 新增「漸進式採用」段落：定義 Level 0（手動）/ Level 1（半自動）/ Level 2（全自動）三階段採用路徑，補充開新專案、加功能、補規格的具體操作範例 |
| v0.3 | 2026-02-13 | 套用 Windsurf Review：executor-result 升級為建議採用（P0）；STATE.json 新增 blocked_by 欄位（P1）；review step 支援 reason-based routing（P1）；新增 OpenClaw Adapter Spec（P1）；新增 Token Budget 參考表（P2）；釐清 Component Test 在規則表中的位置（P2）；Level 2 新增 Timeout Polling 機制（P2）；新增多 Story 並行的 per-story STATE 設計（P2） |
| v0.4 | 2026-02-14 | 新增「Multi-Executor 協作模式」：三層架構（Orchestrator → Coordinator → Executors）、Complexity-Based Dispatch Mode（S/M/L）、Scoped Context Loading（team_roles 擴展）、Role-Based Context 隔離、Coordinator ↔ Executor 通訊事件定義、Per-Task HANDOFF 格式。新增「參考實作：Claude Code Agent Teams（實驗性）」：三層架構對應、Lead delegate mode 行為規則、Spawn Prompt 範例、Hook 整合（TeammateIdle / TaskCompleted）、完整 Dispatch 流程、已知限制與緩解、四階段實驗路徑。納入 Refinement 四項：動態 context 載入、Test/Impl 隔離、Agent 訂閱機制、交接格式 |
| v0.5 | 2026-02-14 | 新增「Executor 輸出規則」：Diff-Only 原則（per-step 反模式表）、結構化格式優先（機器消費 vs 人類消費分類）、Dispatch Prompt 輸出指示模板。HANDOFF.md 升級為混合格式：YAML front matter（hook 機器解析）+ Markdown body（executor 自然語言交接），含欄位規格表；釐清與 executor-result 的關係（兩種方式並存） |
| v0.6 | 2026-02-14 | 套用 Windsurf Round 2 Review：Hook 虛擬碼改用 YAML front matter 解析取代 grep（P0）；Dispatch Prompt 模板反映 HANDOFF 混合格式要求（P0）；team_roles 補齊 test/verify 角色範例（P1）；task_assigned 的 scoped_context 結構說明（P1）；STATE.json 初始化範例更新完整 schema（P2）；Token Budget 加入 Multi-Executor 交叉引用（P2） |
