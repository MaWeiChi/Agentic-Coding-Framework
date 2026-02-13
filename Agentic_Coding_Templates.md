# Agentic Coding Templates

**各層文件的模板、撰寫指南與範例**

本文件是 [Agentic Coding Framework](Agentic_Coding_Framework.md) 的框架細節補充。Agent 在撰寫 BDD、SDD、API 契約、Memory 等文件時載入參考。

---

## 相關文件

| 文件 | 內容 | Agent 載入時機 |
|------|------|---------------|
| [Agentic_Coding_Framework.md](Agentic_Coding_Framework.md) | 框架本體：分層定義、核心原則、流程 | 每次對話必讀 |
| [Agentic_Coding_Lifecycle.md](Agentic_Coding_Lifecycle.md) | 運作機制：迭代模型、測試策略、CI/CD 接口 | 規劃迭代或設定 CI 時載入 |
| 本文件 | 框架細節：各層文件模板、撰寫指南、範例 | 撰寫 BDD/SDD/契約/Memory 時載入 |

---

## PROJECT_MEMORY.md 模板

### 定位

PROJECT_MEMORY.md 是專案的**動態狀態追蹤文件**，放在專案根目錄。任何 AI 工具（Claude Code、Cursor、Windsurf、Copilot 等）啟動時都應讀取此文件，以接續上次的開發進度。

與專案摘要的分工：專案摘要（第一層）記錄穩定不變的 Why / Who / What；Memory 記錄持續變化的「現在到哪了、接下來做什麼」。

### Git Commit 校驗機制

Memory 記錄最後更新時的 git commit hash。Agent 啟動時應執行以下校驗：

```
1. 讀取 Memory 中的 last_commit_hash
2. 執行 git log --oneline 取得最新 commit
3. 比對：
   - 一致 → Memory 是最新的，直接接續
   - 不一致 → 中間有未記錄的變更（人類或其他 AI 工具）
     → 執行 git log <last_commit_hash>..HEAD 查看差異
     → 執行 git diff <last_commit_hash>..HEAD 查看變更內容
     → 更新 Memory 的相關區塊後再開始工作
```

這個機制讓 Memory 在跨工具使用時仍能保持一致性。不論是人類手動改了 code、或另一個 AI 工具做了修改，下一個接手的 agent 都能察覺並同步。

### 模板

設計原則：**最少 token、最大資訊密度**。同樣的專案狀態，新版比表格版省約 62% token。

結構採三段式分層載入：
1. **HTML 註解**（第 1 行）：機器標記，agent 一行完成 git 校驗
2. **NOW + NEXT**（前 10 行）：agent 只讀這段就能開始工作
3. **其餘區塊**：完整狀態，需要時才深讀

Section 名稱統一用英文大寫縮寫，壓縮 token 同時讓 agent 更容易用關鍵字定位。

```markdown
# PROJECT_MEMORY
<!-- commit:a1b2c3d | branch:main | dirty:no -->

## NOW
US-005 購物車功能 | phase:implementation | 後端 API done, 前端元件 WIP | blocker:none

## NEXT
1. 完成購物車前端元件（BDD US-005）
2. 購物車 Component Test
3. Safari WebP 圖片問題
4. US-006 結帳流程 BDD

## DONE
US-001 ✅ 使用者註冊 (02-13) unit+intg+comp
US-003 ✅ 商品列表 (02-14) unit+intg

## TESTS
unit:42/42 ✅ | intg:18/18 ✅ | comp:12/12 ✅ | e2e:⏸ | perf:⏸

## LOG
a1b2c3d 02-15 購物車後端 API（加入/移除/更新數量）
e4f5g6h 02-14 商品列表元件，分頁+排序
i7j8k9l 02-14 修正 email 驗證邏輯

## ISSUES
- [Med] Safari WebP 顯示異常 (02-14)

## SYNC
- Product model → OpenAPI spec + 前端 type
- 認證邏輯 → middleware test + E2E 登入
- DB schema → migration + SDD 資料模型
```

### Section 說明

