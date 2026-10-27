# B13 — release-controller

- **階段**：M2
- **唯一 Owner**：REL.controller（非 LLM） + REL.devops
- **方法／Skills**：ClaudeLib ship-gate（檢查訊號） + GitLab CI
- **輸入**：MR、QA Manifest、發布策略及授權
- **輸出**：Release/Denied receipt
- **允許權限／邊界**：正式部署權只由可信 Controller 發出
- **上游依賴**：B12
- **獨立驗收案例**：CI/QA/安全權限缺一即停；緊急權限另外界定

## 行為契約

把上線當獨立操作，不由開發者順手做。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
