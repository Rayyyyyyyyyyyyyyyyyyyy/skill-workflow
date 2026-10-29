# Claude 雲端方法包接手

原始目標：整理這個 repo 的文件及用到的 Skills，供 Claude 雲端 session 從 GitHub clone 使用；使用者確認只搬 repo 所需方法，目前沒有要搬移的業務 Project 執行狀態。

交付入口：CLAUDE.md、AGENTS.md、docs/WORKFLOW.md、docs/CLAUDE_CLOUD.md。實際方法：.claude/agents、.claude/skills，由 library/roles.json 綁定，methods-manifest.json 記錄來源及內容雜湊。包括既有 grilling 與有／無文件的討論入口，沒有新增另一套討論 Playbook。

執行：先跑 python3 scripts/check_portability.py，讀雲端接手後提出需求。正式版本由控制程式提交／Proof 記錄固定 commit，勿把本文當作正式接受。驗證範圍與未執行項目見 VALIDATION.md。

下一步：此版經獨立 Proof 接受及安全回寫；由使用者授權的主控制者 commit／push 到 GitHub 後，雲端 session 才能取得。推送狀態依來源 Git history 與 remote 確認；不要把本機驗收當作發布憑證。真正 Claude 雲端需再確認方法發現、獨立 Agent ID／停止訊號、工具與 GitHub 權限。既有本機 .workflow/tasks 不需搬移，正式跨機恢復尚不支援。
