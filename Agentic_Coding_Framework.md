# Agentic Coding Framework

**AI 協作開發的專案上下文基礎建設**

Discussion Summary | February 2026

---

## 核心理念

在 Agentic Coding 的脈絡下，token 就是成本。前期建立好專案的「上下文基礎建設」能大幅減少後續每次對話的重複說明，降低整體開發成本。

這套框架的本質是強迫專案把隱性知識顯性化。如果專案連人類讀了都搞不清楚狀況，agent 也不會搞得清楚。因此，這套框架同時服務於 AI 與人類團隊成員的入職需求。

---

## 框架分層

### 第一層：專案摘要（Project Summary）

用幾句話讓 agent 快速定位專案的核心資訊，建議放在專案根目錄（如 `CLAUDE.md` 或 `PROJECT_CONTEXT.md`），每次開啟對話時 agent 讀一次即可。

- **Why** — 專案目的：解決什麼問題？
- **Who** — 使用者：給誰用？
- **What** — 成品：最終產出是什麼？

### 第二層：BDD（Behavior-Driven Development）

以 Given / When / Then 格式描述使用者行為與預期結果。對 agent 特別有用，因為它同時是需求規格和驗收標準——agent 寫完 code 可以直接對照 BDD 場景自我驗證。

粒度較粗，對應的是使用者場景。

### 第三層：SDD（Software Design Document）

定義架構決策、技術選型、模組邊界。避免 agent 每次都要「猜」你想用什麼框架、資料怎麼流動。

BDD 場景拆解出需要哪些模組和介面，這些都記錄在 SDD 中。

### 介面層：OpenAPI / WebSocket 契約

對於前後端分離的專案，具體的介面定義讓 agent 在處理前後端時不用猜測介面長什麼樣，直接根據契約實作。

### Review Checkpoint（人類審查）

在進入實作之前的明確審查點。此時 BDD、SDD、API 契約都已產出，人類介入確認方向正確。這是修改成本最低的階段——一旦進入實作，回頭改 SDD 的代價就高很多。

### 第四層：TDD（Test-Driven Development）

分為兩個明確步驟：

**Test Scaffolding（紅燈）**：根據 BDD 場景和 API 契約，先產出測試檔案骨架。此時還沒有實作代碼，所有測試全部失敗。這一步的價值在於讓 agent 先證明它理解了需求。

**Implementation（綠燈）**：agent 讀取 SDD、API 契約和失敗的測試日誌，寫最少量的 code 讓測試通過，然後 refactor。每一輪 agent 都可以自己跑測試驗證，不需要人類介入，這是最省 token 的地方。

---

## 可選擴充

### ADR（Architecture Decision Records）

SDD 記錄「現在的架構長怎樣」，ADR 記錄「為什麼選 A 不選 B」。防止 agent「好心重構」把有特定原因的設計改壞。可併入 SDD，不一定需要獨立檔案。

最佳產生時機：當你做了有爭議的決策時，當下順手記一筆即可。

### NFR（Non-Functional Requirements）

效能、安全性、可用性等約束。Agent 預設會寫出「功能正確」的 code，但不會主動考慮這些非功能性約束。

建議在開發中實際碰到問題時再補進去，不用一開始就追求完備。

---

## 新專案 vs. 既有專案

不管專案新舊，最終都收斂到同一組文件作為 agent 的工作基礎。差別只在產出路徑不同。

### 新專案流程

往前定義，主動建構上下文給 agent。

| 步驟 | 說明 |
|------|------|
| 專案摘要 | 定義 Who / What / Why |
| BDD | 撰寫使用者行為場景 |
| SDD | 定義架構與模組劃分 |
| OpenAPI / WS | 制定前後端介面契約 |
| **Review Checkpoint** | **人類審查確認方向正確** |
| Test Scaffolding | 產出測試骨架（全部紅燈） |
| Implementation | 實作讓測試通過 → Refactor |

### 既有專案流程

往回萃取，從現有 codebase 反向產出文件。

