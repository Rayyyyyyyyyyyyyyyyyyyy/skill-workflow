# B07 — attempt-manager

- **階段**：M0
- **唯一 Owner**：ORCH.attempt（非 LLM 控制程式）
- **方法／Skills**：Job/Attempt Schema + A2A v2
- **輸入**：Job、短效工具憑證、Worker
- **輸出**：Attempt / Lease / Fence Generation
- **允許權限／邊界**：控制 CAS、取消、撤權、工作區清理
- **上游依賴**：B06
- **獨立驗收案例**：重試後舊結果無效；未退出程序不得清理 Worktree

## 行為契約

每次執行 attempt_id + 單調遞增 fence；禁止舊結果冒充新結果。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
