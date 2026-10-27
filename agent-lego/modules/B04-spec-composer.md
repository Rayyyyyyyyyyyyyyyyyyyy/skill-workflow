# B04 — spec-composer

- **階段**：M0
- **唯一 Owner**：PRODUCT.owner（Agency Product Manager）
- **方法／Skills**：Matt to-spec；domain-modeling（有需要時）
- **輸入**：ApprovedBrief
- **輸出**：Spec artifact / requirement ID 映射
- **允許權限／邊界**：只可在核准範圍內寫 Spec；不可直接派工
- **上游依賴**：B03
- **獨立驗收案例**：每個 Spec 需求可追到原 scope_id；未知的問題停下等待決策

## 行為契約

核准問題 → 可驗收規格；背景流程不能假裝完成互動訪談。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
