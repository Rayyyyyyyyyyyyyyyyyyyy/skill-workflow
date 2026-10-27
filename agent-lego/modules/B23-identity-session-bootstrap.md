# B23 Identity & Session Bootstrap

- **階段**：M0
- **唯一 Owner**：非 LLM Bootstrap Controller
- **輸入**：Agent ID、Role/Profile SHA、Scope 與新 Attempt、持久 Checkpoint
- **輸出**：新 Session 建立封包，載入最小可信上下文
- **禁止事項／權限邊界**：不得用舊聊天推斷授權；不得復用舊 session_id 或 attempt_id
- **依賴**：B22 / B03 / B07
- **驗收**：同 Agent 跨 Session 可接續；失效授權與無效 Artifact BLOCK

## 行為契約

此積木只能透過 `contracts/` 已版本化 JSON、持久交易與 Artifact refs 交接；A2A v2 沿用 `job_id / attempt_id / fence_generation`。詳細故障策略見 [`../DURABLE_AGENT_RUNTIME.md`](../DURABLE_AGENT_RUNTIME.md)。

## 開發要求

先用 Stub 驗證輸入拒絕與輸出結構，再介接真實 Postgres、GitLab、Worker Supervisor。SQLite 參考測試不構成生產級權限或程序隔離證明。

## P00 全域政策掛載（v0.3）

- 本積木遵守 [`P00 Grounded Answer Policy`](../policies/P00-GROUNDED-ANSWER.md)，不得由局部 Role/Skill 覆蓋。
- 涉及實際觀測、技術驗收、事實判斷或重大決策時，綁定 `policy_ref`、保存來源 refs 和未知限制；需要時生成 [`ClaimEvidence`](../contracts/claim-evidence.schema.json)。
- Session 重啟必須從持久化 Job 載入釘選版本與 digest，載入失敗不得執行需要證據的 Gate。
