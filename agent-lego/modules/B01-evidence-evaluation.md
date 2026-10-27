# B01 — evidence-evaluation

- **階段**：M0
- **唯一 Owner**：EVAL.product；按需 EVAL.market／technical
- **方法／Skills**：AGENCY Product Manager + ClaudeLib product-discovery
- **輸入**：DemandCandidate
- **輸出**：EvaluationPacket（事實／推論／假設／未知＋refs）
- **允許權限／邊界**：唯讀；不得建工程 Ticket
- **上游依賴**：B00
- **獨立驗收案例**：無外部證據時不能輸出 FACT；不得把 Agent 多數同意當市場證據

## 行為契約

限定本次要驗證的需求，不把可行性報告當立項授權。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。

## P00 全域政策掛載（v0.3）

- 本積木遵守 [`P00 Grounded Answer Policy`](../policies/P00-GROUNDED-ANSWER.md)，不得由局部 Role/Skill 覆蓋。
- 涉及實際觀測、技術驗收、事實判斷或重大決策時，綁定 `policy_ref`、保存來源 refs 和未知限制；需要時生成 [`ClaimEvidence`](../contracts/claim-evidence.schema.json)。
