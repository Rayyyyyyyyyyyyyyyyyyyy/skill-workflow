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
