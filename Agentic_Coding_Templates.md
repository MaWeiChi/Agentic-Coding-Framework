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

```markdown
# PROJECT_MEMORY

> 本文件由 AI Agent 自動維護，記錄專案的動態狀態。
> 人類也可以手動編輯，agent 會在下次啟動時讀取並尊重手動修改。

## Git 狀態

- **Last Commit**: `<hash>` — <commit message> (<date>)
- **Branch**: `<current branch>`
- **Uncommitted Changes**: 有 / 無（簡述）

## 已完成功能

| 功能 | 完成日期 | 相關 Story | 測試狀態 |
|------|----------|-----------|----------|
| 使用者註冊 | 2026-02-13 | US-001 | ✅ Unit + Integration + Component |
| 商品列表 | 2026-02-14 | US-003 | ✅ Unit + Integration |

## 當前任務

- **Story**: US-005 購物車功能
- **階段**: Implementation（TDD 綠燈進行中）
- **進度**: 後端 API 已完成，前端元件進行中
- **卡點**: 無 / 描述卡住的問題

## 未解決問題

| 問題 | 優先級 | 發現時間 | 備註 |
|------|--------|----------|------|
| 商品圖片在 Safari 上顯示異常 | Medium | 2026-02-14 | 可能是 WebP 支援問題 |

## 最近變更記錄

> 保留最近 5 筆，舊的移到 git log。

1. **2026-02-15** `a1b2c3d` — 完成購物車後端 API（加入/移除/更新數量）
2. **2026-02-14** `e4f5g6h` — 完成商品列表元件，含分頁與排序
3. **2026-02-14** `i7j8k9l` — 修正使用者註冊的 email 驗證邏輯

## 測試狀態

| 層級 | 狀態 | 最後執行 | 備註 |
|------|------|----------|------|
| Unit | ✅ 42/42 passed | 2026-02-15 | |
| Integration | ✅ 18/18 passed | 2026-02-15 | |
| Component | ✅ 12/12 passed | 2026-02-14 | 購物車元件測試尚未加入 |
| E2E | ⏸ 尚未執行 | — | 等購物車完成後跑里程碑 E2E |
| Performance | ⏸ 尚未執行 | — | |

## 連動提醒

> 記錄「改 A 要同步改 B」的隱性關聯，防止遺漏。

- 修改 `Product` model → 同步更新 OpenAPI spec + 前端 type 定義
- 修改認證邏輯 → 同步更新 middleware test + E2E 登入場景
- 修改 DB schema → 執行 migration + 更新 SDD 資料模型段落

## 下一步

> 依優先順序排列，agent 從第一項開始。

1. 完成購物車前端元件（對照 BDD 場景 US-005）
2. 撰寫購物車 Component Test
3. 處理 Safari WebP 圖片問題
4. 開始 US-006 結帳流程 BDD
```

### 撰寫原則

**簡潔優先**：Memory 是 agent 的快速定位工具，不是完整文件。每個區塊點到為止，細節留在對應的文件中（BDD、SDD、測試報告）。

**Agent 可執行**：「下一步」的描述要具體到 agent 能直接行動，避免模糊的描述。好的例子：「完成購物車前端元件（對照 BDD 場景 US-005）」。壞的例子：「繼續開發購物車」。

**Git 為錨**：每次更新 Memory 時，必須同步記錄當前的 git commit hash。這是跨工具校驗的基礎。

**人機共寫**：Agent 自動更新日常變動；人類手動編輯優先級調整、策略變更等 agent 無法判斷的內容。Agent 應尊重人類的手動修改，不自行覆蓋。

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

@perf
Scenario: <效能相關場景>
  Given <負載條件>
  When <觸發操作>
  Then <效能指標 + 具體數值>
```

### 撰寫原則

**一個場景驗證一件事**：避免在單一場景中塞太多 Then。如果一個場景的 Then 超過三條，考慮拆分。

**標記必填**：每個場景至少一個測試層級標記。這是 Test Scaffolding 的驅動依據，缺標記的場景不會被自動產出測試。

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
