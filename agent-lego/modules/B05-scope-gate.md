# B05 — scope-gate

- **階段**：M0
- **唯一 Owner**：SCOPE.validator（非 LLM） + QA.scope（獨立語意審查）
- **方法／Skills**：Scope hard checks + 獨立 Spec review
- **輸入**：ApprovedBrief、Spec、Ticket/Job、變更檔案
- **輸出**：硬限制 verdict + SemanticReviewRef
- **允許權限／邊界**：只有 ALLOW / BLOCK；不擴大範圍
- **上游依賴**：B03,B04
- **獨立驗收案例**：ID、Repo、路徑、額度硬檢查；同路徑偷加功能仍需獨立語意審查

## 行為契約

把機械可判斷與語意判斷分開，任何一側缺失都不能當 PASS。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
