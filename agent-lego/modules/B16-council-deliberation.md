# B16 — council-deliberation

- **階段**：M2
- **唯一 Owner**：COUNCIL.review（專用審議職務）
- **方法／Skills**：council-of-high-intelligence
- **輸入**：EvaluationPacket
- **輸出**：CouncilVerdict（異議、kill criteria）
- **允許權限／邊界**：只能提議和保留異議
- **上游依賴**：B01
- **獨立驗收案例**：不會以投票結果直接核發 ApprovedBrief；與評估資料交叉驗證

## 行為契約

插在 B01 與 B02 之間，B02 的輸入擴充但權限不變。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
