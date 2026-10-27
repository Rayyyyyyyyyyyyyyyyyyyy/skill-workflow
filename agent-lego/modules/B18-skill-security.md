# B18 — skill-security

- **階段**：M3
- **唯一 Owner**：CAP.security（Agency Security Architect）
- **方法／Skills**：ClaudeLib skill-security-auditor
- **輸入**：SkillCandidate 釘選原始碼
- **輸出**：SecurityFindings
- **允許權限／邊界**：無正式安裝／Registry 寫入權
- **上游依賴**：B17
- **獨立驗收案例**：危險腳本、網路呼叫、授權風險逐項驗證

## 行為契約

安全掃描只是必要條件，非充分保證。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
