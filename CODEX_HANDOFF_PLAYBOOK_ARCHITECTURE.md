# Codex Handoff｜Playbook-first 自主 AI 工作系統（架構重新設計）

> **交接日期**：2026-10-22（Asia/Taipei）  
> **階段**：設計討論／架構探索，**尚未決定實作細節，也沒有要求開始編碼**。  
> **用途**：將這份 Markdown 交給新的 Codex Session，直接接續本次已達成的共識。  
> **最重要的提醒**：這是**推倒重做的新方案**，不是舊版「57 Roles／27 LEGO Blocks」的增修版。舊文件只能當作需求與失敗經驗的參考，不是新設計的權威規格。

---

## 0. Codex 請先遵守的交接約定

1. **先討論，不要直接寫程式、修改 Repo、建立文件、安裝 Skill 或宣告架構已定案。** 使用者目前在做架構取捨；Codex 的第一項工作是深化設計論證。
2. **延續已決策的 B 方案，不能退回 A，也不要默默改寫成折衷版。** Playbook 不直接呼叫其他 Playbook；**只有 Workflow Engine** 組裝、排程及觸發跨 Playbook 工作。
3. **不要把 57 個職稱或原本 27 個積木當作不可改的限制。** 可以完全捨棄原架構；保留的是使用者真正的目標與已辨識的工程不變條件。
4. **全程遵守 P00 實證回答原則**：直接回答、不迎合、不為反對而反對；明確區分事實、推論、假設與未知；聲稱某機制可以保證安全時，必須交代真正的程式控制點。
5. **不要再用新增 Agent 解決每個問題。** 首先判斷確定性程式／腳本、現有 Executor + Skill 或 Playbook 是否足夠；只有獨立性、權限、並行效益或隔離需求才啟動額外 Session。
6. **不要把 Playbook 誤認為 Prompt／Agent Persona。** Playbook 是可執行、可版本化、可驗收、可改進的工作契約。
7. **不捏造目前的完成度。** 先前有文檔、SQLite 參考實作、契約測試草案；並**未**完成正式 Claude/Codex Runner、GitLab、真實授權、真實終止隔離、部署與跨 Repo 端到端驗證。
8. 使用**繁體中文及台灣用語**。盡量提供專業實作機制、取捨及反例，不重複讚美使用者的設計，也不提出空泛結論。

## 1. 使用者真正想建立的系統

**長期目標**：一套可持續運作、可自由組裝的自主 AI 工作平台。完整組裝範例是一個 AI 自主產品孵化流程：

`發現市場需求 → 蒐集／驗證證據 → 多視角評估 → 立項及授權 → 規格與開發 → 獨立 QA/Review → MR/部署 → 追蹤市場結果 → 改善工作方法`

使用者強調的不是模擬一家公司有多少位員工，而是：

> **重點不是建立更多 Agent，而是讓 Agent 擁有更可靠、可重複使用、能持續改善的工作方法。**

平台同時必須支援**積木式使用**。例如單獨執行市場研究、商機評估、工程開發與驗收、報告產生、Skill 評估等，不應為其中一件事啟動整個公司。

另有不可遺失的長期需求：

- **Session-independent**：Agent Session 可結束，但 Job、邏輯身分、進度、成果、授權歷史仍在；新 Session 可恢復工作。
- **Multi-Repo**：跨多個 Git Repository 的依賴與交付；Worktree 隔離；平行工作與中斷恢復。
- **可重複用的工作知識**：成功方法和失敗教訓被存成 Playbook 的可控版本，不依賴某次聊天上下文。
- **自動化但有授權邊界**：AI 可提出立項、工作計畫與部署意見；產生決定的文字本身不等於執行權。依預先設定的政策可自動核准低風險範圍，但資源使用、寫入和發布需要可信程式 Gate。
- **品質與成本**：以實際成功率、證據品質、延遲與帳單衡量，不把「Agent 數量少」或「CLI 輸出縮短」誤認為整體效率提升。

## 2. 此次架構討論的決策紀錄（以此為準）

