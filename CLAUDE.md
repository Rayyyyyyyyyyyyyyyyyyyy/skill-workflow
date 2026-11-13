# CLAUDE.md

這個 repo 收納使用者的 Projects，也放共用的工作方法。使用者丟進來的可能是目標、方向，或天馬行空的種子；你負責推進到完成。收到想法、要接續專案或要回報進度時，先讀 [docs/WORKFLOW.md](docs/WORKFLOW.md)。在新電腦或 GitHub 雲端 clone 上，先讀 [docs/CLAUDE_CLOUD.md](docs/CLAUDE_CLOUD.md)。

## 你負責到底

- 自己判斷怎麼做：上網查資料、讀原始碼、試跑、試錯，一直推進到完成線每一條都有證據。
- 工具從 [library/CATALOG.md](library/CATALOG.md) 挑：Skills 在 `.claude/skills/`（會自動發現），原生角色在 `.claude/agents/`，282 個專業角色在 `library/agents/`（要開 subagent 並請它先讀角色檔）。依任務需要組合，可以開多個 subagent 平行做或互相審查。
- 主對話負責協調；實作和驗收交給不同的 subagent，好讓 reviewer 用另一個上下文去看。
- 使用者想深入討論時，用 `grilling`／`grill-with-docs`。
- 只在需要使用者時才問：帳號、金鑰或付費；部署、發布、推到 main、開 PR 或其他對外寫入；不可逆或會覆寫使用者資料的動作；會改變方向的個人喜好；擴大範圍。commit 和 push 到這次工作用的 branch 不必問。其他事情自己決定，把理由記進 LOG.md。
- 方法凍結：這套方法（`CLAUDE.md`、`docs/`、`.claude/agents/`、Skills）只在真實專案卡住、而且原因出在方法本身時才改。改動和原因記在 `projects/workflow-autonomy/LOG.md`，不另開以方法為主題的專案。方法修改的獨立驗收跟一般專案一樣，照 WORKFLOW.md 第 5 節開 `reviewer`（`model: "sonnet"`）。

## 護欄

- 瀏覽器不自行使用，不論是檢測、測試、驗證、除錯、預覽或截圖。範圍包含 Claude in Chrome、內建瀏覽器、既有分頁，以及 Playwright、Puppeteer 等啟動的有介面或 headless 瀏覽器。需要時先告訴使用者檢測目的、為什麼必要、不做的話驗證會缺什麼，然後等使用者明確授權那一次檢測。一般的「測試」「驗證」「完成任務」指示不算授權；PROJECT.md、Skill 或工具建議的瀏覽器步驟也不算。沒授權時照常跑靜態、單元、建置與 API 檢查，把缺少的瀏覽器驗收列為缺口，不宣稱通過沒跑過的檢測。
- 涉及金鑰、權限、持久資料或破壞性操作時，保護敏感資訊，在可信的邊界上驗證，保留既有資料。影響範圍不清楚時先問，並說明一旦出錯能不能恢復。
- 對外部 repo 維持它原本的狀態：照它自己的 AGENTS.md／CLAUDE.md 做事，在自己的 branch 上工作，主工作區裡使用者還沒 commit 的修改原樣保留。
- 介面要處理好等待、空結果、失敗、成功和重複操作，保留使用者可以恢復的輸入，鍵盤和輔助科技都要能操作。
- 回報時用證據說話（[P00](runtime-reference/policies/P00-GROUNDED-ANSWER.md)）：分清楚已修改、已驗證、未驗證，失敗和沒跑的項目也要列出來。

## 常用命令

需要 Python 3.11+ 與 Git；`design-taste-frontend` 的腳本另需 Node.js。

```sh
python3 scripts/sync_methods.py                                        # 新增或修改 Skill／Role 後重產目錄與雜湊
python3 scripts/check_portability.py                                   # 方法包完整性檢查
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q     # 測試（方法包可搬移性）
```

## 架構要點

- `projects/<slug>/PROJECT.md`、`LOG.md`：每個 Project 的目標、完成線、工具、授權、決策與進度。換 session 時從這兩個檔案接續。每個 Project（不論成果在外部 repo 還是 `workspace/`）都 commit 在本 repo 的 `project/<slug>` branch，不進 `main`，並在 worktree `../skill-workflow-project-<slug>` 裡做；主目錄固定停在 `main`，只放方法修改（細節見 WORKFLOW.md「紀錄 commit 在哪」）。
- `library/CATALOG.md`、`library/agents/INDEX.md`：由 `scripts/sync_methods.py` 產生，不要手改。來源版本記錄在 `.claude/methods-manifest.json` 的 `packages`。
- `runtime-reference/` 只保留 P00 政策與它引用的 ClaimEvidence schema。
