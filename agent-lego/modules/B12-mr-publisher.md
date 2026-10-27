# B12 — mr-publisher

- **階段**：M0
- **唯一 Owner**：ENG.git（有界 MR 發布職務）
- **方法／Skills**：Matt pr + GitLab API
- **輸入**：Evidence PASS、固定 SHA、核准 Repo
- **輸出**：MR ref + 發布收據
- **允許權限／邊界**：只建 MR；預設不得 Merge 到保護分支
- **上游依賴**：B11
- **獨立驗收案例**：MR 對準已驗收 SHA；沒有證據不能發布 MR

## 行為契約

M0 到 MR 為止，不直接部署。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
