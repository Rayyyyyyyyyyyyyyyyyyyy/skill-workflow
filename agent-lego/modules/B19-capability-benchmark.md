# B19 — capability-benchmark

- **階段**：M3
- **唯一 Owner**：CAP.benchmark（Agency Tool Evaluator / Model QA）
- **方法／Skills**：ClaudeLib skill-doctor / skillopt-sleep（離線評估）
- **輸入**：SkillCandidate + Sandbox + 固定測試集
- **輸出**：BenchmarkReport（品質、成功率、延遲、成本）
- **允許權限／邊界**：只有隔離環境執行權
- **上游依賴**：B18
- **獨立驗收案例**：有 baseline、相同任務、失敗案例與可回滾產物

## 行為契約

不能只看作者宣稱的 benchmark。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
