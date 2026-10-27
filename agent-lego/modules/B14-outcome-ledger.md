# B14 — outcome-ledger

- **階段**：M2
- **唯一 Owner**：OUTCOME.evaluator（Product Manager + Analytics Reporter）
- **方法／Skills**：ClaudeLib product-discovery + saas-metrics-coach（SaaS 時）
- **輸入**：原 DecisionRecord、收款、使用行為、實驗結果
- **輸出**：OutcomeRecord
- **允許權限／邊界**：只能附加結果，不可修改當初決策
- **上游依賴**：B13
- **獨立驗收案例**：結果有時間窗、樣本數與來源；拒絕案要標反事實未知

## 行為契約

市場回饋供下一輪評估；尚不構成模型訓練資料。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
