# Claude 雲端／換電腦接手

目標環境是 Claude Code 從 GitHub 取得這個 repo 的雲端 session；也適用新電腦上的 clone。工作方法與文件在 repo 內，不需要原電腦的 `~/.codex`、`~/.agents` 或個人 Claude 設定。這是 repo 準備與本機搬移驗證，尚未在真正的 Claude 雲端環境試跑。

## 第一次開始

1. 在 Claude Code 選擇 GitHub repo 與**包含這次整理的 branch／commit**。本機未推送的改動不會出現在雲端；GitHub 連線與平台權限由你的帳號提供，repo 不包含登入憑證。
2. 讀取根目錄 `CLAUDE.md`（匯入共用 `AGENTS.md`）、`docs/WORKFLOW.md`。根目錄 `.claude/skills/` 與 `.claude/agents/` 提供方法與角色；是否自動載入仍取決於 Claude 環境與組織設定。若未發現，明確讀取 repo 內的檔案，不能宣稱已原生啟用。
3. 在集合根目錄執行以下檢查，再提出需求。

```sh
WORKBENCH_ROOT="$(pwd -P)"
python3 scripts/check_portability.py
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" list
```

必要工具是 Python 3.11+ 與 Git；Python 控制程式及 UI 資料搜尋只使用標準庫。`design-taste-frontend` 的腳本另需 Node.js；檢查會回報 Node 是否可用，不會自動安裝。UI Skill 中需網路取圖、瀏覽器或其他工具的步驟仍受當次環境及授權限制，靜態搜尋能執行不等於完整 UI 驗收通過。

Claude 的一般 repo 雲端 session 可使用 repo Skills；若你開的是 Claude Projects 內的 cloud thread，官方文件目前指出不會自動載入 repo Skills，應依平台設定提供 Skill，或讓 Agent 明確閱讀 repo 中的方法來源。不可把兩種環境的自動發現能力混為一談。

## 可以直接給 Claude 的話

> 先讀 CLAUDE.md、docs/WORKFLOW.md 與 docs/CLAUDE_CLOUD.md，執行搬移檢查，查看既有 Projects。我要先討論一個需求種子：……。使用既有 clarify／planner 與 grill-with-docs，保存原始想法、每輪回答、決策和未決問題，等我確認共同理解後再銜接實作。

需求清楚時可以直接說：

> 新需求：……。交付……，限制……，我會用……判斷完成。依 repo Flow 推進，使用獨立 task worktree 與獨立 Reviewer；缺必要能力就保存缺口。

## 討論、角色與正式執行

- `grilling` 是分輪訪談方法；`grill-me` 是不寫本機討論文件的入口。Project 要保存討論時用 `grill-with-docs`，搭配 `domain-modeling` 記錄已定義詞彙與適用的 ADR；一般問答另存 Project 討論紀錄，不能把 glossary 當聊天筆記。
- 使用者每輪回答會改變決策樹；只問已具備前置答案的問題，由 Agent 查明可自行取得的事實。討論結束需要使用者確認共同理解，不因問完一輪就假定方向已定。
- `library/roles.json` 指定實際 Role 與 Skills。主對話負責控制命令；正式計畫固定來源後，作者／Reviewer 使用派工快照。Skill 引用的支援檔若實際使用，須列入該 task 的 `supporting_sources`，manifest 本身不代替計畫來源快照。
- 使用 Claude 工具回傳的實際 session／subagent ID，保存回執並填入 `planner`、`--actor` 與 `contributors`。等待工具明確回傳完成／停止，才可標示 `--stopped`。角色名稱不是 host ID；若環境沒有可查證身分或獨立上下文，保存能力缺口，不自編 ID 或以主對話自審。
- 控制程式建立 task branch／worktree；Claude 作者必須使用 `packet.workspace` 和精確 `allowed_paths`。不要另外開原生 worktree 取代已指定工作樹，也不要從作者副本建立第二個控制集合。`codex/` 只是目前私有 task 的歷史分支前綴，沒有呼叫 Codex 服務。
- 若平台不允許必要 Git worktree 操作、獨立查核或來源存取，停在已保存的狀態；文件與角色不提供額外工具權限。瀏覽器檢測仍需該次明確授權，發布／部署／外部寫入／付費不在 Workbench 本機交付範圍。

## 換 session 時保存什麼

工作成果和接手資訊需要進入 Git，之後的 GitHub session 才拿得到。由主控制者在安全回寫後，依使用者授權及當次平台分支規則處理 commit／push；作者不直接推私有 task repo，不強制推送或改動其他分支。平台自動帶走 commit 的行為也須以實際結果確認。

在 `projects/<slug>/HANDOFF.md` 保存原始需求、使用者已確認的決策、固定成果路徑／版本、實際驗證、未決問題、下一步及當前限制；相關討論、Proof 放同 Project 可追蹤的文件。版本綁定採已知的固定成果 commit／digest，避免要求手寫文件包含它自身尚未產生的 commit。

新 session 同時查看 `projects/` 的文件和 `workbench.py list`。目前 `list` 只列**本環境有正式狀態**的專案；GitHub clone 可能已有 Project 文件、卻沒有本機正式狀態。遇到這種情況先讀接手紀錄並說明缺口，不能覆寫目錄、重跑已接受工作，或另建同目標 Project 假裝無事；若需要重建正式追蹤，先與使用者決定重建範圍與來源關聯。

本機 `.workflow/` 與 `tasks/` 被 Git 忽略，其中包含控制狀態、封存資料及私有 Git worktrees；此次不搬它們，也不提供跨主機執行狀態匯入。`adopt-git` 只接管同一私有 repo 的既有工作樹，不能用來恢復新機器。repo 內 `workflow-hub` 是建立這套體系的歷史試跑紀錄，不是你的第一個業務需求。

## 維護與驗證邊界

- `.claude/methods-manifest.json` 提供檔案雜湊、原來源摘要及適配紀錄；隨附授權保留。方法來源更新後應重新查核，不直接對進行中的計畫替換內容。
- `python3 scripts/check_portability.py` 只做工具、來源、manifest 與檔案完整性檢查；不呼叫模型、不連線 GitHub、不啟動瀏覽器。
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q` 驗證本機控制及搬移行為；不證明 Claude 平台已原生載入角色、登入／網路設定可用，或所有領域交付已通過。

平台依據（查核日期 2026-10-29）：[CLAUDE.md／共用指引匯入](https://code.claude.com/docs/en/memory)、[Skills 與雲端差異](https://code.claude.com/docs/en/skills)、[Project subagents](https://code.claude.com/docs/en/sub-agents)、[Cloud session 與 GitHub](https://code.claude.com/docs/en/claude-code-on-the-web)。平台後續行為可能更新，以當次環境實際能力為準。
