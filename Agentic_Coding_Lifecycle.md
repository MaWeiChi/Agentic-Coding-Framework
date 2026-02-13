# Agentic Coding Lifecycle

**迭代機制、測試策略、CI/CD 接口**

本文件是 [Agentic Coding Framework](Agentic_Coding_Framework.md) 的運作機制補充，說明框架在時間軸上如何運作。

---

## 執行粒度與迭代模型

框架分層描述了「需要哪些文件、什麼順序產出」，但沒有說明跨多個 User Story 時如何運作。這裡補充框架的時間軸維度。

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
| **Update Memory** | **更新 PROJECT_MEMORY.md（詳見下方規則）** |

### Story 之間的相依性處理

Story 之間的相依分為兩種：

**技術相依**——Story B 需要 Story A 產出的模組或資料結構才能開始（例如「使用者登入」必須先於「個人頁面」）。這種相依是硬性的，按依賴順序排進迭代即可。因為介面已在 Bootstrap 時定好，被依賴的 Story 完成後，後續 Story 的 SDD 增量更新通常只需微調。

**功能相依**——多個 Story 共用某些模組但不互相阻塞（例如「商品搜尋」和「商品收藏」都依賴商品列表元件）。這類 Story 可以平行進入微觀瀑布，各自的 SDD 增量更新如果觸及同一模組，在 Review Checkpoint 時由人類確認沒有衝突。

**開發中才發現的相依**——做 Story C 時才發現它依賴 Story A 的某個元件。此時回到 SDD 補上依賴關係，評估是暫停 C 先做 A，還是先定義 A 的元件介面（stub）讓 C 繼續。這是巨觀敏捷發揮作用的地方——Story 排序可以動態調整。

**啟發式規則：** Story 的拆分應盡量採用垂直切片（vertical slice，從 UI 到 API 到 DB 一刀到底），而非水平分層，這能天然減少 Story 間的相依。若相依鏈超過兩層（A → B → C），應回頭檢視 Story 拆分或 SDD 的模組邊界是否合理。

### PROJECT_MEMORY 更新時機與規則

Memory 的更新嵌入微觀瀑布流程，由 agent 在特定時機自動執行。

**Session 啟動時（每次對話開始）：**

1. 讀取 PROJECT_MEMORY.md
2. 比對 git commit hash（詳見 [Templates 文件](Agentic_Coding_Templates.md) 的 Git Commit 校驗機制）
3. 若不一致，先同步 Memory 再開始工作

**Story 完成時（微觀瀑布最後一步）：**

| Memory 區塊 | 更新內容 |
|-------------|----------|
| Git 狀態 | 更新為當前 commit hash |
| 已完成功能 | 追加本次 Story 的功能與測試狀態 |
| 當前任務 | 清除或更新為下一個 Story |
| 最近變更記錄 | 追加本次 commit（保留最近 5 筆） |
| 測試狀態 | 更新各層級的通過數與執行時間 |
| 下一步 | 根據完成情況重新排列優先順序 |

**中途中斷時（Session 異常結束或手動停止）：**

Agent 應盡可能在中斷前更新 Memory 的「當前任務」區塊，記錄進行到哪一步、卡在什麼問題，讓下次接手的 agent（可能是不同工具）能繼續。

**人類手動編輯時：**

Agent 在下次啟動時讀取 Memory，應辨識並尊重人類的手動修改（如優先級調整、新增待辦事項、策略變更等），不自行覆蓋。

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

功能測試的標準來自 BDD 場景，效能測試的標準來自 NFR 文件。隨著 Story 累積，之前通過的測試持續作為迴歸保護——這是 CI 的職責，在下方 CI/CD 段落中進一步說明。

---

## CI/CD 與框架的接口

本段落定義 CI/CD 與框架其他部分的關係，不涉及具體 pipeline 實作或部署目標的配置。

### CI：BDD 標記驅動的自動化測試

CI 是測試策略的執行引擎。BDD 場景的 tag 同時驅動兩件事：agent 在 Test Scaffolding 時產出哪些測試，以及 CI 在什麼時機跑哪些測試。

| 觸發時機 | 執行的測試標記 | 對應的框架階段 |
|----------|---------------|---------------|
| PR / Push | `@unit` + `@integration` + `@component` | 微觀瀑布 TDD + Component Test |
| Merge 到主分支 | 上述 + `@e2e` | 跨 Story 里程碑驗證 |
| 定期 / 手動 | `@perf` + `@load` | NFR 驗證 |

CI 同時負責迴歸保護：隨著 Story 累積，先前通過的測試在每次 PR 時重跑，確保新 Story 沒有破壞舊功能。這是 agent self-correction loop 的延伸——agent 在本地跑一輪，CI 在合併前再跑一輪確保沒有環境差異。

### CD：Agent 的信任邊界

在這套框架裡，CD 的關鍵不是「怎麼部署」（那是 infrastructure 層的配置），而是 agent 的職責到哪裡結束。

**Agent 負責到：** CI 全綠 + Container image build 成功 + push 到 registry。

**Agent 不介入：** 從 registry 到目標環境的部署。不論目標是 IoT 上的 Docker、未來的 K8s、或 cloud service，都是 infrastructure 層的事。

這條邊界的好處是：部署目標怎麼變，框架本身不需要修改。Agent 的產出物永遠是一個通過所有測試的 container image，部署方式是 infrastructure 的配置問題。

### 不同專案型態的 CD 差異

不同專案型態（Go container 服務、WordPress CMS、Astro + WordPress headless 等）的部署方式差異大，不適合在框架層級統一。建議在 SDD 中標注專案的部署類型，由專案層級的 CI/CD 配置處理差異。框架的前半段（BDD → SDD → TDD → CI 測試）對所有專案型態是通用的。
