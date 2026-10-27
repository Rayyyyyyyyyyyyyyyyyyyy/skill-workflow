# B17 — skill-scout

- **階段**：M3
- **唯一 Owner**：CAP.scout（Agency Tool Evaluator）
- **方法／Skills**：Matt research + ClaudeLib loop-library
- **輸入**：失敗紀錄、能力缺口、搜尋索引
- **輸出**：SkillCandidate（來源 URL + commit）
- **允許權限／邊界**：唯讀候選；無安裝權
- **上游依賴**：無
- **獨立驗收案例**：找得到釘選來源且證明解決的問題，不接受無出處推薦

## 行為契約

能力線獨立於產品線。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
