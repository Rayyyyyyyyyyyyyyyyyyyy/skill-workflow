# skill-install-handoff

## 原始想法

改成交給 Claude 自行安裝的技能清單；沿用排除 Codex 外掛／CLI 專屬工具條件，列出本機已安裝方法、可查證上游、repo 已附與缺來源項目。包含 Agency 與 Matt 系列，不複製／安裝新 Skills 或角色庫，不改 Flow。

進度與接續：在集合根目錄執行 `python3 workbench.py status skill-install-handoff`。
正式狀態與版本保存在 `.workflow/`；成果預設放 `workspace/`。