| Section | 用途 | 權威來源 | 更新頻率 |
|---------|------|----------|----------|
| `<!-- -->` | git 狀態，機器快速校驗用 | git（事實） | 每次 commit |
| `NOW` | 當前任務、階段、卡點 | 人類意圖優先 | 每次 session |
| `NEXT` | 待辦優先順序 | 人類意圖優先 | Story 完成時 |
| `DONE` | 已完成功能 + 測試覆蓋摘要 | git + 測試（事實） | Story 完成時 |
| `TESTS` | 各層級測試通過數 | CI / 測試（事實） | 每次測試後 |
| `LOG` | 最近 5 筆 commit（舊的靠 git log） | git（事實） | 每次 commit |
| `ISSUES` | 未解決問題 | 混合（agent 可追加，不刪人類的） | 隨時 |
| `SYNC` | 連動提醒（改 A 要改 B） | 人類知識優先 | 發現時追加 |

### 撰寫原則

**簡潔優先**：Memory 是 agent 的快速定位工具，不是完整文件。每個區塊點到為止，細節留在對應的文件中（BDD、SDD、測試報告）。

**Agent 可執行**：「下一步」的描述要具體到 agent 能直接行動，避免模糊的描述。好的例子：「完成購物車前端元件（對照 BDD 場景 US-005）」。壞的例子：「繼續開發購物車」。

**Git 為錨**：每次更新 Memory 時，必須同步記錄當前的 git commit hash。這是跨工具校驗的基礎。

**人機共寫**：Agent 自動更新日常變動；人類手動編輯優先級調整、策略變更等 agent 無法判斷的內容。衝突時按「事實 vs. 意圖」區分權威來源：事實性區塊（Git 狀態、測試狀態、變更記錄）以 git / 測試為準；意圖性區塊（當前任務、下一步、連動提醒）以人類為準。Agent 永遠可以「追加」，但不「覆蓋」或「刪除」人類的手動編輯。完整的衝突處理策略定義在 [Lifecycle 文件](Agentic_Coding_Lifecycle.md)的 Memory 更新規則中。

---

## CLAUDE.md / 專案入口文件模板

### 定位

放在專案根目錄，是 agent 每次對話的第一份讀取文件。因為要跨工具使用，建議檔名用通用的 `PROJECT_CONTEXT.md`，各工具再以自己的方式指向它（Claude Code 可在 CLAUDE.md 中 `@include` 或直接引用）。

### 模板

```markdown
# <專案名稱>

## 專案摘要

- **Why** — <解決什麼問題>
- **Who** — <目標使用者>
- **What** — <最終產出是什麼形式的產品>

## 技術棧

- **Frontend**: <框架、語言>
- **Backend**: <框架、語言>
- **Database**: <資料庫類型與名稱>
- **Infrastructure**: <部署方式>

## 專案結構

<簡要目錄結構，標註 agent 最常接觸的目錄>

## 開發慣例

- Git 分支策略：<說明>
- Commit 規範：<說明>
- 命名慣例：<說明>

## Agent 指引

- 每次對話前先讀 `PROJECT_MEMORY.md` 了解專案現況
- 遵循 BDD → SDD → TDD 的開發流程（詳見 Agentic Coding Framework）
- 每次 Story 結束時更新 `PROJECT_MEMORY.md`
- 不要重構沒有 ADR 記錄原因的設計決策
```

### 撰寫原則

**穩定為主**：這份文件在 Bootstrap 後應很少變動。會頻繁變動的資訊（進度、任務、狀態）放 Memory，不放這裡。

**Token 友善**：控制在 agent 的 context window 中佔比最小，讓更多空間留給實際程式碼。

---

## BDD 場景模板

### 定位

每個 User Story 一份或一組 BDD 場景檔案，放在 `docs/bdd/` 或 `features/` 目錄。

### 模板

