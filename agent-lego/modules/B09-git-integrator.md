# B09 — git-integrator

- **階段**：M1
- **唯一 Owner**：ENG.git（Agency Git Workflow Master）
- **方法／Skills**：Git 命令 + Matt pr（MR 內文）；**不載入 implement-spec**
- **輸入**：已驗收 Commit refs／衝突策略
- **輸出**：固定 Integration SHA / Branch
- **允許權限／邊界**：只執行工頭派發的整合命令；無擴權
- **上游依賴**：B08
- **獨立驗收案例**：衝突停止並回報；不可 force-push／擅自更換已驗收 SHA

## 行為契約

多 Worker 才需要獨立整合積木；M0 直接用 Worker 固定 SHA。模組只能透過產物引用／明確事件與其他模組協作；詳細報告寫入 Artifact Store，A2A 訊息僅傳 refs、attempt 與執行狀態。

## 測試方法

使用 `examples/` 的合法樣本或 Stub 上游事件，加入至少一筆違規樣本。無須啟動其他部門即可驗證輸入、輸出、拒絕條件；全流程整合另於 M0 進行。
