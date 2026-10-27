# B00 — candidate-intake

- **階段**：M0
- **唯一 Owner**：DISC.intake (人工輸入；M2 改接 DISC.signal)
- **方法／Skills**：A2A v2；無需模型
- **輸入**：使用者需求 / URL / raw_refs
- **輸出**：DemandCandidate
- **允許權限／邊界**：唯讀來源、只能寫候選庫
- **上游依賴**：無
- **獨立驗收案例**：相同來源重送不產生重複候選；缺來源標 UNKNOWN

## 行為契約

保存原始文字與來源，不下結論。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