| 步驟 | 說明 |
|------|------|
| 掃描 Codebase | Agent 讀專案結構、關鍵檔案 |
| 反向產出文件 | 產出專案摘要 + BDD + SDD |
| 人工校正 | 你確認並補充隱性知識 |
| 補 Characterization Test | 描述現有行為，建立基線 |
| 正常流程 | 後續新功能進入 BDD → SDD → TDD |

既有專案的額外注意事項：部分隱性架構決策或歷史包袱是 agent 從 code 裡讀不出來的，需要手動補進 SDD，避免 agent「好心重構」改壞設計。

---

## 核心原則

| 原則 | 說明 |
|------|------|
| 越穩定的資訊越早固定 | Agent 不需反覆推斷，每次對話只處理差異部分 |
| 按需載入 | 常用資訊放 CLAUDE.md，偶爾需要的放獨立檔案 |
| 雙重回報 | 同時服務 AI agent 與人類團隊成員 |
| ADR / NFR 可迭代補充 | 不用一開始追求完備，踩到坑再補 |
| 規模決定深度 | 小型 CRUD 四層即可，分散式系統才需要更多文件 |

---

## 執行粒度與迭代模型

上面的框架分層描述了「需要哪些文件、什麼順序產出」，但沒有說明跨多個 User Story 時如何運作。這裡補充框架的時間軸維度。

### 巨觀敏捷 × 微觀瀑布

本框架採用兩層結構：**Story 之間是敏捷的，Story 內部是瀑布的。**

微觀瀑布指的是單一 User Story 內的步驟（BDD → SDD 增量更新 → 契約更新 → Review → TDD → Implementation）嚴格順序執行。順序性在這個粒度下是優勢——每一步都有明確的輸入和輸出，agent 不需要做模糊的判斷。

巨觀敏捷指的是 Story 之間的排序、優先級、需求變更保持彈性。你可以在第三個 Story 做完後發現方向不對，砍掉第四個，插入新的。每個 Story 是獨立的迭代單元，微觀瀑布不會限制巨觀層的靈活性。

這個組合適合 Agentic Coding 的原因：傳統瀑布的風險（方向錯了浪費整個專案）被壓縮到單一 Story 的範圍；同時 agent 擅長的「明確輸入 → 明確產出」模式在微觀瀑布中得到充分發揮。巨觀層的戰略判斷（哪些 Story 先做、要不要 pivot）則留給人類。

### Bootstrap（一次性）

專案摘要（Why / Who / What）和初始 SDD 骨架在專案啟動時做一次。這個階段的目標是建立整個專案的上下文基礎，讓後續每個 User Story 的迭代都有穩定的錨點可以參照。

Bootstrap 階段除了專案摘要和 SDD 骨架，也應把已知的模組間介面（internal interface）定義出來——至少到函式簽名和資料結構的層級。這是 contract-first 的做法，讓後續 Story 可以對著介面開發，降低 Story 之間的耦合。

對於既有專案，Bootstrap 對應的就是「掃描 Codebase → 反向產出文件 → 人工校正」那個流程。

### 迭代執行（每個 User Story 一輪）

Bootstrap 完成後，每個 User Story 進入一次獨立的微觀瀑布循環：

| 步驟 | 說明 |
|------|------|
| BDD | 只撰寫**當前這個 Story** 的行為場景 |
| SDD 增量更新 | 追加或修改受影響的模組與架構段落，不重寫整份 SDD |
| API 契約增量更新 | 新增或調整受影響的 endpoint / event，不重寫整份契約 |
| **Review Checkpoint** | **人類確認本輪 BDD + SDD 差異 + 契約差異** |
| Test Scaffolding | 根據本輪 BDD 場景標記產出對應層級的測試骨架（紅燈） |
| Implementation | 實作讓測試通過 → Refactor |
| Component Test | 驗證前端元件行為（Playwright component testing） |

### Story 之間的相依性處理

Story 之間的相依分為兩種：

