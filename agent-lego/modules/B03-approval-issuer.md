# B03 — approval-issuer

- **階段**：M0
- **唯一 Owner**：AUTH.issuer（非 LLM 程式）
- **方法／Skills**：Approved Brief Schema + Policy Validator
- **輸入**：DecisionRecord、scope_ids、acceptance_ids、repo、預算
- **輸出**：ApprovedBrief 或 DENY
- **允許權限／邊界**：唯一授權簽發權；不編輯 DecisionRecord
- **上游依賴**：B02
- **獨立驗收案例**：假批准、逾期、修改預算後原憑證不再有效

## 行為契約

可信資料庫或簽章綁定完整 Brief；Prompt APPROVE 不構成授權。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
