# B10 — qa-coordinator

- **階段**：M0
- **唯一 Owner**：QA.coordinator + QA.standard + QA.spec（責任人）
- **方法／Skills**：M0 僅 QA.coordinator 調用一次 Matt code-review
- **輸入**：固定 Diff SHA、ApprovedBrief、Spec、驗證結果
- **輸出**：Standards/Spec Review Evidence；缺陷 refs
- **允許權限／邊界**：唯讀審查，不能更改 Source；雙軸審查證據
- **上游依賴**：B08
- **獨立驗收案例**：同一 Skill 不得由 QA.standard/QA.spec 重複完整呼叫；修改後證據須重驗

## 行為契約

M1 若 ENG.foreman 全權執行 implement-spec，則只驗其內部 Review receipts，不再啟動重複 Review。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。

## P00 全域政策掛載（v0.3）

- 本積木遵守 [`P00 Grounded Answer Policy`](../policies/P00-GROUNDED-ANSWER.md)，不得由局部 Role/Skill 覆蓋。
- 涉及實際觀測、技術驗收、事實判斷或重大決策時，綁定 `policy_ref`、保存來源 refs 和未知限制；需要時生成 [`ClaimEvidence`](../contracts/claim-evidence.schema.json)。
- 「QA PASS」必須綁定固定 SHA 與測試事實；不得靠 Agent 自述取得驗收。
