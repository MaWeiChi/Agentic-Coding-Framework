# Agentic Coding Framework

**AI 協作開發的專案上下文基礎建設**

Discussion Summary | February 2026

---

## 相關文件

| 文件 | 內容 | Agent 載入時機 |
|------|------|---------------|
| 本文件 | 框架本體：分層定義、核心原則、流程 | 每次對話必讀 |
| [Agentic_Coding_Lifecycle.md](Agentic_Coding_Lifecycle.md) | 運作機制：迭代模型、測試策略、CI/CD 接口 | 規劃迭代或設定 CI 時載入 |
| [Agentic_Coding_Templates.md](Agentic_Coding_Templates.md) | 框架細節：各層文件模板、撰寫指南、範例 | 撰寫 BDD/SDD/契約/Memory 時載入 |
| PROJECT_MEMORY.md（專案層級） | 動態狀態追蹤：進度、任務、測試狀態、git 校驗 | 每次對話必讀（與專案摘要搭配） |

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

### 動態狀態層：PROJECT_MEMORY.md

專案摘要記錄穩定不變的 Why / Who / What，PROJECT_MEMORY.md 記錄持續變化的「現在到哪了、接下來做什麼」。兩者搭配使用，agent 每次對話時一併讀取。

Memory 是獨立於任何特定 AI 工具的檔案，放在專案根目錄。內含 git commit 校驗機制，讓 agent 在跨工具使用時能察覺中間是否有未記錄的變更並自動同步。更新時機定義在 [Lifecycle 文件](Agentic_Coding_Lifecycle.md)，模板定義在 [Templates 文件](Agentic_Coding_Templates.md)。

### 第二層：BDD（Behavior-Driven Development）

以 Given / When / Then 格式描述使用者行為與預期結果。對 agent 特別有用，因為它同時是需求規格和驗收標準——agent 寫完 code 可以直接對照 BDD 場景自我驗證。

粒度較粗，對應的是使用者場景。BDD 場景應加上測試層級標記（`@unit`、`@integration`、`@component`、`@e2e`、`@perf`、`@load`），詳見 [Lifecycle 文件](Agentic_Coding_Lifecycle.md)的測試策略段落。

### 第三層：SDD（Software Design Document）

定義架構決策、技術選型、模組邊界。避免 agent 每次都要「猜」你想用什麼框架、資料怎麼流動。

BDD 場景拆解出需要哪些模組和介面，這些都記錄在 SDD 中。

### 介面層：OpenAPI / AsyncAPI 契約

對於前後端分離的專案，具體的介面定義讓 agent 在處理前後端時不用猜測介面長什麼樣，直接根據契約實作。REST API 使用 OpenAPI 格式，事件驅動介面（WebSocket、MQTT 等）使用 AsyncAPI 格式。

### Review Checkpoint（人類審查）

在進入實作之前的明確審查點。此時 BDD、SDD、API 契約都已產出，人類介入確認方向正確。這是修改成本最低的階段——一旦進入實作，回頭改 SDD 的代價就高很多。

### 第四層：TDD（Test-Driven Development）

分為兩個明確步驟：

**Test Scaffolding（紅燈）**：根據 BDD 場景標記和 API 契約，先產出對應層級的測試檔案骨架。此時還沒有實作代碼，所有測試全部失敗。這一步的價值在於讓 agent 先證明它理解了需求。

**Implementation（綠燈）**：agent 讀取 SDD、API 契約和失敗的測試日誌，寫最少量的 code 讓測試通過，然後 refactor。每一輪 agent 都可以自己跑測試驗證，不需要人類介入，這是最省 token 的地方。

---

## 可選擴充

### ADR（Architecture Decision Records）

SDD 記錄「現在的架構長怎樣」，ADR 記錄「為什麼選 A 不選 B」。防止 agent「好心重構」把有特定原因的設計改壞。可併入 SDD，不一定需要獨立檔案。

最佳產生時機：當你做了有爭議的決策時，當下順手記一筆即可。

### DDD Strategic Design（Domain-Driven Design 戰略設計）

當專案涉及多個業務領域、同一名詞在不同模組代表不同概念時觸發。位置在專案摘要之後、BDD 之前，用來劃定 agent 的工作邊界。

建議採用輕量級 DDD，由淺入深分三個 level：

