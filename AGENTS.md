# Project 工作入口

這個 repo 收納使用者的 Projects，也放共用的工作方法。使用者丟進來的可能是目標、方向，或天馬行空的種子；你負責推進到完成。收到想法、要接續專案或要回報進度時，先讀 [docs/WORKFLOW.md](docs/WORKFLOW.md)。

## 你負責到底

- 自己判斷怎麼做：上網查資料、讀原始碼、試跑、試錯，一直推進到完成線每一條都有證據。
- 工具從 [library/CATALOG.md](library/CATALOG.md) 挑：Skills 在 `.claude/skills/`，原生角色在 `.claude/agents/`，282 個專業角色在 `library/agents/`。依任務需要組合，可以開多個 subagent 平行做或互相審查。
- 只在需要使用者時才問：帳號、金鑰或付費；部署、發布、推到 main、開 PR 或其他對外寫入；不可逆或會覆寫使用者資料的動作；會改變方向的個人喜好；擴大範圍。commit 和 push 到這次工作用的 branch 不必問。其他事情自己決定，把理由記進 LOG.md。

## 護欄

- 瀏覽器（包含 headless、Playwright、Puppeteer）只在使用者授權後才使用：可以在當次對話授權，或在該專案 PROJECT.md 的「授權」欄記下使用者的原話、日期與出處。這一欄只能記使用者說過的話，Agent 不能自己填。授權範圍寫明是哪個專案、做什麼用。還沒授權時，先跑靜態、單元、建置與 API 檢查，並把缺少的瀏覽器驗收列為缺口。
- 涉及金鑰、權限、持久資料或破壞性操作時，保護敏感資訊，在可信的邊界上驗證，保留既有資料。影響範圍不清楚時先問，並說明一旦出錯能不能恢復。
- 對外部 repo 維持它原本的狀態：照它自己的 AGENTS.md 做事，在自己的 branch 上工作，主工作區裡使用者還沒 commit 的修改原樣保留。
- 介面要處理好等待、空結果、失敗、成功和重複操作，保留使用者可以恢復的輸入，鍵盤和輔助科技都要能操作。
- 回報時用證據說話（[P00](runtime-reference/policies/P00-GROUNDED-ANSWER.md)）：分清楚已修改、已驗證、未驗證，失敗和沒跑的項目也要列出來。

## 換環境

Claude 從 `CLAUDE.md` 進入；在 GitHub 雲端或新電腦上，先讀 [docs/CLAUDE_CLOUD.md](docs/CLAUDE_CLOUD.md)。工作進度存在每個 Project 的 `PROJECT.md` 和 `LOG.md`，換 session 時從那裡接續。

新增或修改 Skill／Role 之後，跑 `python3 scripts/sync_methods.py` 更新目錄和雜湊，再跑 `python3 scripts/check_portability.py` 確認。

`workbench.py` 是可選的嚴格控制程式（[docs/WORKBENCH.md](docs/WORKBENCH.md)），只在使用者要求逐版控管時使用。`docs/playbook/` 和 `runtime-reference/` 是設計參考。
