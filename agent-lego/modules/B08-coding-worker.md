# B08 — coding-worker

- **階段**：M0
- **唯一 Owner**：ENG.worker（Agency Frontend/Backend 等按需）
- **方法／Skills**：Matt tdd + Ponytail + A2A v2 + RTK（可選）
- **輸入**：TASK v2 + 最小 Scope/Ticket refs + 隔離 Worktree
- **輸出**：RESULT v2 + commit SHA + Test Evidence
- **允許權限／邊界**：只可修改短效授權隔離 Worktree；無 merge/deploy 權
- **上游依賴**：B07
- **獨立驗收案例**：有可測邏輯時 Red-Green-Refactor；DONE 必須有產物且有驗證

## 行為契約

一名 Worker 一個有界 Ticket；測試原始 Log 保存在 Artifact。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
