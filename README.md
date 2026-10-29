# Project Workbench

把想法放進來，在這個 repo 建立或接續 Project，透過討論培養需求、選擇 Flow，由 Agent 按 Playbook 做事，以 Proof 驗收。

## Claude 雲端開始

在 Claude Code 選這個 GitHub repo，使用包含最新整理的 branch／commit，先讀 [CLAUDE.md](CLAUDE.md) 和 [雲端接手](docs/CLAUDE_CLOUD.md)。Role／Skills 與所需支援檔隨 repo 保存，不必複製原電腦的個人安裝。

在集合根目錄先執行：

```sh
python3 scripts/check_portability.py
python3 workbench.py list
```

需要 Python 3.11+ 和 Git；設計 Skill 的 JavaScript 工具另需 Node.js。這是 repo 內的可搬移方法包；尚未在真正 Claude 雲端試跑，平台自動發現及工具權限須依當次環境確認。

## 怎麼提出需求

直接在這個 repo 的對話說：

> 我有一個需求種子：……，先跟我討論，幫我把方向長出來。

> 我想做一個離線探索遊戲，先確認玩法與第一版範圍。

> 在 csv-export 專案修正空資料時漏掉標題列的問題，交付本機可驗收版本。

需求種子使用既有 clarify／planner 與 `grilling`，分輪討論並保存使用者決策；Project 優先用 `/grill-with-docs`，`/grill-me` 是不保存文件的入口。你確認共同理解後，再銜接研究、設計或實作。需求已清楚就直接選適用工作，不強制重跑訪談。

Agent 保存原始想法、判斷成熟度、組成 Flow、載入 Role／Skills、執行工作並安排獨立 Proof。這些選路由 Agent 留下理由，CLI 不宣稱能理解自然語言，也不是背景常駐服務。

## 各層負責什麼

| 層次 | 責任 |
|---|---|
| Project | 保存目標、原始需求、討論、決策、進度、成果及證據 |
| Flow | 組合適用 Playbooks，固定依賴、交接及交付終點 |
| Playbook | 定義可委派、可驗收的工作契約與內部階段 |
| Agent Role | 提供執行者的專業責任與判斷準則 |
| Skill | 提供角色完成工作的方法 |
| Proof | 對指定成果版本提供逐項驗收證據與查核結果 |
| 控制程式 | 保存正式狀態，檢查計畫、版本、依賴與接受條件 |

## 文件與方法的位置

| 路徑 | 用途 |
|---|---|
| [AGENTS.md](AGENTS.md) | Claude／Codex 共用入口與使用者護欄 |
| [docs/WORKFLOW.md](docs/WORKFLOW.md) | 當前六步流程、正式命令、Git tasks、Proof 與恢復契約 |
| [docs/CLAUDE_CLOUD.md](docs/CLAUDE_CLOUD.md) | GitHub 雲端、新 session 與新電腦接手 |
| [library/](library/README.md) | Playbooks 及 Role／Skill 綁定 |
| `.claude/agents/`、`.claude/skills/` | 隨 repo 保存的實際角色指引與 Skills |
| `.claude/methods-manifest.json` | 方法包版本、來源、適配與檔案雜湊 |
| `projects/<slug>/` | 原始想法、可追蹤成果及接手紀錄；新 session 也要查看這裡 |
| [docs/playbook/](docs/playbook/) | 原完整目標設計；未落實能力及舊實作連結不作目前能力宣告 |
| [runtime-reference/](runtime-reference/README.md) | 獨立參考元件，其測試不代替當前 Flow 驗收 |

正式命令一律使用原集合入口，即使作者已在 task worktree：

```sh
WORKBENCH_ROOT="$(pwd -P)"  # 在集合根目錄設定
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" new csv-export --idea "修正 CSV 空資料匯出漏掉標題列，交付本機可驗收版本"
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" status csv-export
```

建立 Project 只是保存需求；還須固定計畫、准入、獨立 task worktrees、Proof，以及必要整合與安全回寫。主 repo 的 HEAD／index 與使用者既有修改不被控制程式 reset、stash 或 stage。

## 執行範圍

目前是受信任的本環境協作：Claude Code／Codex 與協作 Agent 執行工作，Python 標準庫與本機 Git 管理狀態和成果。支援研究、設計、工程／文件的本機交付；不提供部署、發布、外部寫入、付費、敵意 Worker 隔離或精確費用上限。瀏覽器檢測須另外明確授權。

換 session 依靠已推上 GitHub 的文件與成果，不靠前一段聊天。正式控制狀態與私有工作樹不進 Git，尚不支援跨主機還原執行中的任務；詳見雲端接手。來源／版本快照可追溯，但不能保證 Agent 判斷正確。
