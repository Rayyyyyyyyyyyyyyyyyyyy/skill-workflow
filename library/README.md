# library

| 路徑 | 內容 |
|---|---|
| [CATALOG.md](CATALOG.md) | 工具目錄：Skills、原生角色、角色庫分部。每次接任務先看這裡 |
| [agents/INDEX.md](agents/INDEX.md) | 282 個專業角色的一行說明，方便用關鍵字搜尋 |
| `agents/<分部>/*.md` | agency-agents 角色檔（MIT，來源版本見 `.claude/methods-manifest.json`） |

CATALOG.md 和 INDEX.md 由 `python3 scripts/sync_methods.py` 產生，這個腳本也會更新 manifest 的檔案雜湊。
