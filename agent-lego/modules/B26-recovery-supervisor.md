# B26 Recovery Supervisor

- **階段**：M0
- **唯一 Owner**：非 LLM Reconciler
- **輸入**：B22 Jobs / Lease / Heartbeat / Session 記錄
- **輸出**：失聯事件、QUARANTINE/RETRY 請求、復原審計紀錄
- **禁止事項／權限邊界**：只偵測並呼叫 B07，不能簽發 Attempt，也不能自行宣稱已退出
- **依賴**：B22 / B07 / B25
- **驗收**：Controller 重啟掃描；逾時舊結果失效；未確認退出不重派

## 行為契約

此積木只能透過 `contracts/` 已版本化 JSON、持久交易與 Artifact refs 交接；A2A v2 沿用 `job_id / attempt_id / fence_generation`。詳細故障策略見 [`../DURABLE_AGENT_RUNTIME.md`](../DURABLE_AGENT_RUNTIME.md)。

## 開發要求

先用 Stub 驗證輸入拒絕與輸出結構，再介接真實 Postgres、GitLab、Worker Supervisor。SQLite 參考測試不構成生產級權限或程序隔離證明。
