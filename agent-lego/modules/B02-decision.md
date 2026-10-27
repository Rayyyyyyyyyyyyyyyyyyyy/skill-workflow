# B02 — decision

- **階段**：M0
- **唯一 Owner**：DECISION.matt（自訂決策角色）
- **方法／Skills**：自訂 Decision Policy；不等於 mattpocock/skills
- **輸入**：EvaluationPacket；M2 再加 CouncilVerdict
- **輸出**：DecisionRecord（APPROVE / REJECT + reason_code）
- **允許權限／邊界**：只有商業建議權；無 Repo/發憑證權
- **上游依賴**：B01
- **獨立驗收案例**：未明確 APPROVE、逾時、格式錯誤一律不放行且保留原因碼

## 行為契約

拍板但不簽發執行權。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。

## P00 全域政策掛載（v0.3）

- 本積木遵守 [`P00 Grounded Answer Policy`](../policies/P00-GROUNDED-ANSWER.md)，不得由局部 Role/Skill 覆蓋。
- 涉及實際觀測、技術驗收、事實判斷或重大決策時，綁定 `policy_ref`、保存來源 refs 和未知限制；需要時生成 [`ClaimEvidence`](../contracts/claim-evidence.schema.json)。
- Matt 是決策提案角色；不能用語言輸出取代 B03 的非 LLM Issuer 授權。
