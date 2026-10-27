# B25 Workspace Provisioner

- **階段**：M0（單 Repo）；M1（多 Repo）
- **唯一 Owner**：非 LLM Workspace Controller
- **輸入**：B07 Attempt + Repo base_sha + 限定憑證
- **輸出**：隔離 Worktree、固定 Artifact／Patch refs、退出證明
- **禁止事項／權限邊界**：未退出不得清理；舊 Attempt 不得存取同一可寫目錄
- **依賴**：B07 / Git / Artifact Store
- **驗收**：獨立 worktree、隔離環境、Kill Worker 後確認終止及安全封存

## 行為契約

此積木只能透過 `contracts/` 已版本化 JSON、持久交易與 Artifact refs 交接；A2A v2 沿用 `job_id / attempt_id / fence_generation`。詳細故障策略見 [`../DURABLE_AGENT_RUNTIME.md`](../DURABLE_AGENT_RUNTIME.md)。

## 開發要求

先用 Stub 驗證輸入拒絕與輸出結構，再介接真實 Postgres、GitLab、Worker Supervisor。SQLite 參考測試不構成生產級權限或程序隔離證明。