```gherkin
# Story: <US-XXX> <Story 標題>

## 前置條件（共用）
# 如果多個場景共用同一組前置條件，在此集中描述。

@unit @integration
Scenario: <正常路徑的行為描述>
  Given <系統或使用者的初始狀態>
  When <使用者的操作或系統事件>
  Then <預期的結果或狀態變化>
  And <額外的驗證點>

@unit
Scenario: <邊界條件或錯誤路徑的行為描述>
  Given <初始狀態>
  When <觸發邊界條件的操作>
  Then <預期的錯誤處理行為>

@e2e
Scenario: <完整使用者流程>
  Given <使用者在某個頁面或狀態>
  When <一連串操作步驟>
  Then <最終預期結果>

@perf(PERF-02) @secure(SEC-01)
Scenario: <效能或安全性相關場景>
  Given <負載條件或安全前提>
  When <觸發操作>
  Then <預期結果（具體閾值查 NFR 表格）>
```

### 撰寫原則

**一個場景驗證一件事**：避免在單一場景中塞太多 Then。如果一個場景的 Then 超過三條，考慮拆分。

**標記必填**：每個場景至少一個測試層級標記。這是 Test Scaffolding 的驅動依據，缺標記的場景不會被自動產出測試。標記分兩種語法：簡單標記（`@unit`、`@e2e`）定義測試層級；帶 ID 標記（`@perf(PERF-01)`、`@secure(SEC-01)`）同時定義測試層級並引用 NFR 表格的具體閾值。

**Given 描述狀態、When 描述動作、Then 描述結果**：避免在 Given 中放操作、在 When 中放預期結果。

**使用領域語言**：場景描述用業務語言，不用技術術語。「使用者提交訂單」而非「POST /api/orders」。

---

## SDD 模板

### 定位

一份 SDD 涵蓋整個專案的架構設計，隨 Story 增量更新。放在 `docs/sdd.md` 或 `docs/design/` 目錄。

### 模板

```markdown
# Software Design Document — <專案名稱>

## 系統架構

<架構圖或文字描述：前後端分離方式、資料流向、部署拓撲>

## 模組劃分

### <模組名稱 A>

- **職責**: <這個模組負責什麼>
- **對外介面**: <提供什麼 API 或函式>
- **依賴**: <依賴哪些其他模組>
- **資料模型**: <核心資料結構>

### <模組名稱 B>

...

## 資料模型

<DB schema 設計，含表名、欄位、關聯>

## 技術決策（ADR 可併入此處）

### <決策標題>
- **決策**: <選了什麼>
- **原因**: <為什麼選這個>
- **替代方案**: <考慮過但沒選的>
- **日期**: <決策日期>

## 跨模組互動

<模組間如何溝通：同步 API call、事件驅動、shared DB 等>
```

### 撰寫原則

**模組邊界清楚**：每個模組有明確的「職責」和「對外介面」定義，讓 Story 的增量更新範圍容易界定。

**ADR 隨手記**：做了有爭議的技術決策時，當下在「技術決策」段落記一筆。不需要事後補。

**增量友善**：新 Story 只追加或修改受影響的模組段落，不需重寫整份文件。建議在每個模組段落開頭標註「由哪些 Story 引入/修改」以追蹤來源。

---

## API 契約模板

### 定位

前後端分離專案的介面定義。REST API 使用 OpenAPI 3.0+ 格式，放在 `docs/api/openapi.yaml`；事件驅動介面（WebSocket、MQTT 等）使用 AsyncAPI 3.0 格式，放在 `docs/api/asyncapi.yaml`。

### REST API（OpenAPI 摘要）

```yaml
openapi: 3.0.3
info:
  title: <專案名稱> API
  version: 0.1.0

paths:
  /api/<resource>:
    get:
      summary: <簡述>
      tags: [<模組名稱>]
      parameters:
        - name: <param>
          in: query
          schema:
            type: string
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/<ResponseModel>'
        '400':
          description: 參數錯誤
        '401':
          description: 未授權

components:
  schemas:
    <Model>:
      type: object
      required: [<field1>, <field2>]
      properties:
        <field1>:
          type: string
          description: <說明>
```

### 事件驅動 API（AsyncAPI 摘要）