### D-01：推倒重做，採用 Playbook-first（已確定）

舊方向：`部門 → Role → Agent → Skill → Workflow`。

新方向：`目標／事件 → Workflow → Playbook → 執行 → Proof → 改善`。

- 57 個 Role 是前一版為了專業分工整理出的職務配置，**不再是設計起點**。
- 可以將它們的專業知識、工作方法、檢查表與模板拆解成 Skills／References／Playbooks；**不用一 Role 對一個 Agent Runtime**。
- Agent 實例數量是**執行時的選擇結果**，不是設計時的固定參數。
- 舊「27 塊積木」的邏輯功能可以重新組合或捨棄，**不要延續編號 B00–B26 作為新架構的強制 API**。

### D-02：Playbook 與 Workflow 嚴格分離（**使用者剛明確選擇 B；已確定**）

**已選方案 B**：

- **Playbook**：只描述一個可獨立驗收工作成果的工作方法。包含 Input／Interview／Procedure／Toolbox／Output／Proof／Failure／Improvement 等。
- **Workflow Engine**：唯一負責 Playbook 之間的組合、依賴、派工、循環與狀態管理的控制平面。
- **Playbook 不可直接呼叫、啟動或隱含展開另一份 Playbook。**
- 如果某 Playbook 發現需要額外工作，可以回傳**結構化的 `next_work_proposals`／`work_request`**；由 Workflow Engine 在依賴、Scope、預算與 Authority 檢查後決定是否安排。**提議不是派工。**
- Playbook 可以在自己流程內使用 Script、工具、References、Skills；但不應透過「工具」繞過跨 Playbook 的管制。所有會造成額外 Job 的操作都必須由 Engine 記帳。

未決：`next_work_proposals` 是否是最終標準輸出欄位、動態分支／迴圈如何表達、如何限制展開深度。**這些是待設計，不是已確定的 Schema**。

### D-03：不以 57 個固定 Agent Persona 進行專業分工（方向已確定）

優先採用**通用 Executor**，依 Job 需求載入不同 Playbook、Skills、工具及限制。

只有在以下理由成立時才建立新 Agent Session：

1. 必須有獨立的審查上下文（開發者不可自我獨立認證）。
2. 不同權限或信任層級必須隔離。
3. 可以真正並行且收益抵過交接／上下文成本。
4. 能證明專門的執行環境較適合。

過去討論曾將 Executor／Reviewer／Optimizer 當成三種**執行型態**；它們**不是**確定需要三個常駐 Agent 或三類固定 Persona。

### D-04：保留四種不可混淆的核心能力（原則已確定）

| 核心能力 | 真正負責 | 不應負責 |
|---|---|---|
| **Playbook** | 如何執行一項工作及產出什麼 | 自行授權、跨 Playbook 派工 |
| **Proof** | 完成標準、證據與驗證規則 | 將 Agent 的 `PASS` 字串當作證明 |
| **Durable Execution** | Job／Attempt／Checkpoint／Artifact／Repo 狀態跨 Session 保存與恢復 | 將聊天視為唯一真相來源 |
| **Authority** | 決定何種動作可用、何時能提交或部署 | 依 Agent Persona／Playbook 文字宣告授權 |

另有非 LLM **Workflow Engine** 串接以上能力。這是**邏輯分層**，不是強制拆成四五個微服務。

### D-05：全域 P00 Grounded Answer Policy（原則已確定）

- 回答要有根據、符合現實，避免討好與自信但無證據的敘述。
- 不刻意唱反調；支持與反對都需依證據。
- 標示必要的 `FACT`、`INFERENCE`、`ASSUMPTION`、`UNKNOWN`；證據不足不得假裝已驗證。
- 對重要決策保留來源／測試／SHA 等可追溯證據；不應用形式上的引用或信心分數取代查核。
- P00 是**全域規範**，不是第 N 個職務或按需啟用的可選 Skill；新 Session 需載入已釘選版本。
- 提示詞無法單獨形成強制保證；正式系統必須由 Runtime、Schema Gate 和外部權限機制落實可檢查部分。

