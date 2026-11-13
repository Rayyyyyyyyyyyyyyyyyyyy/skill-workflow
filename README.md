# Project 集合

把目標、方向或天馬行空的想法丟進來，Agent 自己推進到完成線每一條都有獨立驗收的證據：上網查資料、挑工具、實作、舉證、試錯。這包方法 clone 到任何電腦或雲端都能直接用；專業角色要另外安裝（見「另外安裝」）。

## 怎麼用

在 Claude Code 開這個 repo，直接說其中一種：

> 目標：……。做到……就算完成。

> 方向：我想讓……變得更好，先跟我談這次要推進到哪裡。

> 種子：我有個想法……，先研究看看，只問你查不到的事。

> 接續 <slug>，從上次停下的地方繼續。

只有在需要帳號、金鑰、付費、部署、對外寫入、不可逆操作，或純屬你個人喜好的選擇時，Agent 才會回來問你。

## 工具

- [method/CATALOG.md](method/CATALOG.md)：Skills 與原生角色的目錄。
- `.claude/skills/`：Matt Pocock 系列、impeccable、ui-ux-pro-max、design-taste-frontend、humanizer、ponytail 等。
- 專業角色：[agency-agents](https://github.com/msitarzewski/agency-agents) 約 280 個，裝在全域 `~/.claude/agents/`，不在 repo 裡。

## 另外安裝（不在 repo 內）

換電腦或交接時，下面這些要另外裝，`check_portability.py` 會印出全域專業角色的數量。

| 項目 | 裝到哪 | 怎麼裝 | 沒裝會怎樣 |
|---|---|---|---|
| agency-agents 專業角色 | `~/.claude/agents/` | 裝 [Agency Agents app](https://agencyagents.app)（Mac：`brew install --cask msitarzewski/agency-agents/agency-agents`），它會自動更新；或 clone 上游 repo 執行 `./scripts/install.sh --tool claude-code` | 只能用 6 個原生角色 |
| Python 3.11+、Git | 系統 | 照各自官方方式 | 檢查腳本與測試跑不了 |
| Node.js | 系統 | 照官方方式 | `design-taste-frontend` 的腳本跑不了 |

### 比較常用到的專業角色

依過去專案的類型（網頁樣板、閱讀 app、iOS app、方法文件）推估，還沒有使用紀錄。名稱就是 subagent 類型。

| 角色 | 什麼時候用 |
|---|---|
| `Frontend Developer` | 網頁前端實作（React／Vue） |
| `Mobile App Builder` | iOS／Android 或跨平台 app |
| `Software Architect` | 系統設計、拆模組、技術取捨 |
| `UX Researcher` | 使用者行為、可用性問題 |
| `UX Architect` | 資訊架構、版面與 CSS 系統 |
| `Accessibility Auditor` | WCAG、鍵盤與讀屏檢查 |
| `Test Automation Engineer` | 端對端測試、修不穩定的測試 |
| `Performance Benchmarker` | 量測與調校效能 |
| `Codebase Onboarding Engineer` | 快速讀懂陌生的 codebase |
| `Application Security Engineer` | 威脅建模、安全審查 |
| `Reality Checker` | 紅隊：預設「還不能交」，要求證據 |
| `Evidence Collector` | 紅隊：重現問題、留下證據 |

規劃、研究、設計、實作、寫文件、驗收先用原生角色（`planner`、`researcher`、`designer`、`implementer`、`writer`、`reviewer`），它們改寫自 Product Manager、Research Synthesist、UI Designer、Minimal Change Engineer、Technical Writer、Code Reviewer。

## 文件

| 路徑 | 用途 |
|---|---|
| [CLAUDE.md](CLAUDE.md) | 入口：護欄、往哪裡找、常用命令 |
| [method/](method/) | 方法：流程、工具目錄、issue tracker 設定、P00 政策 |
| [method/WORKFLOW.md](method/WORKFLOW.md) | 三種輸入、推進迴圈、驗收、紀錄格式 |
| [method/CLAUDE_CLOUD.md](method/CLAUDE_CLOUD.md) | 雲端與新電腦接手 |
| [records/](records/) | 紀錄：方法修改的歷史、已結案專案的最後 commit、參考資料。不是規則 |
| `projects/<slug>/`（在 `project/<slug>` branch，不在 `main`） | 每個 Project 的目標、完成線、進度與成果 |

```sh
python3 scripts/check_portability.py   # 檢查方法包
python3 scripts/sync_methods.py        # 新增或修改 Skill／Role 後重產目錄
```