**技術相依**——Story B 需要 Story A 產出的模組或資料結構才能開始（例如「使用者登入」必須先於「個人頁面」）。這種相依是硬性的，按依賴順序排進迭代即可。因為介面已在 Bootstrap 時定好，被依賴的 Story 完成後，後續 Story 的 SDD 增量更新通常只需微調。

**功能相依**——多個 Story 共用某些模組但不互相阻塞（例如「商品搜尋」和「商品收藏」都依賴商品列表元件）。這類 Story 可以平行進入微觀瀑布，各自的 SDD 增量更新如果觸及同一模組，在 Review Checkpoint 時由人類確認沒有衝突。

**開發中才發現的相依**——做 Story C 時才發現它依賴 Story A 的某個元件。此時回到 SDD 補上依賴關係，評估是暫停 C 先做 A，還是先定義 A 的元件介面（stub）讓 C 繼續。這是巨觀敏捷發揮作用的地方——Story 排序可以動態調整。

**啟發式規則：** Story 的拆分應盡量採用垂直切片（vertical slice，從 UI 到 API 到 DB 一刀到底），而非水平分層，這能天然減少 Story 間的相依。若相依鏈超過兩層（A → B → C），應回頭檢視 Story 拆分或 SDD 的模組邊界是否合理。

### 為什麼是「增量更新」而非「重寫」

SDD 和 API 契約是**活文件**（living documents），每個 Story 只動受影響的部分。這有兩個好處：

- **省 token**：agent 不需要每次重新生成整份 SDD，只需要讀取現有內容、追加差異。
- **降低風險**：不會因為重寫而意外丟失先前的設計決策或 ADR 中記錄的取捨。

實務上，這意味著 SDD 檔案中應該有清楚的模組邊界劃分，讓每次增量更新的範圍容易界定。

---

## 測試策略

### BDD 場景標記

BDD 場景應加上測試層級標記（tag），讓 agent 在 Test Scaffolding 階段根據標記自動產出對應層級的測試骨架。一個場景可以有多個標記，代表它需要在不同層級被驗證。

```gherkin
@unit @component
Scenario: 使用者輸入無效 email 時顯示錯誤訊息
  Given 使用者在註冊頁面
  When 輸入 "not-an-email" 到 email 欄位
  Then 顯示 "請輸入有效的 email 地址"

@e2e
Scenario: 使用者完成完整註冊流程
  Given 使用者在首頁
  When 點擊註冊按鈕
  And 填寫所有必填欄位
  And 提交表單
  Then 導向歡迎頁面
  And 收到確認信

@perf
Scenario: 商品搜尋在高併發下維持回應時間
  Given 系統承受 1000 併發使用者
  When 同時發送搜尋請求
  Then 95th percentile 回應時間 < 200ms
```

可用標記：`@unit`、`@integration`、`@component`、`@e2e`、`@perf`、`@load`。效能相關標記的具體基準定義在 NFR 文件中。

### 測試金字塔

| 層級 | 範圍 | 時機 | 工具 |
|------|------|------|------|
| Unit Test | 單一函式 / 模組邏輯 | 每個 Story TDD 階段 | Go: `testing` + `testify` |
| API Integration Test | 後端 API 契約驗證 | 每個 Story TDD 階段 | Go: `net/http/httptest` + `testify` |
| Component Test | 前端元件行為（隔離） | 每個 Story Implementation 後 | Playwright component testing |
| Performance / Load Test | 效能基準驗證 | 標記 `@perf` 的 Story 或里程碑 | k6, vegeta |
| Full E2E Test | 完整使用者流程（前後端） | 跨 Story 里程碑 | Playwright browser testing |

### 測試時機與微觀瀑布的整合

測試在微觀瀑布中分為兩個階段執行：

**TDD 階段（Story 內，快速迴圈）：** Unit Test + API Integration Test。這是 agent 的 self-correction loop，每次實作都跑，feedback 必須快。後端為主，不依賴前端環境。Agent 看到 `@unit` 和 `@integration` 標記的 BDD 場景，產出對應的 Go 測試骨架。

