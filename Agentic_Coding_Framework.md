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

### Bootstrap（一次性）

專案摘要（Why / Who / What）和初始 SDD 骨架在專案啟動時做一次。這個階段的目標是建立整個專案的上下文基礎，讓後續每個 User Story 的迭代都有穩定的錨點可以參照。

對於既有專案，Bootstrap 對應的就是「掃描 Codebase → 反向產出文件 → 人工校正」那個流程。

### 迭代執行（每個 User Story 一輪）

Bootstrap 完成後，每個 User Story 進入一次獨立的微觀瀑布循環：

| 步驟 | 說明 |
|------|------|
| BDD | 只撰寫**當前這個 Story** 的行為場景 |
| SDD 增量更新 | 追加或修改受影響的模組與架構段落，不重寫整份 SDD |
| API 契約增量更新 | 新增或調整受影響的 endpoint / event，不重寫整份契約 |
| **Review Checkpoint** | **人類確認本輪 BDD + SDD 差異 + 契約差異** |
| Test Scaffolding | 根據本輪 BDD 場景產出測試骨架（紅燈） |
| Implementation | 實作讓測試通過 → Refactor |

### 為什麼是「增量更新」而非「重寫」

SDD 和 API 契約是**活文件**（living documents），每個 Story 只動受影響的部分。這有兩個好處：

- **省 token**：agent 不需要每次重新生成整份 SDD，只需要讀取現有內容、追加差異。
- **降低風險**：不會因為重寫而意外丟失先前的設計決策或 ADR 中記錄的取捨。

實務上，這意味著 SDD 檔案中應該有清楚的模組邊界劃分，讓每次增量更新的範圍容易界定。

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
- 巨觀敏捷 vs. 微觀瀑布的運作方式
- E2E 測試策略
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
