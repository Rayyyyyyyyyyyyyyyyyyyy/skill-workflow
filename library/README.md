# library

| 路徑 | 內容 |
|---|---|
| [CATALOG.md](CATALOG.md) | 工具目錄：Skills、原生角色、角色庫分部。每次接任務先看這裡 |
| [agents/INDEX.md](agents/INDEX.md) | 282 個專業角色的一行說明，方便用關鍵字搜尋 |
| `agents/<分部>/*.md` | agency-agents 角色檔（MIT，來源版本見 `.claude/methods-manifest.json`） |
| `playbooks/*.json`、`roles.json`、`git_tasks.py` | 可選的 [Workbench](../docs/WORKBENCH.md) 使用的契約與角色綁定 |

CATALOG.md 和 INDEX.md 由 `python3 scripts/sync_methods.py` 產生，這個腳本也會更新 manifest 的檔案雜湊。

Playbooks 的 `required_criteria` 也可以當成一般工作的驗收清單參考：research 要有可追查的來源，design 要有可接手的狀態與流程，deliver 要附驗證證據。
