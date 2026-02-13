# Agentic Coding Framework — 精進清單

**工具無關 · 以 Token / 品質 / 智慧化三維度篩選**

本文件是框架本體的精進建議，不綁定任何特定工具或 orchestrator。任何 AI 工具（Claude Code、Cursor、Windsurf、Copilot 等）採用本框架時都適用。

---

## 篩選標準

從四份比較分析（BDD / SDD / TDD / DDD）的 30 條建議中，以三個維度篩選：

| 維度 | 判斷問題 |
|------|---------|
| **Token** | 能否在實際 agent 工作流中省下 token？（防重跑、減歧義、避 scope 膨脹） |
| **品質** | 能否可測量地提升 agent 產出品質？ |
| **智慧化** | 能否讓 agent 更自主，減少人類介入次數？ |

三項全中 → 必做，兩項 → 值得做，一項以下 → 不納入。

---

## 必做（8 條）

### 1. TDD 遞迴上限

**三維命中：** Token（防無限打轉）· 品質（逼出更好策略）· 智慧化（agent 知道何時該停）

在 Lifecycle 文件的 Implementation 階段加入：agent 的 self-correction loop 最多迭代 N 次（建議 3-5 次）。超過上限時：

- 標記 blocker 到 MEMORY 的 ISSUES 區塊
- 記錄失敗的測試名稱和已嘗試的修復方向
- 暫停當前 Story，等待人類介入

參考來源：GPT-Pilot 的 5 層遞迴限制。

**影響文件：** Lifecycle

### 2. 資料模型 Source of Truth

**三維命中：** Token（消除矛盾導致的來回修正）· 品質（一致性）· 智慧化（agent 不需判斷「衝突時聽誰的」）

在 SDD 撰寫原則中加入：

- SDD 的資料模型段落是唯一的 source of truth
- API 契約的 schemas 從 SDD 推導
- DDD Glossary 的類型約束從 SDD 推導
- 三者出現矛盾時，以 SDD 為準

**影響文件：** Templates → SDD

### 3. Non-Goals / Out of Scope

**三維命中：** Token（防 scope creep 是最高效的省 token 策略）· 品質（不 over-engineer）· 智慧化（agent 有明確的「不做什麼」指令）

在 BDD 場景或 SDD Delta Spec 中加入可選的 Non-Goals 段落。格式：

```markdown
## Non-Goals (US-007)
- 本 Story 不處理優惠券的批量匯入功能
- 不考慮多幣種折扣計算
- 不修改現有的 CartService.AddItem() 介面
```

Agent 在 Implementation 時應檢查自己的變更是否觸及 Non-Goals 範圍。觸及時標記 `[SCOPE WARNING]` 暫停。

參考來源：Google Design Doc 將 Non-Goals 列為必填。

**影響文件：** Templates → SDD + BDD

### 4. Scenario Outline（參數化場景）

**三維命中：** Token（一個 Outline 取代 N 個重複場景）· 品質（參數化測試覆蓋更多邊界）· 智慧化（agent 知道何時用 data table）

在 BDD 模板中補充 Scenario Outline 範例：

```gherkin
@unit
Scenario Outline: 密碼強度驗證
  Given 使用者在註冊頁面
  When 輸入密碼 "<password>"
  Then 顯示驗證結果 "<result>"

  Examples:
    | password     | result           |
    | abc          | 至少 8 字元       |
    | abcdefgh     | 需要包含數字      |
    | Abcdefg1     | 通過             |
```

撰寫原則補充：當同一個行為需要驗證多組輸入輸出時，使用 Scenario Outline 而非複製多個 Scenario。

**影響文件：** Templates → BDD

### 5. AST Linting 整合

**三維命中：** Token（syntax error 在 linting 階段攔截，不跑到 Verify）· 品質（底層 code quality gate）· 智慧化（自動化，不需人類介入）

在 Lifecycle 文件的 Implementation 迴圈中加入：每次 Implementation 迭代後、進入 Verify 前，先跑 syntax-level 檢查。Go 後端建議 `go vet` + `golangci-lint`，前端建議 ESLint + TypeScript compiler。

Linting 失敗不進入 Verify，直接回到 Implementation 修復。這比 Verify 發現再回頭省一整輪。

**影響文件：** Lifecycle

### 6. Helper Function 提取原則

**三維命中：** Token（減少 Test Scaffolding 重複的 setup code）· 品質（DRY 測試更好維護）· 智慧化（agent 知道何時該提取）

在 Test Scaffolding 撰寫原則中加入：

- 當兩個以上測試共用相同的 Given setup，應提取為 `setupXxx(t *testing.T)` helper
- 當三個以上測試共用相同的 assertion pattern，應提取為 `assertXxx(t *testing.T, ...)` helper
- Helper 命名從 BDD 場景的 Given/Then 描述推導

**影響文件：** Templates → Test Scaffolding

### 7. Subdomain 分類

**三維命中：** Token（Generic Subdomain 可直接用現成方案省 token）· 品質（Core Domain 得到更多測試覆蓋）· 智慧化（agent 自動依類型調整投入力度）