```yaml
asyncapi: 3.0.0
info:
  title: <專案名稱> WebSocket API
  version: 0.1.0

servers:
  production:
    host: <host>
    protocol: ws
    description: WebSocket 伺服器

channels:
  joinRoom:
    address: /ws
    messages:
      joinRoom:
        $ref: '#/components/messages/JoinRoom'
    description: 客戶端加入房間

  roomUpdate:
    address: /ws
    messages:
      roomUpdate:
        $ref: '#/components/messages/RoomUpdate'
    description: 伺服器推送房間狀態

operations:
  sendJoinRoom:
    action: send
    channel:
      $ref: '#/channels/joinRoom'
    summary: 客戶端請求加入房間

  receiveRoomUpdate:
    action: receive
    channel:
      $ref: '#/channels/roomUpdate'
    summary: 接收房間狀態更新

components:
  messages:
    JoinRoom:
      payload:
        type: object
        required: [roomId]
        properties:
          roomId:
            type: string
            description: 房間 ID

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
            description: 房間狀態

  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
```

### 撰寫原則

**契約先行**：先定義好 API 契約，前後端再各自對著契約實作。Agent 不需要「猜」介面長什麼樣。

**REST 用 OpenAPI、事件用 AsyncAPI**：兩者都是機器可讀的標準格式，agent 可以直接解析並產出對應的 type 定義和測試骨架。避免用 markdown 表格描述 API——結構化格式才能被工具鏈（code generator、mock server、validator）消費。

**增量更新**：新 Story 只增加新的 endpoint / channel 或修改受影響的部分，不重寫整份契約。

**Payload 必須定義**：不論 REST response 或 WebSocket message，都要包含完整的資料結構。這是前端 agent 能否自主實作的關鍵。

---

## NFR 模板

### 定位

NFR（Non-Functional Requirements）定義效能、安全性、可靠性等非功能性約束。Agent 預設會寫出「功能正確」的 code，但不會主動考慮這些約束。NFR 文件讓 agent 在產出 `@perf` / `@load` 測試時有明確的閾值可查。

放在 `docs/nfr.md` 或併入 SDD。建議專案初期先定義 3 條最關鍵的 NFR（API latency、error rate、authentication），讓 agent 養成「寫功能必帶 NFR 測試」的習慣，之後再擴充。

### NFR ID 系統

每一條 NFR 都有唯一 ID，這是 BDD 場景與 NFR 的連接點。BDD 場景透過 `@perf(PERF-01)` 語法引用 NFR ID，agent 在 Test Scaffolding 時查表取得閾值、工具、範圍，直接產出對應的測試腳本。

NFR 表格是閾值的**單一真相來源**。不允許在 BDD 場景中 inline override 閾值（如 `@perf(p95=2000ms)`），避免效能標準散落在多個 BDD 檔案裡。如果特殊場景需要不同閾值，在 NFR 表格中新增一條獨立 ID。

### 模板

