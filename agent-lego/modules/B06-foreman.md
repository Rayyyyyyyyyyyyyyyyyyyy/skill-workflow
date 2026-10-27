# B06 — foreman

- **階段**：M0
- **唯一 Owner**：ENG.foreman（Agency Agents Orchestrator）
- **方法／Skills**：ASK agent-workflows（規則）；Matt to-tickets（單票）；M1 可選 implement-spec
- **輸入**：ApprovedSpec + Scope Gate PASS
- **輸出**：Job + 分派決議
- **允許權限／邊界**：只能派 Ready 的已核准 Job，對預算與模型路由負責
- **上游依賴**：B05
- **獨立驗收案例**：沒 ApprovedBrief 不派工；同工種不得重複啟動兩個生命週期主控

## 行為契約

M0 只有一張 Ticket、一名 Worker；DAG 並行留到 M1。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
