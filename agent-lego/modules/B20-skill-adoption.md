# B20 — skill-adoption

- **階段**：M3
- **唯一 Owner**：CAP.adoption（非 LLM 控制程式）
- **方法／Skills**：版本化 Registry、Adoption Policy
- **輸入**：安全結果、Benchmark、License、Rollback
- **輸出**：ADOPT/REJECT + pinned version
- **允許權限／邊界**：唯一 Skill Registry 發布權
- **上游依賴**：B19
- **獨立驗收案例**：不得自動繞過成本上限／授權／回滾計畫

## 行為契約

任何更新不修改商業決策及正在執行的 Job。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
