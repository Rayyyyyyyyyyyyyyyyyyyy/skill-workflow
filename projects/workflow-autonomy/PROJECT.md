# workflow-autonomy

## 目前狀態（2026-11-08）
- 模式：方向，已和使用者談定完成線
- 狀態：完成線已交付，等使用者實際試用後回饋
- 成果位置：本 repo，branch `claude/inspiring-feynman-ied4yc`
- 下一步：使用者在真實專案上試用新流程；把原電腦上的 11 個 Skill 資料夾推上來

## 原始想法
> 我最近用workflow用的很不開心
> 這個repo沒有照我的預期運作
> 我的理想是 我訂一個目標或方向或是一個天馬行空的想法
> Agent 自己判斷跟思考該怎麼執行跟完成
> 目標就是要做到
> 方向是可以討論要推進到那裡
> 天馬行空的想法可以問問題收集必要資訊
> 剩下的就是agent自己上網搜尋找資料收集資訊來實作
> 舉證驗證試錯跟推進

> 明明就有這麼多的工具可以用
> 57個skill
> 跟200多個role agent

> 對 這個方向是我要的（回應：把工具帶進 repo、改由 Agent 自選工具、三種輸入、拿掉兩輪上限、workbench 降為可選）

## 診斷（2026-11-08，依 repo 紀錄）
- 四個實際專案（book-notes、book-reader-ux、book-reader-mobile、winter-ux-motion）都沒走 workbench 正式流程，因為成果在外部 repo；完整走完流程的只有建這套系統本身的 workflow-hub。
- `library/roles.json` 固定 7 個角色、10 個 Skill；准入時要鎖定雜湊，所以做到一半沒辦法加工具。
- 兩輪審查失敗或兩次准入失敗就停下來等使用者，跟「目標就是要做到」相反。
- skills-inventory 和 skill-install-handoff 只做了盤點，沒有安裝任何東西。

## 完成線
- [x] C1 Matt 系列缺的 15 份 Skill、impeccable、agency-agents 282 個角色都進 repo，固定上游 commit，附上 LICENSE
- [x] C2 有工具目錄（`library/CATALOG.md`、`library/agents/INDEX.md`），可以用腳本重產，`check_portability.py` 會檢查目錄是否同步
- [x] C3 `docs/WORKFLOW.md` 改成三種輸入（目標、方向、種子）＋推進迴圈＋獨立驗收，沒有輪數上限，列清楚什麼時候才問使用者
- [x] C4 `AGENTS.md`、`CLAUDE.md` 改成 Agent 負責到底、自選工具；瀏覽器可以按專案授權一次
- [x] C5 workbench 降為可選（`docs/WORKBENCH.md`），既有測試照常通過

## 工具
- Skills：`writing-for-agents`（改寫 AGENTS.md 和 CLAUDE.md 的寫法準則）
- 角色：`reviewer`（獨立驗收）

## 授權
- 瀏覽器：未授權（這次用不到）
- 對外動作：push 到指定的 branch

## 決策
- 2026-11-08 使用者同意方向：工具全部進 repo、Agent 自選工具、workbench 降為可選，不刪除
- 2026-11-08 Agent 判斷：agency 角色放 `library/agents/`，不放 `.claude/agents/`，因為 282 個原生角色的說明會在每一輪都佔用 context；改成用目錄搜尋，再請 subagent 讀角色檔。如果想要某些常用角色變成原生，可以把它複製到 `.claude/agents/`
- 2026-11-08 Agent 判斷：瀏覽器從「每次授權」改成「當次對話或 PROJECT.md 授權一次」；部署、付費、對外寫入仍然要每次先問