```markdown
# Non-Functional Requirements (NFR)

## Performance (效能)

| ID | 描述 | 指標 (Metric) | 閾值 (Threshold) | 範圍 (Scope/Regex) | 工具 (Tool) | 優先級 |
|:---|:---|:---|:---|:---|:---|:---|
| `PERF-01` | API 快速回應 | p95 latency | < 200ms | `/api/v1/*`（排除 `/api/v1/report/*`） | k6 | P0 |
| `PERF-02` | 搜尋高併發 | VUs, error rate | 1000 users, 0 errors | `/api/v1/search` | k6 | P0 |
| `PERF-03` | 頁面載入速度 | LCP | < 2.5s | `/*`（公開頁面） | Lighthouse CI | P1 |
| `PERF-04` | 報表生成（重型） | p95 latency | < 2000ms | `/api/v1/report/*` | k6 | P1 |

## Security (安全性)

| ID | 描述 | 驗證規則 | 範圍 (Scope/Regex) | 工具 (Tool) | 備註 |
|:---|:---|:---|:---|:---|:---|
| `SEC-01` | 身份驗證 | Bearer Token (JWT) | 所有非 `/public/*` 路由 | Integration Test | 需驗證 401/403 |
| `SEC-02` | 輸入消毒 | No XSS / SQL Injection | 所有 POST/PUT body | OWASP ZAP / SonarQube | CI 階段掃描 |

## Reliability (可靠性)

| ID | 描述 | 指標 (Metric) | 目標 | 測量方式 | 備註 |
|:---|:---|:---|:---|:---|:---|
| `REL-01` | 系統可用性 | Uptime | 99.5% | Monitoring Alert | 不含計畫性維護 |
| `REL-02` | 錯誤率 | HTTP 5xx rate | < 0.1% | CI + Monitoring | 每次部署後驗證 |
```

### Agent 執行流程

```
1. Agent 讀取 BDD 場景，看到 @perf(PERF-01) @secure(SEC-01)
2. 查 NFR 表格：
   - PERF-01 → p95 < 200ms, 工具 k6, 範圍 /api/v1/*
   - SEC-01  → JWT Bearer Token, 驗證 401/403
3. Test Scaffolding：
   - 產出 k6 腳本，thresholds 填入 p95 < 200ms
   - 產出 Integration Test，驗證未授權回傳 401
4. 若當前 endpoint 不在 PERF-01 範圍內（如 /api/v1/report/annual）
   → 自動匹配 PERF-04（p95 < 2000ms）
```

### 分層粒度

NFR 表格定義**全域基準線**（Global Defaults）。當特殊場景需要不同標準時，不要在 BDD 裡覆寫，而是在 NFR 表格中新增一條帶有明確範圍的 ID（如 `PERF-04` 專給報表生成）。

這確保：效能標準永遠可以在一份文件中總覽，agent 不需要掃描所有 BDD 檔案才能知道「這個 API 應該多快」。

### 撰寫原則

**每條都有 ID**：ID 是 BDD ↔ NFR 的連接點。缺 ID 的 NFR 無法被 BDD 場景引用，等於不存在。

**範圍要精確**：用 regex 或路徑模式定義適用範圍，避免「所有 API」這種籠統描述。排除規則（如「排除 `/report/*`」）要明確寫出。

**工具要指定**：Agent 需要知道用什麼工具生成測試腳本。`k6`、`Lighthouse CI`、`OWASP ZAP` 等直接影響 agent 產出的 code 結構。

**先少後多**：專案初期 3 條就夠（latency、error rate、auth）。碰到效能問題時再追加，不用一開始追求完備。

---

## Test Scaffolding 模板

### 定位

根據 BDD 場景標記產出的測試骨架，所有測試初始狀態為失敗（紅燈）。

### 模板（Go 後端 Unit/Integration）

```go
// <module>_test.go
// Generated from: BDD US-XXX — <場景描述>
// Tags: @unit

func TestXxx_GivenCondition_WhenAction_ThenResult(t *testing.T) {
	// Given: <從 BDD 場景複製的前置條件>
	// TODO: setup

	// When: <從 BDD 場景複製的操作>
	// TODO: execute

	// Then: <從 BDD 場景複製的預期結果>
	t.Fatal("Not implemented — RED phase")
}
```

### 模板（Playwright Component Test）

```typescript
// <component>.spec.ts
// Generated from: BDD US-XXX — <場景描述>
// Tags: @component

import { test, expect } from '@playwright/experimental-ct-react';
import { ComponentName } from './ComponentName';

test('<從 BDD 場景複製的行為描述>', async ({ mount }) => {
  // Given: <前置條件>
  // TODO: setup props and context

  // When: <操作>
  const component = await mount(<ComponentName />);
  // TODO: simulate user action

  // Then: <預期結果>
  // TODO: add assertions
  test.fail(); // RED phase
});
```

### 撰寫原則

**BDD 場景可追溯**：每個測試檔案開頭標註來源 BDD 場景編號和標記，建立雙向追蹤。

**命名來自場景**：測試函式名用 Given/When/Then 組合，不自行發明測試名稱。

**全部紅燈**：骨架產出後所有測試必須失敗。如果有測試意外通過，說明測試寫得不夠精確。

---

## DDD 格式指南

### 定位

DDD（Domain-Driven Design）是 [Framework](Agentic_Coding_Framework.md) 的可選擴充，在專案涉及多個業務領域時觸發。本段落定義三個 Level 的具體文件格式。

### 漸進式分裂策略

DDD 文件的存放位置隨專案規模演進，不需要一開始就獨立成目錄：

| 專案規模 | 判定標準 | 存放位置 | 理由 |
|----------|----------|----------|------|
| 小型 / MVP | < 3 個 Context，代碼 < 5000 行 | 併入 `SDD.md` 各佔一段落 | Agent 一次讀取全貌，減少讀檔次數 |
| 中大型 / 複雜 | ≥ 3 個 Context，或多 Agent 並行 | 獨立 `docs/ddd/` 目錄 | 避免 SDD 超過 Context Window；Agent 只載入當前 Context |

分裂的觸發信號：當 SDD 長度導致 agent 的 context window 裝不下完整文件，或多個 agent 各負責一個 Context 時，就該把 DDD 獨立出來。

### Level 1 — Bounded Context Map

定義各 Context 的邊界、職責與溝通方式。文字 + Mermaid 圖表的組合讓 agent 既能解析結構，也能理解依賴關係。

```markdown
# Bounded Context Map

## 視覺化關係

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

## 上下文定義

| Context | 職責 | 路徑 | 對外契約 | 備註 |
|---------|------|------|----------|------|
| Sales | 商品目錄、購物車、結帳 | `/src/sales/` | `docs/api/sales-openapi.yaml` | 核心業務，變動頻率高 |
| Shipping | 庫存扣減、物流單生成 | `/src/shipping/` | `docs/api/shipping-openapi.yaml` | 接收 Sales 事件觸發 |
| Billing | 付款處理、發票 | `/src/billing/` | `docs/api/billing-openapi.yaml` | 接收 Sales 事件觸發 |

## 互動模式（Integration Patterns）

| 上游 | 下游 | 關係類型 | 介面 | 模式 |
|------|------|----------|------|------|
| Sales | Shipping | Customer-Supplier | Event: `OrderPlaced` | ACL（Anti-Corruption Layer），非同步 |
| Sales | Billing | Customer-Supplier | Event: `PaymentAuthorized` | ACL，非同步 |
| Frontend | Sales | — | REST API | OHS（Open Host Service） |
```

### Level 2 — Glossary（Ubiquitous Language）

通用語言表，強制 agent 在命名變數和欄位時查閱。加入「類型/約束」欄位，讓 agent 產出 DB Schema 和 API DTO 時不需猜測。

```markdown
# Ubiquitous Language（通用語言 & 資料字典）

> 指令：所有 Agent 在命名變數、資料庫欄位、API 參數時，必須嚴格遵守此表。禁止使用同義詞。

| 術語 | Sales Context 定義 | Shipping Context 定義 | 類型/約束 | 範例值 |
|------|-------------------|----------------------|-----------|--------|
| User | `Customer`（下單者） | `Recipient`（收件人） | UUID (v4) | `550e8400-e29b...` |
| Order | `SalesOrder`（含金額明細） | `ShippingOrder`（含重量材積） | String `ORD-{Timestamp}` | `ORD-2026021301` |
| Address | 帳單地址（Billing） | 配送地址（Delivery） | JSON Structure | `{ "zip": "100", ... }` |
| Item | 商品（含價格快照） | 包裹內容物（含材積） | Array | — |
```

### Level 3 — Aggregate Root（嵌入 SDD）

Aggregate Root 屬於戰術設計，直接嵌入 SDD 的模組段落。用 `[DDD 戰術約束]` 標記區塊，讓 agent 一眼識別不變規則與存取限制。

```markdown
## 模組：Sales Context

### 核心實體

> **[DDD 戰術約束]**
> - **Aggregate Root:** `Order`
> - **Invariant:** 訂單總金額必須等於明細總和；訂單一旦 Confirmed 不可修改明細。

#### Order（Aggregate Root）
- **Attributes:**
  - `id`: UUID
  - `status`: Enum (DRAFT, CONFIRMED, SHIPPED)
  - `items`: List<OrderItem>
- **Methods:**
  - `addItem(product, quantity)`: 必須檢查庫存
  - `confirm()`: 觸發 `OrderPlaced` 事件

#### OrderItem（Local Entity）
- **Access:** 只能透過 `Order` 存取，禁止單獨 Repository 查詢。
```

### 撰寫原則

**Context Map 是全域文件**：不論放在 SDD 裡還是獨立目錄，Context Map 和 Glossary 都是所有 agent 共用的參考。任何 agent 開始工作前應先查閱，確認自己在哪個 Context 裡。

**Glossary 是命名的強制約束**：Agent 不得自行發明同義詞。「Sales Context 的 User 叫 Customer」就是叫 Customer，不能叫 Buyer、Client 或 Purchaser。

**Aggregate Root 約束實作邊界**：標記了 `[DDD 戰術約束]` 的區塊，agent 在實作時必須遵守 Invariant 規則，不得繞過 Aggregate Root 直接操作子實體。

**Mermaid 和表格並用**：Mermaid 讓 agent 快速理解依賴拓撲，表格提供精確的路徑、契約、型別細節。兩者互補，缺一不可。

---

## 既有專案反向工程流程

### 定位

將既有 codebase 反向產出框架所需的文件，讓後續開發可以進入正常的 BDD → SDD → TDD 流程。

### 步驟

```
1. 掃描專案結構
   - Agent 讀取目錄樹、package.json / go.mod 等配置
   - 產出初步的技術棧描述

2. 反向產出專案摘要
   - 從 README、主要程式碼入口推斷 Why / Who / What
   - 人類校正並補充

3. 反向產出 SDD
   - Agent 掃描主要模組、路由、資料模型
   - 產出模組劃分和資料模型草稿
   - 人類補充隱性架構決策（記入 ADR）

4. 反向產出 BDD（Characterization Test）
   - 描述「現有行為」而非「期望行為」
   - 目的是建立基線，不是定義新需求
   - 標記測試層級

5. 補 Test Scaffolding
   - 根據反向產出的 BDD 標記產出測試骨架
   - 實作 Characterization Test 讓它們全部通過
   - 這些測試成為後續修改的迴歸保護

6. 初始化 PROJECT_MEMORY.md
   - 記錄當前 git commit hash
   - 填入已完成功能清單
   - 設定下一步行動
```

### 注意事項

**不要遺漏隱性知識**：部分架構決策是 agent 從 code 讀不出來的。例如「這裡用了 polling 而不是 WebSocket 是因為目標設備不支援」，這類資訊必須人類手動補進 SDD。

**Characterization Test ≠ 理想行為**：如果現有行為有 bug，Characterization Test 仍然描述現有行為。Bug 修正作為後續新 Story 處理。

---

## Changelog

| 版本 | 日期 | 變更內容 |
|------|------|----------|
| v0.1 | 2026-02-13 | 初版：建立全部模板（PROJECT_MEMORY、專案入口、BDD、SDD、API 契約、Test Scaffolding、反向工程流程） |
| v0.2 | 2026-02-13 | WebSocket 契約改用 AsyncAPI 3.0 格式 |
| v0.3 | 2026-02-13 | 新增 NFR 模板（含 ID 系統、Agent 執行流程、分層粒度）；BDD 標記擴充支援帶 ID 語法 `@perf(PERF-01)` |
| v0.4 | 2026-02-13 | 新增 DDD 格式指南（漸進式分裂策略、Level 1 Context Map 含 Mermaid、Level 2 Glossary 含型別約束、Level 3 Aggregate Root 嵌入 SDD）；Memory 衝突處理策略引用 Lifecycle |
| v0.5 | 2026-02-13 | Memory 模板重新設計：壓縮格式（省 62% token）、HTML 註解機器標記、三段式分層載入、英文大寫 Section 名稱；新增 Section 說明表（含權威來源與更新頻率） |
