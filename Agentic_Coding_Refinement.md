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

## 必做（8 條）— 全部已納入

### ~~1. TDD 遞迴上限~~ → **已納入** Lifecycle v0.2 + Protocol v0.1（max_attempts）

### ~~2. 資料模型 Source of Truth~~ → **已納入** Templates v0.7（SDD 撰寫原則）

### ~~3. Non-Goals / Out of Scope~~ → **已納入** Templates v0.7（BDD + SDD Delta Spec）

### ~~4. Scenario Outline（參數化場景）~~ → **已納入** Templates v0.7（BDD 模板）

### ~~5. AST Linting 整合~~ → **已納入** Lifecycle v0.2 + Protocol v0.1（post_check）

### ~~6. Helper Function 提取原則~~ → **已納入** Templates v0.7（Test Scaffolding 撰寫原則）

### ~~7. Subdomain 分類~~ → **已納入** Templates v0.7（DDD Level 1 Context Map）

### ~~8. testify 模式對接~~ → **已納入** Templates v0.7（Test Scaffolding：require/assert + Table-Driven + Suite）

---

## 值得做（5 條）— 全部已納入

| # | 建議 | 狀態 |
|---|------|------|
| ~~9~~ | **宣告式風格指引** | **已納入** Templates v0.7（BDD 撰寫原則） |
| ~~10~~ | **System Context 描述** | **已納入** Templates v0.7（SDD 撰寫原則） |
| ~~11~~ | **Mermaid 圖表指引** | **已納入** Templates v0.7（SDD 撰寫原則） |
| ~~12~~ | **Anti-Pattern 清單** | **已納入** Templates v0.7（BDD 撰寫原則） |
| ~~13~~ | **Domain Event Registry** | **已納入** Templates v0.7（DDD 格式指南） |

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
| ~~動態 context 載入~~ | ~~實作層議題~~ → **已納入** Protocol v0.4 Multi-Executor 的 Scoped Context Loading |
| ~~Test/Impl context 隔離~~ | ~~實作層議題~~ → **已納入** Protocol v0.4 Multi-Executor 的 Role-Based Context 隔離 |
| Aggregate 設計原則 | Level 3 才觸發，太早定義 |
| Context 演進策略 | 極少數專案會碰到 |
| Runtime View | BDD 場景已描述行為 |
| Cross-cutting Concerns | 可併入 Constitution |
| Deployment View | 框架刻意排除，止於 image push |
| ~~Agent 訂閱機制~~ | ~~多 agent 協作實作層~~ → **已納入** Protocol v0.4 Multi-Executor 的 Coordinator ↔ Executor 通訊 |
| ~~YAML 交接格式~~ | ~~多 agent 協作實作層~~ → **已納入** Protocol v0.4 Multi-Executor 的 Per-Task HANDOFF + Protocol v0.5 HANDOFF.md 混合格式（YAML front matter） |
| 多語言 Test Scaffolding | 按需擴充，不需預先定義 |

---

## 影響範圍摘要

| 文件 | 必做 | 值得做 | 合計 | 狀態 |
|------|:----:|:-----:|:----:|:----:|
| Templates → BDD | 2 | 2 | 4 | ✅ 全部已納入 |
| Templates → SDD | 2 | 2 | 4 | ✅ 全部已納入 |
| Templates → Test | 2 | 0 | 2 | ✅ 全部已納入 |
| Templates → DDD | 1 | 1 | 2 | ✅ 全部已納入 |
| Lifecycle | 2 | 0 | 2 | ✅ 全部已納入 |
| **Framework 主文件** | **0** | **0** | **0** | — |
| **合計** | **8** | **5** | **13** | **✅ 13/13** |

---

## Changelog

| 版本 | 日期 | 變更 |
|------|------|------|
| v0.1 | 2026-02-13 | 初版：從 30 條比較建議中以 Token/品質/智慧化三維度篩選為 13 條（8 必做 + 5 值得做） |
| v0.2 | 2026-02-14 | 更新狀態：全部 13 條已納入（8 必做→Templates v0.7 + Lifecycle v0.2 + Protocol v0.1；5 值得做→Templates v0.7）；4 條「不納入」項目已納入 Protocol v0.4 Multi-Executor 協作模式 |
