# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

# Claude 工作入口

先讀 `docs/WORKFLOW.md`；在新電腦或 GitHub 雲端 clone 上，接著讀 `docs/CLAUDE_CLOUD.md`。共用工作規則以 AGENTS.md 為準，不依賴前一個 session 的聊天記憶。

- Role 在 `.claude/agents/`，Skills 在 `.claude/skills/`；控制程式綁定以 `library/roles.json` 為準，不需要原電腦的個人安裝。
- 想法需要討論培養時用既有 `clarify`／planner 與 `/grill-with-docs`；`/grill-me` 是不保存文件的入口。完整訪談方法是 `grilling`，先讀再用，使用者確認共識後才銜接實作。
- 雲端首次開工先跑 `python3 scripts/check_portability.py`，同時查看 `projects/` 文件和控制程式 `list`；空 list 不代表已存在的 Project 可被覆寫。
- 主對話是控制者。派工包固定來源優先於當前可變檔案；作者在控制程式指定的工作樹執行，不另建原生 `isolation: worktree` 取代它。Reviewer 使用另一個上下文。
- 瀏覽器檢測、部署、發布與付費的限制仍適用。套件內附的瀏覽器腳本不代表已獲執行授權。

## 常用命令

需要 Python 3.11+（用到 `tomllib`）與 Git；控制程式只用標準庫，`design-taste-frontend` 的腳本另需 Node.js。

```sh
python3 scripts/check_portability.py                                   # 方法包／雜湊可搬移檢查
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q     # 控制程式測試
python3 -m unittest tests.test_workbench.WorkbenchTests.test_plan_must_be_independently_approved_before_dispatch  # 單一測試
WORKBENCH_ROOT="$(pwd -P)"; python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" list
```

`runtime-reference/` 有獨立測試（需 `jsonschema>=4`，見其 README），不代替當前 Flow 驗收。

## 架構要點

- `workbench.py`：單檔 CLI 控制者（子命令見 `--help`，流程見 `docs/WORKFLOW.md`）。輸出 JSON 到 stdout，錯誤以 JSON 寫 stderr 並 exit 2。
- 正式狀態：每個 Project 的 `projects/<slug>/.workflow/state.sqlite3`，加上私有 Git repo、來源快照與證據；這些與 `projects/*/tasks/` 都被 gitignore，clone 不會帶上。來源及安全回寫目錄預設是 `projects/<slug>/workspace/`，計畫設 `workspace: "."` 時改為集合根目錄。
- `library/git_tasks.py`：私有 Git 快照與 task worktree；從不 stage／reset 來源 repo。`allowed()`／`clean()` 守住 task `allowed_paths`。
- `library/playbooks/*.json`（clarify、research、design、deliver、review、integrate）提供各 task 的最低驗收項，`plan` 存入時自動附加為 `PB-<task>-<criterion>`。
- `library/roles.json` 把 Role 綁到 `.claude/agents/*.md` 與 `.claude/skills/*/SKILL.md`；派工時固定內容 Digest。`.claude/methods-manifest.json` 記錄方法包來源與檔案雜湊，`check_portability.py` 依它查核。改 Role／Skill 檔要手動更新 manifest `files` 內的 SHA-256（沒有更新腳本），否則檢查回報 `method checksum mismatch`。
- Task 狀態流：`READY → RUNNING → AWAITING_REVIEW → DONE`，異常進 `WAITING`（附 reason，如 `GIT_MERGE_CONFLICT`、`REVIEW_BLOCKED`）或 `CANCELLED`。Project 層另有自己的 `state`／`reason`（如 `PLAN_REWORK_REQUIRED`、`SOURCE_CHANGED`）。審查 FAIL 時第 1 輪退回 `READY`，之後進 `WAITING`（`GOAL_ALIGNMENT_REQUIRED`）。輪次、Attempt 與准入失敗計數跨重啟保留，不可藉換計畫歸零。
- `tests/test_workbench.py` 以行為描述命名測試，是控制契約的可執行規格；改 `workbench.py` 行為先對照它與 `docs/WORKFLOW.md`。
