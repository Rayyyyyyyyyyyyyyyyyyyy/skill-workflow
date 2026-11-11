# workflow-autonomy

## 目前狀態（2026-11-11）
- 模式：目標（2026-11-11 使用者重新確定目標，並指定照目標模式執行）
- 狀態：進行中，G1–G5 待獨立驗收
- 成果位置：本 repo，branch `ft/workflow-cleanup`（worktree `../skill-workflow-ft-workflow-cleanup`），尚未 push
- 下一步：獨立驗收 G1–G5；之後等使用者決定是否 push、併回 main

## 目標（2026-11-11 重新確定）
> 我丟一個目標、方向或種子，Agent 自己推進到完成線每一條都有獨立驗收的證據。我只在帳號、付費、對外寫入、不可逆操作、個人喜好這幾種情況被打擾。這包方法 clone 到任何電腦或雲端都能直接用。

怎麼算成功：看真實專案上使用者被打擾幾次、獨立驗收失敗重做幾輪，不看方法本身多完整。

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

### 第二批（2026-11-11，對應重新確定的目標）
- [ ] G1 目標原文寫進本檔與 README 開頭（驗證：`grep -c "獨立驗收的證據" README.md projects/workflow-autonomy/PROJECT.md` 兩個檔都 ≥1）
- [ ] G2 成功標準可以被記錄：`docs/WORKFLOW.md` 第 6 節規定每個專案收尾時在 LOG.md 記「使用者被問了幾次」與「獨立驗收 FAIL 幾輪」（驗證：`grep -n "被問了幾次" docs/WORKFLOW.md` 有結果，且在第 6 節內）
- [ ] G3 方法凍結規則寫進 `CLAUDE.md`：只在真實專案卡住且原因出在方法時才改，不另開以方法為主題的專案（驗證：`grep -n "方法凍結" CLAUDE.md` 有結果）
- [ ] G4 工具庫維持原狀：26 個 Skill、7 個原生角色、282 個角色庫角色（驗證：`python3 scripts/sync_methods.py` 輸出這三個數字，且執行後 `git status --short` 沒有變動）
- [ ] G5 方法包檢查與測試通過，repo 內（`projects/` 的歷史紀錄除外）沒有殘留的 workbench 引用（驗證：`python3 scripts/check_portability.py` 印出 PASS；`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q` 結果 OK；`grep -rIli workbench --exclude-dir=.git --exclude-dir=projects --exclude-dir=skills .` 沒有輸出）

不在這批完成線內、等使用者決定：push 與併回 main、`~/.claude/agents/` 的 286 個全域角色、瀏覽器規則以哪一套為準、`integrator` 角色去留。

## 工具
- Skills：`writing-for-agents`（改寫 AGENTS.md 和 CLAUDE.md 的寫法準則）
- 角色：`reviewer`（獨立驗收）

## 授權（只記使用者親口說的話）
- 瀏覽器：未授權（這次用不到）
- 對外動作：push 到這次工作用的 branch（session 設定指定的 branch）

## 決策
- 2026-11-08 使用者同意方向：工具全部進 repo、Agent 自選工具、workbench 降為可選，不刪除
- 2026-11-08 Agent 判斷：agency 角色放 `library/agents/`，不放 `.claude/agents/`，因為 282 個原生角色的說明會在每一輪都佔用 context；改成用目錄搜尋，再請 subagent 讀角色檔。如果想要某些常用角色變成原生，可以把它複製到 `.claude/agents/`
- 2026-11-08 Agent 判斷：瀏覽器從「每次授權」改成「當次對話或 PROJECT.md 授權一次」；部署、付費、對外寫入仍然要每次先問
- 2026-11-11 使用者決定（原話「照你建議」「目標也是用goal 來執行」）：採用上面的目標寫法；方法凍結；工具庫維持全部帶著；成功標準用「被問幾次、驗收失敗幾輪」。Agent 解讀：「用 goal 來執行」指照 WORKFLOW 的目標模式，自己寫完成線後直接開工
- 2026-11-11 使用者決定：workbench 刪掉（原話「workbench 刪掉」）。移除 `workbench.py`、`docs/WORKBENCH.md`、`library/playbooks/`、`library/roles.json`、`library/git_tasks.py`、`runtime-reference/config/` 與對應測試；P00 政策與 schema 保留
- 2026-11-09 使用者決定：原電腦上那 11 個 Codex 自建 Skill 不搬，repo 裡跟 Codex 有關的內容刪掉
