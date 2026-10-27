# B21 — finops-telemetry

- **階段**：M1
- **唯一 Owner**：FINOPS.cost（Agency FinOps Engineer）
- **方法／Skills**：RTK gain + Provider Billing + Job 事件
- **輸入**：Token、模型、重試、工時計量、CLI 估算
- **輸出**：CostReport + Budget Alert
- **允許權限／邊界**：只能統計與阻擋超額；不能自行提額
- **上游依賴**：B07
- **獨立驗收案例**：Token 估算 ≠ 帳單；每 Job 有實際供應商用量紀錄

## 行為契約

作為跨部門旁路，預設不在主流程增加 LLM 步驟。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
