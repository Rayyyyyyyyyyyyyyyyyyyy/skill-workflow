# Claude 雲端／換電腦接手

工作方法都在 repo 裡，不需要原電腦的個人設定目錄。

## 第一次開始

1. 在 Claude Code 選這個 repo，並選含最新整理的 branch。本機還沒推送的修改，雲端看不到。
2. 讀 `CLAUDE.md`，再讀 `docs/WORKFLOW.md`。
3. 在 repo 根目錄執行 `python3 scripts/check_portability.py`，然後看 `projects/` 底下各 Project 的 `PROJECT.md`，掌握目前進度。

`.claude/skills/` 底下的 Skills 會自動發現。`library/agents/` 底下的角色不會自動載入，要用時請 subagent 先讀角色檔。在 Claude Projects 裡開的 cloud thread 可能不會載入 repo Skills，這時就直接讀 `.claude/skills/<name>/SKILL.md`。

## 可以直接給 Claude 的話

> 目標：……。做到……就算完成。

> 方向：我想讓……變得更好，先跟我談這次要推進到哪裡。

> 種子：我有個想法……，先研究看看，只問你查不到的事。

> 接續 <slug>，從上次停下的地方繼續。

## 外部 repo

成果在別的 repo 時（例如 winter、book-reader），用 `add_repo` 或 clone 把它加進 session，在那個 repo 的 branch 上工作，紀錄寫回這裡的 Project 資料夾。PROJECT.md 的「目前狀態」只在實際查過外部 repo 之後才更新，並寫上查核日期。

## 換 session 時保存什麼

雲端容器用完就會回收，所以重要的東西都要 commit 並 push：成果、`PROJECT.md`、`LOG.md`。舊 Project 照資料夾裡現有的文件接續，不要重建或覆寫。

## 新增 Skill 或角色

把整個資料夾放進 `.claude/skills/<name>/`（角色放 `.claude/agents/` 或 `library/agents/<分部>/`），然後跑 `python3 scripts/sync_methods.py`，並在 `.claude/methods-manifest.json` 的 `packages` 記下來源與版本。