### D-06：不允許不受控的「Fix the Playbook」（已確定的設計原則）

- **修正當次成果**與**修改共用 Playbook**是不同層次的工作、不同權限。
- 遵循 `Run → Check → Failure analysis → Propose Patch → Isolated Test / Benchmark → Approve → Versioned Publish / Rollback`。
- 不只會新增檢查，也要能合併／刪除多餘步驟，避免 Playbook 無限膨脹。
- 進行中的 Job 固定 Playbook 版本；升版不能悄悄改動正在執行 Job 的契約，除非有明確受控遷移程序。

## 3. 目前對 Playbook 的工作定義（設計方向，Schema 尚未定案）

**一份 Playbook 對應一個具體且可獨立驗收的工作成果。**

例如 `market-discovery` 可產生 `OpportunityBrief`；「在 Reddit 搜尋關鍵字」通常只是其中一個 Tool／Script 步驟；「從商機到上線」則是跨 Playbook 的 Workflow，而不是一個過度巨大的 Playbook。

建議至少要描述：

| 欄位 | 目的 | 實作上的注意點 |
|---|---|---|
| `id`, `version`, `digest` | Playbook 身分及不可變版本 | Job 必須釘選完整版本／Digest |
| `input_contract` | 必需輸入、前置條件與結構 | 缺少關鍵資訊不直接啟動有副作用工作 |
| `interview` | 消除歧義、發現缺口 | **不限定訪談人類**；先查可信現有資料，必要時才請求人工決策 |
| `procedure` | 有界執行步驟及停止條件 | 不能隱藏跨 Playbook 調用 |
| `toolbox` | Skills、Scripts、Templates、References、資料來源 | **描述所需能力，不等於給予工具權限** |
| `output_contract` | 唯一可驗收成果型態 | 儘量結構化且可由其他 Workflow 重用 |
| `proof_contract` | 主張、測試／證據、成功／失敗條件 | 區分確定性、實證與獨立語意審查 |
| `failure_and_recovery` | 逾時、未知、重試、部分完成與恢復 | 避免「全部重跑」造成重複外部副作用 |
| `improvement` | 失敗記錄及改善提議 | 正式版本變更須隔離測試與審核 |

**概念範例（非正式 Schema）**：

```yaml
id: market-discovery
version: 1.0.0
input_contract: opportunity_search_scope.schema.json
interview:
  - detect_missing_context
  - resolve_from_trusted_artifacts
  - request_decision_if_blocking
procedure:
  - collect_real_world_signals
  - deduplicate_source_origins
  - cluster_problem_patterns
  - analyze_disconfirming_evidence
toolbox:
  skills: [product-research, market-research]
  tools: [web_search, structured_extraction]
output_contract: opportunity_brief.schema.json
proof_contract:
  - source_provenance_verifiable
  - assumptions_and_unknowns_explicit
  - same_root_source_not_counted_as_independent_evidence
failure_and_recovery:
  - insufficient_evidence_returns_unknown
  - persist_checkpoints
improvement:
  - propose_revision_only
```

**此範例中的工具與 Skill 名稱僅示意可用類型，不保證已完成安裝或執行。**

## 4. Proof：不是自我勾選 Checklist（重要）

三種驗證要分清楚：

1. **Deterministic Verification**：計算、格式、Schema、測試、CI、簽章、Commit SHA、一致性規則等。由程式實測，不由 LLM 宣稱。
2. **Empirical Evidence**：外部來源、實驗、真實使用者資料等。要求可追溯來源、原始脈絡、來源獨立性、時效與限制；可證明的結論不得超出證據範圍。
3. **Independent Semantic Review**：設計、因果、商業價值、需求解讀與風險等需獨立上下文和清楚的審議範圍。Reviewer 提供判斷，不是不可質疑的真理來源。

例如「論壇有人抱怨某功能」不代表「存在足夠願付費的市場」。**有需求訊號 ≠ 可證實商機**。