**Implementation 後（Story 內，驗證前端）：** Component Test。驗證該 Story 涉及的前端元件行為，使用 Playwright component testing 隔離執行，不需要完整的應用環境。Agent 看到 `@component` 標記的場景，產出 Playwright 測試。

**里程碑（跨 Story）：** Full E2E Test + Performance Test。累積多個相關 Story 完成後，統一跑 Playwright full browser test 和 k6/vegeta 壓力測試。這一層需要前後端都就緒，不適合每個 Story 都跑。標記 `@e2e` 和 `@perf` 的場景在此階段執行。

### 測試與其他文件的關係

功能測試的標準來自 BDD 場景，效能測試的標準來自 NFR 文件。隨著 Story 累積，之前通過的測試持續作為迴歸保護——這是 CI 的職責，在 CI/CD 段落中進一步說明。

---

## Gemini「Agentic Waterfall」建議的取捨

討論中參考了 Gemini 提出的角色分工（Product Manager Agent、Architect Agent、QA Agent、Coder Agent）方案。評估後的結論：

**吸收的部分：** Review Checkpoint 的概念（已納入框架）、Test Scaffolding 先行（已納入 TDD 階段）。

**獨立議題：** 角色分工（Agent Teams）。本框架定義的是「專案需要哪些文件、什麼順序產出」，與最終由一個 agent 還是多個 agent 執行無關。框架是工作的藍圖，agent teams 是執行的編制，兩者可獨立討論，組合時也不衝突。Self-correction loop 本質上就是 TDD 循環本身，不需要額外框架化。

---

## 待探討事項

以下主題可在後續討論中深入探討：

**框架細節：**
- 各層文件的具體模板與範例
- BDD 場景的撰寫最佳實踐
- SDD 應包含哪些最小必要資訊
- CLAUDE.md 的結構設計
- 既有專案的反向工程實作流程
- 如何讓 agent 根據 BDD 和 SDD 自動推導 TDD 測試案例

**迭代機制與開發生命週期：**
- ~~執行粒度：以 User Story 為單位的微觀瀑布循環~~（v0.4 已納入）
- ~~SDD 與 API 契約的增量更新策略~~（v0.4 已納入）
- ~~巨觀敏捷 vs. 微觀瀑布的運作方式~~（v0.5 已納入）
- ~~Story 相依性處理策略~~（v0.5 已納入）
- ~~E2E 測試策略~~（v0.6 已納入）
- CI/CD pipeline 設計
- DevOps 與部署流程
- 如何將上述流程與本框架串接成完整的開發生命週期

---

## Changelog

| 版本 | 日期 | 變更內容 |
|------|------|----------|
| v0.1 | 2026-02-13 | 初版：建立四層核心框架（專案摘要 → BDD → SDD → TDD），確立新舊專案雙路徑，定義可選擴充（ADR / NFR） |
| v0.2 | 2026-02-13 | 納入 Gemini「Agentic Waterfall」建議：加入 Review Checkpoint、TDD 拆分為 Test Scaffolding + Implementation |
| v0.3 | 2026-02-13 | 釐清角色分工（Agent Teams）為獨立議題；納入 Gemini「巨觀敏捷 / 微觀瀑布」觀點，列入下一階段待探討事項；修正專案摘要為 Why / Who / What |
| v0.4 | 2026-02-13 | 新增「執行粒度與迭代模型」：定義 Bootstrap 一次性 + User Story 微觀瀑布循環，明確 SDD 與 API 契約為增量更新而非重寫 |
| v0.5 | 2026-02-13 | 擴充「執行粒度與迭代模型」：加入巨觀敏捷 × 微觀瀑布兩層結構說明、Story 相依性處理策略（技術相依 / 功能相依 / 動態發現）、Bootstrap 階段 internal interface 定義、垂直切片啟發式規則 |
| v0.6 | 2026-02-13 | 新增「測試策略」：BDD 場景標記（@unit / @integration / @component / @e2e / @perf）、測試金字塔五層定義、測試時機與微觀瀑布整合、Go 後端 + Playwright 前端工具鏈 |
