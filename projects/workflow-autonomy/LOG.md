# workflow-autonomy 進度

## 2026-11-08
- 讀了 WORKFLOW、AGENTS、roles.json、playbooks 和 projects/ 的所有紀錄，找出跟使用者理想不合的地方（見 PROJECT.md「診斷」）。
- 從上游 clone 固定版本：mattpocock/skills@59db609、agency-agents@4e3ac3c、impeccable@924bbd1。複製 15 份 Matt Skill（各附 LICENSE）、impeccable，以及 282 個 agency 角色到 `library/agents/`。282 這個數字跟原電腦盤點記錄的數量相同。
- 新增 `scripts/sync_methods.py`，用來產生 CATALOG／INDEX 並重算 manifest 雜湊；`check_portability.py` 加上目錄同步檢查。
- 改寫 WORKFLOW、AGENTS、CLAUDE、CLAUDE_CLOUD、README、library/README；舊流程搬到 docs/WORKBENCH.md。7 個原生角色的開頭說明改成不綁 workbench。
- 驗證：`check_portability.py` PASS；`unittest` 51 項全部 OK。
- 已確認：Claude Code 在本 session 自動發現了新加入的 Skills（系統列出 code-review、tdd、impeccable 等）。
- 未驗證：impeccable 的 launcher 下載 engine（沒有執行）；agency 角色由 subagent 讀檔使用的實際效果（還沒在真實專案上跑過）。