Proof Artifact 應綁定 Job、Attempt、輸出 Artifact、必要時綁定 Repo/Commit SHA、執行時間、驗證程序、證據來源與版本。`PASS` 只能在定義的驗收範圍內成立。

## 5. Durable Execution：不可丟掉的工程不變條件

**Job 存在於 Session 之外；Session 是可替換的執行載體。**

- Job／Workflow／Playbook 版本、事件、Checkpoint、Artifact References、依賴、審查結果與授權狀態要寫入外部持久化來源；不依賴舊聊天記憶。
- 區分 `workflow_id`, `job_id`, `attempt_id`, `session_id`, `logical_executor_id`、Repo 身分與授權憑證。
- 每次重試有新 Attempt 與 Fencing Generation；**晚到的舊 Attempt 不能覆蓋新結果**。
- Session 中斷後**不是還原模型隱藏推理**，而是根據結構化的工作包（要求、已完成步驟、Checkpoint、證據、Artifact、下一步）啟動新 Session。
- 偵測 Worker 逾時不能馬上刪 Worktree 或派出另一個可寫入 Worker；先撤銷有效寫入權、終止程序樹並確認退出；若無法確認則隔離待處理。
- 跨多 Repo 可以有 Job DAG、獨立 Workspace、固定 base/commit SHA；在多 Repo 交付情境需處理部分成功與補償／對帳，不要假設跨 Git Repo 具備原子交易。
- 外部副作用（Push、MR、Deploy、寄信、付費）需要冪等鍵、查詢／對帳或其他重複執行防護。例如 MR 已建立但 Worker 回覆前掛掉，新 Session 不應盲目再建第二個。
- Fencing 在 DB 通過**不等於**外部 API 被限制；GitLab／Cloud 寫入必須透過真正受控的權限路徑，不能讓舊 Worker 持有永久 Token。

舊附件使用 SQLite 與測試作為參考；**正式資料庫／程式語言／Queue／Runner／Repo Provider 等尚未在新架構重新決定**。不應因為舊版寫 PostgreSQL／GitLab 就無條件將其設為新版的不可變硬需求；但使用者確實希望 Git 工作流、跨 Repo 與 MR 能被整合。

## 6. Authority：AI 提案與可信授權分離

- Agent、Council、Playbook、文件內容都可**提出**決策／工作建議，但不能因文字上寫 `APPROVE` 就取得執行權。
- 非 LLM Policy/Issuer 根據使用者預先設定的政策、Scope、Repo、路徑、預算、風險、時間及 Proof 決定是否允許**具副作用的動作**。
- **自主性不等於每次問人類**：低風險可在預授權範圍內自動進行，超出界限才阻塞／請求批准。
- Scope 確定性部分（ID、路徑、Repo、額度等）由程式檢查；是否語意偏離原需求仍需獨立審查。
- 最小權限、短效 Token、審核可追溯、禁止跨 Job 偷帶權限、敏感資料隔離仍成立。
- 對 P00 或 Authority 有衝突的 Skill／Playbook 指令不得越權。

## 7. Workflow Engine 組合 B 方案（已選）

### Workflow 是組裝描述，不是 Agent Persona

建議將 Workflow 定義為 DAG／狀態機／有界控制流，把 Playbook 當作節點：

```yaml
workflow: venture-discovery-to-mr
version: draft
nodes:
  - id: discover
    playbook: market-discovery@1.0.0
  - id: evaluate
    playbook: opportunity-evaluation@1.0.0
    needs: [discover]
  - id: decision
    kind: authority_gate
    needs: [evaluate]
  - id: specify
    playbook: product-specification@1.0.0
    needs: [decision]
  - id: implement
    playbook: implement-feature@1.0.0
    needs: [specify]
  - id: verify
    playbook: independent-qa@1.0.0
    needs: [implement]
  - id: publish_mr
    kind: controlled_action
    needs: [verify]
```

**此 YAML 只是討論例子，並非正式 DSL；完整版還需要決定部署、營運與成效追蹤節點。**

核心執行規則：

