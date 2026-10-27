# Skill Workflow

以 Playbook 為核心的 AI 工作流架構設計。跨 Playbook 派工、正式狀態、驗收及授權由非 LLM Engine 控制。

目前新版仍為設計規格，尚未實作或通過 Runtime 驗收。

## 閱讀入口

1. [架構建議稿](PLAYBOOK_MVP_ARCHITECTURE_PROPOSAL.md)：責任邊界、Playbook、Runner、Proof、權限及版本治理。
2. [端到端執行流程與驗收契約](PLAYBOOK_MVP_EXECUTION_FLOW.md)：計畫准入、狀態轉移、交接、兩輪審查、停止恢復及待執行的驗收案例。
3. [架構討論紀錄](PLAYBOOK_MVP_ARCHITECTURE_NOTES.md)：歷史討論與決策來源。

架構建議稿與執行流程共同構成新版規格；討論紀錄中的舊草案保留歷史身分。文件中的本機角色路徑指原討論環境，不是此 repo 內的檔案。

## 歷史參考

- [原始交接](CODEX_HANDOFF_PLAYBOOK_ARCHITECTURE.md)
- [P00 實證原則](P00_GROUNDED_ANSWER_POLICY.md)
- [舊版工作流](LEGO_WORKFLOWS_P00.md)
- [agent-lego 參考原始檔](agent-lego/README.md)：舊版規格與局部參考程式，其測試不代表新版 Runtime 已通過驗收。

舊 Graphify 快照已刪除，未產生新版圖譜。CSV 匯出案例僅用於解釋流程，不是已選定的產品需求。
