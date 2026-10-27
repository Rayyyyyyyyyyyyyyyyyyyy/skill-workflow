# B22 Durable State Store

- **階段**：M0
- **唯一 Owner**：非 LLM State API
- **輸入**：已驗證 ApprovedBrief、Job、Agent Registry 設定、事件
- **輸出**：交易化 Job/Attempt/Session/Event + Checkpoint 索引
- **禁止事項／權限邊界**：PostgreSQL Transaction、事件 Outbox；不得直接作商業決策
- **依賴**：B03 / B07
- **驗收**：重啟仍查得任務與事件；多 Worker 原子 Claim；API 權限驗證

## 行為契約

此積木只能透過 `contracts/` 已版本化 JSON、持久交易與 Artifact refs 交接；A2A v2 沿用 `job_id / attempt_id / fence_generation`。詳細故障策略見 [`../DURABLE_AGENT_RUNTIME.md`](../DURABLE_AGENT_RUNTIME.md)。

## 開發要求

先用 Stub 驗證輸入拒絕與輸出結構，再介接真實 Postgres、GitLab、Worker Supervisor。SQLite 參考測試不構成生產級權限或程序隔離證明。
