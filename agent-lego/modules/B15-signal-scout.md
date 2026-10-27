# B15 — signal-scout

- **階段**：M2
- **唯一 Owner**：DISC.signal（Agency Trend Researcher）
- **方法／Skills**：ClaudeLib market-research + product-research
- **輸入**：授權的公開來源／排程
- **輸出**：DemandCandidate + source refs
- **允許權限／邊界**：只讀取准許來源；避免未授權擷取個資
- **上游依賴**：無
- **獨立驗收案例**：同一來源幂等、保留時間戳、按平台限制存取

## 行為契約

取代 B00 手動供給，但維持 B00 的輸入契約。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
