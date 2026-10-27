# B24 Multi-Repo Coordinator

- **階段**：M1
- **唯一 Owner**：非 LLM DAG Controller
- **輸入**：ApprovedBrief 與跨 Repo Ticket Dependency
- **輸出**：每 Repo Job / DAG + Cohort SHA Manifest
- **禁止事項／權限邊界**：不能跳過 B06 派工；不能宣稱 Git Multi Repo 原子交易
- **依賴**：B22 / B06 / B09
- **驗收**：兩 Repo、平行與依賴測試；QA 沒通過不能解鎖下游；SHA 漂移 BLOCK

## 行為契約

此積木只能透過 `contracts/` 已版本化 JSON、持久交易與 Artifact refs 交接；A2A v2 沿用 `job_id / attempt_id / fence_generation`。詳細故障策略見 [`../DURABLE_AGENT_RUNTIME.md`](../DURABLE_AGENT_RUNTIME.md)。

## 開發要求

先用 Stub 驗證輸入拒絕與輸出結構，再介接真實 Postgres、GitLab、Worker Supervisor。SQLite 參考測試不構成生產級權限或程序隔離證明。
