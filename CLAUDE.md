# CLAUDE.md

這個 repo 收納使用者的 Projects 和共用的工作方法。使用者丟進來的可能是目標、方向，或天馬行空的種子；你負責推進到完成線每一條都有證據。

## 往哪裡找

| 什麼時候 | 讀什麼 |
|---|---|
| 收到想法、要接續專案、要回報進度 | [method/WORKFLOW.md](method/WORKFLOW.md) |
| 新電腦或雲端 clone 第一次開工 | [method/CLAUDE_CLOUD.md](method/CLAUDE_CLOUD.md) |
| 挑 Skill 和角色 | [method/CATALOG.md](method/CATALOG.md)（由 `scripts/sync_methods.py` 產生，不要手改） |
| 寫 spec、切票，或 Skill 要找 issue tracker | [method/agents/issue-tracker.md](method/agents/issue-tracker.md)；triage 標籤看 `method/agents/triage-labels.md`，領域文件看 `method/agents/domain.md` |
| 回報時分清楚事實、推論和假設 | [method/policies/P00-GROUNDED-ANSWER.md](method/policies/P00-GROUNDED-ANSWER.md) |
| 某條規則為什麼這樣改、已結案專案的最後 commit | [records/METHOD_LOG.md](records/METHOD_LOG.md) |
| 方法改動參考過的外部文章 | `records/references/`（例如 [rieseberg-ambition.md](records/references/rieseberg-ambition.md)：完成線的外部判準與四問從這裡來） |
| 接續某個專案：目標、完成線和進度 | 先用 `git branch -a --list '*project/*'` 找出 `project/<slug>`，再讀那個 branch 上的 `projects/<slug>/PROJECT.md` 和 `LOG.md` |

## 資料夾分工

- `method/`：方法，也就是執行時要照做的規則。
- `records/`：紀錄，只往後追加。裡面的內容和 `method/` 或本檔衝突時，以 `method/` 和本檔為準。
- `.claude/skills/`、`.claude/agents/`：Skills 和原生角色，Claude Code 會從這裡自動發現。專業角色裝在全域 `~/.claude/agents/`，直接拿名稱當 subagent 類型開；新電腦的安裝方式見 README「另外安裝」。
- `scripts/`、`tests/`：檢查方法包用的工具。
- `main` 只放方法和紀錄。Project 一律在 `project/<slug>` branch、worktree `../skill-workflow-project-<slug>` 裡做（細節見 WORKFLOW.md 第 1 節）。

## 你負責到底

- 自己判斷怎麼做：上網查資料、讀原始碼、試跑、試錯，一直推進到完成線每一條都有證據。可以開多個 subagent 平行做，或讓它們互相審查。
- 主對話負責協調；實作和驗收交給不同的 subagent，讓 reviewer 用另一個上下文去看。
- 使用者想深入討論時，用 `grilling`／`grill-with-docs`。
- 只在需要使用者時才問：帳號、金鑰或付費；部署、發布、推到 main、開 PR 或其他對外寫入；不可逆或會覆寫使用者資料的動作；會改變方向的個人喜好；擴大範圍。commit 和 push 到這次工作用的 branch 不必問。其他事情自己決定，把理由記進 LOG.md。
- 方法凍結：方法（本檔、`method/`、`.claude/agents/`、Skills）只在真實專案卡住、而且原因出在方法本身時才改。修改內容和原因追加到 `records/METHOD_LOG.md`，不另開以方法為主題的專案。方法修改的獨立驗收照 WORKFLOW.md 第 5 節開 `reviewer`（比執行者高一級，預設 opus）。

## 護欄

- 瀏覽器不自行使用，不論是檢測、測試、驗證、除錯、預覽或截圖。範圍包含 Claude in Chrome、內建瀏覽器、既有分頁，以及 Playwright、Puppeteer 等啟動的有介面或 headless 瀏覽器。需要時先告訴使用者檢測目的、為什麼必要、不做的話驗證會缺什麼，然後等使用者明確授權那一次檢測。一般的「測試」「驗證」「完成任務」指示不算授權；PROJECT.md、Skill 或工具建議的瀏覽器步驟也不算。沒授權時照常跑靜態、單元、建置與 API 檢查，把缺少的瀏覽器驗收列為缺口，不宣稱通過沒跑過的檢測。
- 涉及金鑰、權限、持久資料或破壞性操作時，保護敏感資訊，在可信的邊界上驗證，保留既有資料。影響範圍不清楚時先問，並說明一旦出錯能不能恢復。
- 對外部 repo 維持它原本的狀態：照它自己的 AGENTS.md／CLAUDE.md 做事，在自己的 branch 上工作，主工作區裡使用者還沒 commit 的修改原樣保留。
- 介面要處理好等待、空結果、失敗、成功和重複操作，保留使用者可以恢復的輸入，鍵盤和輔助科技都要能操作。
- 回報時用證據說話（P00）：分清楚已修改、已驗證、未驗證，失敗和沒跑的項目也要列出來。

## 常用命令

需要 Python 3.11+ 與 Git；`design-taste-frontend` 的腳本另需 Node.js。

```sh
python3 scripts/sync_methods.py                                        # 新增或修改 Skill／Role 後，重產 method/CATALOG.md 與雜湊
python3 scripts/check_portability.py                                   # 方法包完整性檢查
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q     # 測試（方法包可搬移性）
```

Skills 的來源與版本記在 `.claude/methods-manifest.json` 的 `packages`。
