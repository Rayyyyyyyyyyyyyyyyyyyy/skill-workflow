@AGENTS.md

# Claude 工作入口

先讀 `docs/WORKFLOW.md`；在新電腦或 GitHub 雲端 clone 上，接著讀 `docs/CLAUDE_CLOUD.md`。共用工作規則以 AGENTS.md 為準，不依賴前一個 session 的聊天記憶。

- Role 在 `.claude/agents/`，Skills 在 `.claude/skills/`；控制程式綁定以 `library/roles.json` 為準，不需要原電腦的個人安裝。
- 想法需要討論培養時用既有 `clarify`／planner 與 `/grill-with-docs`；`/grill-me` 是不保存文件的入口。完整訪談方法是 `grilling`，先讀再用，使用者確認共識後才銜接實作。
- 雲端首次開工先跑 `python3 scripts/check_portability.py`，同時查看 `projects/` 文件和控制程式 `list`；空 list 不代表已存在的 Project 可被覆寫。
- 主對話是控制者。派工包固定來源優先於當前可變檔案；作者在控制程式指定的工作樹執行，不另建原生 `isolation: worktree` 取代它。Reviewer 使用另一個上下文。
- 瀏覽器檢測、部署、發布與付費的限制仍適用。套件內附的瀏覽器腳本不代表已獲執行授權。
