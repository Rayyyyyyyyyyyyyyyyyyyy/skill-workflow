# Project Workbench

把想法放進來，在這個 folder 建立或接續 Project，選擇適合的 Flow，由 Agent 按 Playbook 做事，最後以 Proof 驗收。

## 怎麼使用

在這個 repo 開啟對話，直接描述你想做的事。例如：

> 我想做一個離線探索遊戲，先幫我確認玩法與第一版範圍。

> 在 csv-export 專案修正空資料時漏掉標題列的問題，交付本機可驗收版本。

> 接續 csv-export，先看上次停在哪裡，再完成剩餘工作。

Agent 會保存想法、判斷資料是否足夠、組成 Flow、載入 Role 與 Skills、執行工作、提交證據並安排獨立驗收。需求清楚就直接做；有關鍵缺口才釐清、研究或做原型。選路由 Agent 依原始需求判斷並留下理由，CLI 不宣稱能自動理解自然語言。

## 各層負責什麼

| 層次 | 責任 |
|---|---|
| Project | 保存一個目標的需求、決策、進度、成果及證據 |
| Flow | 組合適用 Playbooks，固定依賴、交接及交付終點 |
| Playbook | 定義可委派、可驗收的工作契約與內部階段 |
| Agent Role | 提供執行者的專業責任與判斷準則 |
| Skill | 提供角色完成工作的方法 |
| Proof | 對指定成果版本提供逐項驗收證據與查核結果 |
| 控制程式 | 保存正式狀態，檢查計畫、版本、依賴與接受條件 |

共用方法放在 `library/`；專案放在 `projects/<slug>/`。每個小任務使用獨立 Git branch/worktree；`workspace/` 保存一般專案的來源與安全回寫成果，`.workflow/` 保存 SQLite、私有 Git repo、快照及證據。可並行的小任務分開工作，已接受的提交再經整合與獨立 Proof。

## 本機控制入口

需要 Python 3.11 以上與本機 Git；Python 部分只使用標準庫。控制命令始終使用原集合根目錄，即使作者已在 task worktree 裡：

```sh
WORKBENCH_ROOT=/Users/ray.shao/workflow
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" new csv-export --idea "修正 CSV 空資料匯出漏掉標題列，交付本機可驗收版本"
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" list
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" status csv-export
```

建立 Project 只是保存需求；正式工作還要有固定計畫、需求與驗收對應、Role／Skill 來源及准入查核。作者使用派工包的隔離 `workspace`；原集合入口為 `controller_root`，兩者不能混用。已接受 Git 版本經必要整合、重新 Proof 及安全回寫後，才完成 Project。完整命令與執行規則見 [工作流程](docs/WORKFLOW.md)。

## 可執行範圍

目前採受信任的本機協作模式：現有 Codex 對話與協作 Agent 負責實際思考及工具操作，Python／本機 Git 控制程式管理經由其入口的隔離 task、狀態、版本、整合、Proof 與安全回寫。沒有另建模型服務 Runner，也不是背景常駐自動化。

task 工作樹由當前選定輸入建立固定 Git 基線，不從舊 HEAD 忽略本次新檔，也不 reset／stash 來源既有修改。回寫前逐檔比對 baseline；使用者途中改動時等待而不覆寫，來源 Git HEAD／index 不變。

角色／技能來源快照、成果封存與 Digest 有助於追溯和查核；它們不保證自然語言判斷正確，也不能阻擋同一 OS 帳號的惡意程式直接修改控制資料。Agent 身分及停止紀錄由可信控制者依 host 的實際訊號登記。

本版不提供外部發布、部署、付費、敵意 Worker 隔離、精確費用上限或跨主機恢復。瀏覽器檢測仍須取得該次明確授權；缺少必要驗收就保留缺口，不標成完整交付。

## 規格與參考

- [工作流程](docs/WORKFLOW.md)：當前六步入口、交接、Proof、等待與恢復。
- [共用方法](library/)：Playbook、Role 與 Skill 綁定。
- [原完整架構設計](docs/playbook/PLAYBOOK_MVP_ARCHITECTURE_PROPOSAL.md)、[原流程規格](docs/playbook/PLAYBOOK_MVP_EXECUTION_FLOW.md)：保留完整控制、隔離及外部操作的目標要求；文中已刪除實作的連結與舊能力宣告不適用於目前版本。
- [參考元件](runtime-reference/README.md)：獨立的授權、契約、證據與持久化範例；其測試不代表目前端到端 Flow 已驗收。

實際測試與試跑證據應綁定當次程式、契約及產物版本；請依交付時的驗證報告判斷能力，不能只憑這份說明宣告通過。
