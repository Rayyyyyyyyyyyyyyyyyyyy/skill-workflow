# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

# Claude 工作入口

收到想法、方向或目標時，照 `docs/WORKFLOW.md` 推進。在新電腦或 GitHub 雲端 clone 上，先讀 `docs/CLAUDE_CLOUD.md`。

- 工具目錄在 `library/CATALOG.md`。Skills 會自動發現；`library/agents/` 裡的專業角色，要開 subagent 並請它先讀角色檔。
- 使用者想深入討論時，用 `grilling`／`grill-with-docs`。
- 主對話負責協調；實作和驗收交給不同的 subagent，好讓 reviewer 用另一個上下文去看。

## 常用命令

需要 Python 3.11+ 與 Git；`design-taste-frontend` 的腳本另需 Node.js。

```sh
python3 scripts/sync_methods.py                                        # 新增或修改 Skill／Role 後重產目錄與雜湊
python3 scripts/check_portability.py                                   # 方法包完整性檢查
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q     # 測試（workbench 與可搬移性）
```

## 架構要點

- `projects/<slug>/PROJECT.md`、`LOG.md`：每個 Project 的目標、完成線、工具、授權、決策與進度。換 session 時從這兩個檔案接續。
- `library/CATALOG.md`、`library/agents/INDEX.md`：由 `scripts/sync_methods.py` 產生，不要手改。來源版本記錄在 `.claude/methods-manifest.json` 的 `packages`。
- `workbench.py`＋`library/playbooks/`＋`library/roles.json`：可選的嚴格控制流程，說明在 `docs/WORKBENCH.md`；`tests/test_workbench.py` 是它的可執行規格。