1. Workflow Engine 是**唯一**能建立／啟動跨 Playbook Job 的元件。
2. Playbook 給出明確的輸入與輸出 Artifact／狀態，不負責其下游節點的生命週期。
3. AI 可以提出 Workflow／Plan 調整，但 Engine 必須依 Scope、風險、預算、依賴及權限政策驗證，才可實施。
4. 容許條件分支、有限重試與後續工作提案；禁止未受控的遞迴展開、無界迴圈與隱藏調度。
5. 製作成果的 Executor 不能僅依自我檢查通過獨立驗收；Proof Gate 要取得外部證據或另一個獨立 Session 的檢查結果。
6. 一份 Playbook 被多條 Workflow 共用時，只需維護一份經過版本治理的工作方法。

### 可以分段使用的組合

- `market-discovery → opportunity-evaluation`：只研究商機。
- `product-specification → implement-feature → independent-qa → publish_mr`：從已批准需求直接執行工程。
- `independent-qa`：獨立評估既有程式／成果。
- `tool-evaluation → benchmark → adoption-gate`：改善平台的 Skill／Toolbox。
- `report-production → proof-validation`：用於報告型任務，不需額外產生專用 Report Agent。

## 8. 執行策略：不要把縮減 Agent 當唯一 KPI

建議分派優先序：

`確定性程式 / Script → 既有 Executor 載入 Playbook + Skill → 必要時新 Session → 多 Session 平行／獨立審查`

至少追蹤：完成品質、Proof 有效率、錯誤及返工、端到端延遲、實際 Token/API 費用、Session 冷啟動成本、交接重建成本、Recovery 成功率、重複外部操作與安全事件。

長期需要做受控對照：相同工作使用一個 Executor 連續載入 Playbook，與多個獨立 Worker 分段委派，哪個可靠且具成本效益？**這是待測假設，不是已證實答案。**

## 9. 既有 Repo／方法論：參考用途，不是新架構的固定依賴