在 DDD Level 1 的 Context Map 表格中加入「類型」欄位：

| Context | 職責 | 類型 | 路徑 | 對外契約 |
|---------|------|------|------|----------|
| Sales | 商品目錄、購物車、結帳 | **Core** | `/src/sales/` | `sales-openapi.yaml` |
| Auth | 認證、授權 | **Generic** | `/src/auth/` | `auth-openapi.yaml` |

Agent 行為規則：

- **Core**：最高測試覆蓋，Delta Spec + ADR 必填，深度 Review
- **Supporting**：標準測試覆蓋，Delta Spec 必填
- **Generic**：優先使用現成方案，最小測試覆蓋即可

**影響文件：** Templates → DDD

### 8. testify 模式對接

**三維命中：** Token（更精確的測試骨架 → impl 更容易一次過）· 品質（更好的測試結構）· 智慧化（agent 知道何時用 require vs assert）

在 Test Scaffolding 模板中明確區分：

```go
func TestCart_GivenEmptyCart_WhenAddItem_ThenHasOneItem(t *testing.T) {
    // Given — 用 require（前置條件，失敗立即停止）
    cart, err := NewCart(userID)
    require.NoError(t, err)
    require.NotNil(t, cart)

    // When
    err = cart.AddItem(productID, 1)

    // Then — 用 assert（驗證，全部檢查完再報告）
    assert.NoError(t, err)
    assert.Equal(t, 1, cart.ItemCount())
}
```

補充 Table-driven tests 模板（對應 Scenario Outline）和 Suite pattern 模板（對應 Background 共用前置條件）。

**影響文件：** Templates → Test Scaffolding

---

## 值得做（5 條）

| # | 建議 | 命中維度 | 影響文件 |
|---|------|---------|---------|
| 9 | **宣告式風格指引**：在 BDD 撰寫原則加入「優先使用宣告式 Given/When/Then，避免描述 UI 操作細節」 | 品質 + 智慧化 | Templates → BDD |
| 10 | **System Context 描述**：在 SDD「系統架構」加入「系統與外部系統的關係」，用 Mermaid graph 視覺化 | 品質 + 智慧化 | Templates → SDD |
| 11 | **Mermaid 圖表指引**：明確建議系統架構用 `graph`、資料模型用 `erDiagram`、複雜互動用 `sequenceDiagram` | 品質 + 智慧化 | Templates → SDD |
| 12 | **Anti-Pattern 清單**：列出 Agent 常犯的 BDD 反模式（命令式場景、場景間資料傳遞、incidental details） | Token + 品質 | Templates → BDD |
| 13 | **Domain Event Registry**：在 DDD 格式指南加入集中事件清單，減少 agent 需要跨文件查找的次數 | Token + 品質 | Templates → DDD |

---

## 不納入的（17 條）及理由

| 原建議 | 砍掉理由 |
|--------|---------|
| Background 語法標準化 | 格式美化，agent 讀得懂現有寫法 |
| @wip / @skip 標記 | [NEEDS CLARIFICATION] 已覆蓋核心需求 |
| Example Mapping | 人類流程，不是 agent 流程 |
| 模組錯誤處理策略 | 專案層級細節，框架不該統一定義 |
| ADR Status 機制 | 人類流程管理，agent 只需知道「現在的決策是什麼」 |
| Event Storming 對接 | 人類流程，框架定位是 agent 的工作基礎 |
| 補充 Context Mapping 模式 | 企業級場景才需要，碰到再補 |
| 動態 context 載入 | 實作層議題，非框架本體 |
| Test/Impl context 隔離 | 實作層議題，由 orchestrator 或工具處理 |
| Aggregate 設計原則 | Level 3 才觸發，太早定義 |
| Context 演進策略 | 極少數專案會碰到 |
| Runtime View | BDD 場景已描述行為 |
| Cross-cutting Concerns | 可併入 Constitution |
| Deployment View | 框架刻意排除，止於 image push |
| Agent 訂閱機制 | 多 agent 協作的實作層議題 |
| YAML 交接格式 | 多 agent 協作的實作層議題 |
| 多語言 Test Scaffolding | 按需擴充，不需預先定義 |

---

## 影響範圍摘要

| 文件 | 必做 | 值得做 | 合計 |
|------|:----:|:-----:|:----:|
| Templates → BDD | 2 | 2 | 4 |
| Templates → SDD | 2 | 2 | 4 |
| Templates → Test | 2 | 0 | 2 |
| Templates → DDD | 1 | 1 | 2 |
| Lifecycle | 2 | 0 | 2 |
| **Framework 主文件** | **0** | **0** | **0** |
| **合計** | **8** | **5** | **13** |

---

## Changelog

| 版本 | 日期 | 變更 |
|------|------|------|
| v0.1 | 2026-02-13 | 初版：從 30 條比較建議中以 Token/品質/智慧化三維度篩選為 13 條（8 必做 + 5 值得做） |
