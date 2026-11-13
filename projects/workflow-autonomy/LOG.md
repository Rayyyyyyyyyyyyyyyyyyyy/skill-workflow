# workflow-autonomy 進度

## 2026-11-08
- 讀了 WORKFLOW、AGENTS、roles.json、playbooks 和 projects/ 的所有紀錄，找出跟使用者理想不合的地方（見 PROJECT.md「診斷」）。
- 從上游 clone 固定版本：mattpocock/skills@59db609、agency-agents@4e3ac3c、impeccable@924bbd1。複製 15 份 Matt Skill（各附 LICENSE）、impeccable，以及 282 個 agency 角色到 `library/agents/`。282 這個數字跟原電腦盤點記錄的數量相同。
- 新增 `scripts/sync_methods.py`，用來產生 CATALOG／INDEX 並重算 manifest 雜湊；`check_portability.py` 加上目錄同步檢查。
- 改寫 WORKFLOW、AGENTS、CLAUDE、CLAUDE_CLOUD、README、library/README；舊流程搬到 docs/WORKBENCH.md。7 個原生角色的開頭說明改成不綁 workbench。
- 驗證：`check_portability.py` PASS；`unittest` 51 項全部 OK。
- 已確認：Claude Code 在本 session 自動發現了新加入的 Skills（系統列出 code-review、tdd、impeccable 等）。
- 未驗證：impeccable 的 launcher 下載 engine（沒有執行）；agency 角色由 subagent 讀檔使用的實際效果（還沒在真實專案上跑過）。
- 獨立 reviewer（另一個上下文）驗收 `8579001`：C1–C5 PASS，C6 PASS 但附 4 項必修。282 個角色檔、15 份 Matt Skill、impeccable 都和上游逐 byte 相同。
- 修正 4 項必修：
  - 12 份 `disable-model-invocation` 的 Skill 在目錄標成「讀檔」，WORKFLOW 寫明這類 Skill 直接讀 SKILL.md。
  - 新增 `docs/agents/`（本機 Markdown tracker，票放 `projects/<slug>/`），Matt 工程系列不必再跑 setup，也不會建立 GitHub issue。
  - push 規則寫清楚：推到這次的工作 branch 不必問；推到 main、開 PR、推到別人的 repo 要先問。
  - PROJECT.md「授權」欄只能記使用者原話、日期與出處。
- 一併採納的建議：卡關定義統一成「同一個問題換三種做法都沒進展」；種子模式提概念時一起附完成線，使用者只要選一次；使用者要深入討論時以 grilling 節奏為準；補上網路被擋時的處理方式；補上舊專案怎麼轉成新格式。
- 沒採納：sync_methods 的測試、收錄 agency 的 strategy/、還原上游完整版 ask-matt，這幾項留作後續。
- 驗證：check_portability PASS；unittest OK。

## 2026-11-09
- 查證：arxiv、claude-design、ideation、plan、sketch 等 11 個 Skill 只存在 `~/.codex/skills/`、它的備份，以及 `~/Documents/Codex/2026-06-27/sli/work/local-skills/`，不在 `~/.claude/skills/`，也不在 Claude 帳號的 Skill 清單裡。判斷是 Codex 工作時自建的，不是 Claude 內建。
- 依使用者決定刪除 Codex 相關內容：
  - 刪掉 `docs/CLAUDE_SKILLS_INSTALL.md`（剩下的內容只有那 11 份待搬清單和 Codex 排除工具）。
  - CLAUDE_CLOUD 的待搬清單改成「新增 Skill 或角色」的通用做法。
  - WORKBENCH.md 和 workbench.py 的說明不再提 Codex。
- 保留不動：
  - `library/git_tasks.py` 的 `codex/` branch 前綴。改名的話，原電腦上既有的 workbench task branch 就接不上了。
  - `projects/` 底下的歷史紀錄，以及 `docs/playbook/` 的設計稿。
- 驗證：check_portability PASS；unittest OK。

## 2026-11-11 repo 審查後的調整（branch `ft/workflow-cleanup`）
- reviewer 角色內文改成純驗收者：逐條 PASS／FAIL／UNKNOWN、證據親自取得、不改成果。原因：上游 Code Reviewer 人設要求「建議不要求、稱讚、鼓勵」，跟逐票驗收相反。
- `docs/agents/issue-tracker.md` 加本 repo 例外：不做 to-tickets 的使用者核准輪、票必須寫成檔案、必填 Scope／Out of scope／Verify。原因：repo 裡沒有任何 `projects/*/issues/`，票只存在對話裡。
- `docs/WORKFLOW.md` 明確度關卡加上零 context 檢查（一批票派工前，全新 subagent 只讀票檔，回報哪裡必須猜）。來源：Dave Rensin 的 Elephant-Goldfish Model。
- README「怎麼用」補上範例。
- 使用者決定刪掉 workbench：移除程式、文件、playbooks、roles.json、git_tasks.py、`runtime-reference/config/` 與對應測試；七個角色前言不再提 dispatch packet；四個舊專案的接續指令改成指向 `records/`。`check_portability.py` 不再讀 roles.json。
- 驗證：check_portability PASS；unittest 3 個測試 OK。
- 未驗證：新的 reviewer 與零 context 檢查還沒在真實票上跑過。
- 還沒決定：`~/.claude/agents/` 的 286 個全域角色、全域與專案兩套瀏覽器規則以哪一套為準。

