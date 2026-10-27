# B11 — evidence-gate

- **階段**：M0
- **唯一 Owner**：QA.evidence（Agency Evidence Collector） + REL.policy（非 LLM）
- **方法／Skills**：Evidence Manifest Schema、CI 來源核對
- **輸入**：ApprovedBrief、Job、Attempt、固定 SHA、QA/CI 結果
- **輸出**：EvidenceManifest + PASS/BLOCK
- **允許權限／邊界**：可信驗收判定；無 Source 寫入權
- **上游依賴**：B07,B10
- **獨立驗收案例**：缺 Spec/Standards/語意審查或 SHA 不一致必須 BLOCK

## 行為契約

Evidence 只描述既有且可查的測試報告；不是宣告式 PASS。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。

## P00 全域政策掛載（v0.3）

- 本積木遵守 [`P00 Grounded Answer Policy`](../policies/P00-GROUNDED-ANSWER.md)，不得由局部 Role/Skill 覆蓋。
- 涉及實際觀測、技術驗收、事實判斷或重大決策時，綁定 `policy_ref`、保存來源 refs 和未知限制；需要時生成 [`ClaimEvidence`](../contracts/claim-evidence.schema.json)。
- 透過可信 Artifact Registry 核對 Evidence refs；Schema PASS 不等於語意正確，獨立驗證不可省略。