| 來源 | 可吸收的能力 | 不應誤解 |
|---|---|---|
| [Anthropic Agent Skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills) | 可載入工作知識／腳本／資源的概念 | Skill 自動等於完整可驗證 Playbook |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Spec、Tickets、Implement、TDD、Review、Handoff | 其 Skill 本身提供商業授權；`implement-spec` 無副作用地只是文字方法 |
| [MarkBovee/agent-skills-kit](https://github.com/MarkBovee/agent-skills-kit) | Agent 工作分配、風險分層、Proof、報告控制與成本管理 | 同時啟用與 Matt 競爭的完整流程 Router |
| [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | 專業知識與職責／驗收知識素材 | 必須常駐數十個 Agent Persona |
| [0xNyk/council-of-high-intelligence](https://github.com/0xNyk/council-of-high-intelligence) | 必要時多視角獨立論證／反駁 | Council 自動取得正式批准權 |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | 最小完整實作、重用、減少不必要抽象 | A2A 通訊或 Proof 的全部保障 |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | 減少 CLI 雜訊／降低工具輸出 | 命令輸出減少比例等於帳單節省比例 |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 產品、研究、營運、Skill 安全與改善候選能力 | Skill 未經審查即可以改動正式環境 |

**注意**：原本曾談到「Matt 決策」，那是使用者在舊版設計的自訂商業決策關卡，**不是** `mattpocock/skills` 的內建立項批准器。新架構是否仍需要該角色名稱完全**未定**；原則只保留「LLM 提案 ≠ 可信授權」。

## 10. 尚未定案、適合下一個 Codex Session 討論的問題

**第一優先：Playbook 與 Workflow 的邊界、最小契約**

1. Playbook 最小合理粒度是「單一可驗收成果」嗎？如何防止過度拆分？何時 Script/Skill 比 Playbook 更合適？
2. `Interview` 是內部資料補足、釐清問題，還是獨立可重用的需求澄清流程？何時必須等人類輸入？
3. B 方案下的動態新工作：`work_request` 的資料結構、Engine 何時接受／拒絕，以及防止無限展開的預算與深度限制。
4. Workflow 可否包含直接的 Script／Gate 節點？或者所有動作都必須包成 Playbook？（目前傾向讓確定性工作直接執行，**尚未決策**。）
5. Playbook 是否可以包含子步驟或小型狀態機？與「不能直接呼叫另一份 Playbook」的界線要如何定義？
6. `Proof Contract` 如何定義各類工作所需最小證據、無法驗證時的狀態、與独立審查觸發條件？
7. 新舊 Playbook 版本、回歸測試資料、版本相容性與執行中 Job 的升級規則。

**第二優先：執行控制、權限與持久化**

8. Job／Attempt／Session／Workflow／Artifact／Evidence 的最小持久化資料契約，與 Engine 的狀態機。
9. 如何做真正的外部副作用冪等、過期 Worker 寫入隔離、Process termination attestation 與 Recovery 對帳。
10. Playbook 提議需要新工具／新權限時，誰能授權、哪些風險可預先授權？
11. 多 Repo 的分支／Commit／MR 證據與交易非原子情境如何表達？

**第三優先：能力改善與效益測量**

12. 何種失敗應修當次 Job、何種失敗值得更新 Playbook；改善何時可自動上線？
13. 如何防止共用 Playbook 越改越冗長、互相矛盾，並且有可回滾的 Benchmark？
14. 如何量測單一 Executor、多 Executor 與 Script-only 的成本／品質，在何種情況才值得並行？

以上是設計題，不需一次決定全部；**先從第 1～5 題最關鍵的架構邊界討論起**。

## 11. 如何判斷 Codex 是否正確接手

新 Session 應能先準確復述下面六項，而不是重新把話題拉回原版組織圖：

- 使用者要的是**可組裝的自主 AI 工作系統**，自主產品公司只是整體 Workflow 的一種組裝方式。
- **Playbook-first**，不是「一個任務／一個專業就生成一個 Agent」。
- **B 方案已確定：Playbook 不直接呼叫另一份 Playbook；Workflow Engine 唯一負責組裝與派工。**
- **Proof 必須真的可驗證**；P00 禁止用無證據的自信回覆取代事實。
- **Session 可以消失，工作不能消失**；需具備跨 Repo、Attempt/Fence、恢復與外部副作用安全處理。
- **現在還在設計討論**，可推倒重做舊文件，不要擅自轉成實作或虛構已驗證能力。

## 12. 建議給 Codex 的第一則訊息（可直接複製）

> 請先完整閱讀我附上的 `CODEX_HANDOFF_PLAYBOOK_ARCHITECTURE.md`。這是新一輪架構討論，不是要你實作，也不必沿用舊版 57 個 Role／27 個模組。我已選擇**方案 B：Playbook 不直接呼叫其他 Playbook，只有 Workflow Engine 能組合、派工及管理依賴**。請以此為不可忽略的已決策前提，先批判性地檢驗「一份 Playbook 對應一個可獨立驗收成果」這個最小單位是否合理，討論 Skill、Script、Playbook、Workflow 的確切邊界、可能反例及設計取捨。不要先寫規格或程式；務必保留 Proof、Durable Execution、Authority 與 P00，並區分已決策與待決策事項。

---

### 相關舊文件（有提供時再參考，不是必需附件）

- `AGENT_ROLE_SKILL_FLOW.md`：前一版角色分工、技能來源、工程鏈。
- `LEGO_WORKFLOWS_P00.md`：舊版 27 塊模組工作流及其合約概念。
- `DURABLE_AGENT_RUNTIME.md`：跨 Session／Repo、Attempt/Fence／Checkpoint 的舊版設計及參考契約。
- `P00_GROUNDED_ANSWER_POLICY.md`：已討論過的全域實證回答規範。
- `agent-lego-grounded-v03.zip`：舊版參考規格與樣例程式；**不是新架構的正式實作基線**。

> 如新 Codex Session 沒有這些舊檔案，只讀**本 Handoff**也應足以開始設計討論；不要宣稱自己已讀到未提供的文件。