## 2026-11-11 重新確定目標，照目標模式執行 G1–G5
- 做了什麼：目標原文寫進 PROJECT.md 與 README；WORKFLOW 第 6 節加上收尾要記的兩個數字；CLAUDE.md 加方法凍結規則；工具庫不動。commit `1eca1b2`。
- 獨立驗收：全新 sonnet subagent 先讀新版 `.claude/agents/reviewer.md` 再驗收，G1–G5 共 5 條 PASS、0 FAIL、0 UNKNOWN，每條附它自己跑的指令與輸出。這是新 reviewer 角色第一次實際使用；驗收者回報角色說明沒有需要猜的地方。
- 驗收者註記：G5 的 grep 依條件排除了 `skills/`。主 session 先前查過，該目錄裡的 "workbench" 只出現在字型名稱與網站描述文字，跟被刪的程式無關。
- 未驗證：零 context 的票檔檢查還沒在真實票上跑過；新 reviewer 還沒驗過程式碼類的票。
- 收尾數字：使用者被問 3 次（審查後問是否動手、刪除 workbench 後問 push 與 integrator、重新確定目標時問三項決定）；獨立驗收 FAIL 0 輪。
- 下一步：等使用者決定 push 與併回 main。

## 2026-11-11 瀏覽器規則改為每次授權；併回 main
- 使用者決定以全域版為準：`CLAUDE.md` 護欄、`docs/WORKFLOW.md` 的「驗」與 PROJECT.md 格式都改成「每次檢測當次授權，專案文件不算授權」。既有專案 PROJECT.md 裡記過的瀏覽器授權從此不再有效。
- 使用者指示 push `ft/workflow-cleanup` 並併回 main。
- 驗證：check_portability PASS；unittest OK。

## 2026-11-11 刪除 integrator 與全域重複角色
- 刪除 `.claude/agents/integrator.md` 與 manifest 的來源紀錄；README 的原生角色數改為 6。
- 使用者電腦的 `~/.claude/agents/`：刪除前逐檔比對，282 個與 `library/agents/` 逐位元相同才刪；剩 4 個 `impeccable-*`。要還原就從 `library/agents/` 複製回去。
- 驗證：check_portability PASS；unittest OK；sync 輸出 6 native roles。

## 2026-11-11 刪除已結案專案；補裝 implement-spec、retro、pr
- 使用者指示：舊專案都已結案，刪掉。移除 `projects/` 下 8 個資料夾（book-notes、book-reader-mobile、book-reader-ux、claude-cloud-portability、skill-install-handoff、skills-inventory、winter-ux-motion、workflow-hub），只留 workflow-autonomy。要找回就從 git 歷史（`c185aec` 之前）取。
- 使用者指示補裝 `implement-spec`、`retro`、`pr`：取自 mattpocock/skills 與既有 Matt skills 相同的 commit `59db609`，內容未改；同時複製到 `~/.claude/skills/`。
- 已知殘留：manifest 裡 ponytail 的 `fixed_evidence.path` 指向已刪的 `projects/claude-cloud-portability/records/package-review-v1.md`，該檔可從 `review_commit` `b9c7e23` 取回。
- 驗證：sync 輸出 29 skills；check_portability PASS；unittest OK。
- 未驗證：三個新 Skill 還沒實際跑過。

## 2026-11-12 外部 repo 專案的紀錄改放 `project/<slug>` branch
- 起因：template-upgrade 的紀錄被 commit 到本 repo `main`（3 個本機 commit，未 push）。使用者：「但那跟skill-workflow這個repo本體沒有關係呀 只是利用了方法工具，但更新的目標repo另有其他 要push也是另開branch」，並要求「不只要在記憶，也要更新在workflow的方法步驟裡」。
- 處理：3 個 commit 移到本機 branch `project/template-upgrade`，`main` 退回 `origin/main`（`4161ce1`）。
- 方法修改：`docs/WORKFLOW.md` 接案第 1 步加看 `project/*` branch，新增「紀錄 commit 在哪」；`docs/CLAUDE_CLOUD.md` 外部 repo 與保存兩段、`CLAUDE.md` 架構要點同步。

## 2026-11-13 主目錄固定停在 main，專案紀錄改用 worktree
- 起因：主目錄停在 `project/template-upgrade`，使用者每次想改 main 都得特別說要隔離。使用者同意改成 worktree，並等 template-upgrade 結束才執行。
- 處理：template-upgrade 已完成並 push（`project/template-upgrade` 的 `94f7c8a`），主目錄切回 `main`。
- 方法修改：`docs/WORKFLOW.md`「紀錄 commit 在哪」改成外部專案紀錄在 `../skill-workflow-project-<slug>` worktree 做；主目錄只放方法修改，可直接 commit，push 前先問。`CLAUDE.md` 架構要點同步。`docs/CLAUDE_CLOUD.md` 不改，因為雲端 session 每次都是新 clone，直接切 branch 就好。