- **Level 1（建議）**：Bounded Context——將系統切分為獨立模組，每個 Context 有自己的 API 契約和資料夾結構。解決 agent 上下文溢出問題，agent 只需讀取當前 Context 的內容。
- **Level 2（建議）**：Ubiquitous Language——建立 `glossary.md` 通用語言表，強制 agent 在命名變數和欄位時查閱。解決概念混淆問題，如「Sales Context 的 User 稱為 Customer，Shipping Context 的 User 稱為 Recipient」。
- **Level 3（可選）**：Aggregate Root——在 SDD 中標示聚合根，約束 agent 必須透過聚合根操作資料，提升封裝性。

觸發條件：專案出現跨領域名詞衝突、單一 Context Window 塞不下整個 codebase、或需要多個 agent 各負責一個模組時。單一領域的專案可跳過。

### NFR（Non-Functional Requirements）

效能、安全性、可用性等約束。Agent 預設會寫出「功能正確」的 code，但不會主動考慮這些非功能性約束。

建議在開發中實際碰到問題時再補進去，不用一開始就追求完備。效能測試的具體基準定義在 NFR 文件中，由 BDD 場景的 `@perf` / `@load` 標記觸發。

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
| ADR / NFR / DDD 可迭代補充 | 不用一開始追求完備，踩到坑再補 |
| 規模決定深度 | 小型 CRUD 四層即可，分散式系統才需要更多文件 |

---

## Gemini「Agentic Waterfall」建議的取捨

討論中參考了 Gemini 提出的角色分工（Product Manager Agent、Architect Agent、QA Agent、Coder Agent）方案。評估後的結論：

**吸收的部分：** Review Checkpoint 的概念（已納入框架）、Test Scaffolding 先行（已納入 TDD 階段）。

**獨立議題：** 角色分工（Agent Teams）。本框架定義的是「專案需要哪些文件、什麼順序產出」，與最終由一個 agent 還是多個 agent 執行無關。框架是工作的藍圖，agent teams 是執行的編制，兩者可獨立討論，組合時也不衝突。Self-correction loop 本質上就是 TDD 循環本身，不需要額外框架化。

---

## 待探討事項

以下主題可在後續討論中深入探討：

**框架細節（納入 [Templates 文件](Agentic_Coding_Templates.md)）：**
- 各層文件的具體模板與範例
- BDD 場景的撰寫最佳實踐
- SDD 應包含哪些最小必要資訊
- CLAUDE.md 的結構設計
- 既有專案的反向工程實作流程
- 如何讓 agent 根據 BDD 和 SDD 自動推導 TDD 測試案例

**迭代機制與開發生命週期（已納入 [Lifecycle 文件](Agentic_Coding_Lifecycle.md)）：**
- ~~執行粒度：以 User Story 為單位的微觀瀑布循環~~（v0.4）
- ~~SDD 與 API 契約的增量更新策略~~（v0.4）
- ~~巨觀敏捷 vs. 微觀瀑布的運作方式~~（v0.5）
- ~~Story 相依性處理策略~~（v0.5）
- ~~E2E 測試策略~~（v0.6）
- ~~CI/CD 與框架的接口~~（v0.7）
- ~~DevOps 信任邊界~~（v0.7）
- 如何將上述流程與本框架串接成完整的開發生命週期

**專案層級（不納入框架，由各專案 SDD 自行記錄）：**
- 具體 CI/CD pipeline 配置（GitHub Actions YAML、Dockerfile 等）

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
| v0.7 | 2026-02-13 | 新增「CI/CD 與框架的接口」：BDD 標記驅動 CI 觸發時機、Agent 信任邊界（負責到 image push，不介入部署）、不同專案型態的 CD 差異處理原則 |
| v0.8 | 2026-02-13 | 拆分文件：將運作機制移至 Lifecycle 文件、框架細節移至 Templates 文件；主文件精簡為框架本體 + 交叉引用 |
| v0.9 | 2026-02-13 | 新增可選擴充「DDD Strategic Design」：輕量級三層（Bounded Context / Ubiquitous Language / Aggregate Root），定位為條件觸發，專案涉及多業務領域時啟用 |
| v0.10 | 2026-02-13 | 打包為 Cowork Skill（中文版）：SKILL.md + references/framework.md + references/lifecycle.md（待 Templates 完成後重新打包） |
| v0.11 | 2026-02-13 | 新增「動態狀態層：PROJECT_MEMORY.md」：定位為獨立於特定 AI 工具的跨工具狀態追蹤文件，含 git commit 校驗機制；更新相關文件表格 |
