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
