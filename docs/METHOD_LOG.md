# 方法修改紀錄

## 2026-11-08
- 讀了 WORKFLOW、AGENTS、roles.json、playbooks 和 projects/ 的所有紀錄，找出跟使用者理想不合的地方（見 PROJECT.md「診斷」）。
- 從上游 clone 固定版本：mattpocock/skills@59db609、agency-agents@4e3ac3c、impeccable@924bbd1。複製 15 份 Matt Skill（各附 LICENSE）、impeccable，以及 282 個 agency 角色到 `library/agents/`。282 這個數字跟原電腦盤點記錄的數量相同。
- 新增 `scripts/sync_methods.py`，用來產生 CATALOG／INDEX 並重算 manifest 雜湊；`check_portability.py` 加上目錄同步檢查。
- 改寫 WORKFLOW、AGENTS、CLAUDE、CLAUDE_CLOUD、README、library/README；舊流程搬到 docs/WORKBENCH.md。7 個原生角色的開頭說明改成不綁 workbench。
- 驗證：`check_portability.py` PASS；`unittest` 51 項全部 OK。
- 已確認：Claude Code 在本 session 自動發現了新加入的 Skills（系統列出 code-review、tdd、impeccable 等）。
- 未驗證：impeccable 的 launcher 下載 engine（沒有執行）；agency 角色由 subagent 讀檔使用的實際效果（還沒在真實專案上跑過）。
- 獨立 reviewer（另一個上下文）驗收 `8579001`：C1–C5 PASS，C6 PASS 但附 4 項必修。282 個角色檔、15 份 Matt Skill、impeccable 都和上游逐 byte 相同。
- 修正 4 項必修：
  - 12 份 `disable-model-invocation` 的 Skill 在目錄標成「讀檔」，WORKFLOW 寫明這類 Skill 直接讀 SKILL.md。
  - 新增 `docs/agents/`（本機 Markdown tracker，票放 `projects/<slug>/`），Matt 工程系列不必再跑 setup，也不會建立 GitHub issue。
  - push 規則寫清楚：推到這次的工作 branch 不必問；推到 main、開 PR、推到別人的 repo 要先問。
  - PROJECT.md「授權」欄只能記使用者原話、日期與出處。
- 一併採納的建議：卡關定義統一成「同一個問題換三種做法都沒進展」；種子模式提概念時一起附完成線，使用者只要選一次；使用者要深入討論時以 grilling 節奏為準；補上網路被擋時的處理方式；補上舊專案怎麼轉成新格式。
- 沒採納：sync_methods 的測試、收錄 agency 的 strategy/、還原上游完整版 ask-matt，這幾項留作後續。
- 驗證：check_portability PASS；unittest OK。

## 2026-11-09
- 查證：arxiv、claude-design、ideation、plan、sketch 等 11 個 Skill 只存在 `~/.codex/skills/`、它的備份，以及 `~/Documents/Codex/2026-06-27/sli/work/local-skills/`，不在 `~/.claude/skills/`，也不在 Claude 帳號的 Skill 清單裡。判斷是 Codex 工作時自建的，不是 Claude 內建。
- 依使用者決定刪除 Codex 相關內容：
  - 刪掉 `docs/CLAUDE_SKILLS_INSTALL.md`（剩下的內容只有那 11 份待搬清單和 Codex 排除工具）。
  - CLAUDE_CLOUD 的待搬清單改成「新增 Skill 或角色」的通用做法。
  - WORKBENCH.md 和 workbench.py 的說明不再提 Codex。
- 保留不動：
  - `library/git_tasks.py` 的 `codex/` branch 前綴。改名的話，原電腦上既有的 workbench task branch 就接不上了。
  - `projects/` 底下的歷史紀錄，以及 `docs/playbook/` 的設計稿。
- 驗證：check_portability PASS；unittest OK。

## 2026-11-11 repo 審查後的調整（branch `ft/workflow-cleanup`）
- reviewer 角色內文改成純驗收者：逐條 PASS／FAIL／UNKNOWN、證據親自取得、不改成果。原因：上游 Code Reviewer 人設要求「建議不要求、稱讚、鼓勵」，跟逐票驗收相反。
- `docs/agents/issue-tracker.md` 加本 repo 例外：不做 to-tickets 的使用者核准輪、票必須寫成檔案、必填 Scope／Out of scope／Verify。原因：repo 裡沒有任何 `projects/*/issues/`，票只存在對話裡。
- `docs/WORKFLOW.md` 明確度關卡加上零 context 檢查（一批票派工前，全新 subagent 只讀票檔，回報哪裡必須猜）。來源：Dave Rensin 的 Elephant-Goldfish Model。
- README「怎麼用」補上範例。
- 使用者決定刪掉 workbench：移除程式、文件、playbooks、roles.json、git_tasks.py、`runtime-reference/config/` 與對應測試；七個角色前言不再提 dispatch packet；四個舊專案的接續指令改成指向 `records/`。`check_portability.py` 不再讀 roles.json。
- 驗證：check_portability PASS；unittest 3 個測試 OK。
- 未驗證：新的 reviewer 與零 context 檢查還沒在真實票上跑過。
- 還沒決定：`~/.claude/agents/` 的 286 個全域角色、全域與專案兩套瀏覽器規則以哪一套為準。

## 2026-11-11 重新確定目標，照目標模式執行 G1–G5
- 做了什麼：目標原文寫進 PROJECT.md 與 README；WORKFLOW 第 6 節加上收尾要記的兩個數字；CLAUDE.md 加方法凍結規則；工具庫不動。commit `1eca1b2`。
- 獨立驗收：全新 sonnet subagent 先讀新版 `.claude/agents/reviewer.md` 再驗收，G1–G5 共 5 條 PASS、0 FAIL、0 UNKNOWN，每條附它自己跑的指令與輸出。這是新 reviewer 角色第一次實際使用；驗收者回報角色說明沒有需要猜的地方。
- 驗收者註記：G5 的 grep 依條件排除了 `skills/`。主 session 先前查過，該目錄裡的 "workbench" 只出現在字型名稱與網站描述文字，跟被刪的程式無關。
- 未驗證：零 context 的票檔檢查還沒在真實票上跑過；新 reviewer 還沒驗過程式碼類的票。
- 收尾數字：使用者被問 3 次（審查後問是否動手、刪除 workbench 後問 push 與 integrator、重新確定目標時問三項決定）；獨立驗收 FAIL 0 輪。
- 下一步：等使用者決定 push 與併回 main。

## 2026-11-11 瀏覽器規則改為每次授權；併回 main
- 使用者決定以全域版為準：`CLAUDE.md` 護欄、`docs/WORKFLOW.md` 的「驗」與 PROJECT.md 格式都改成「每次檢測當次授權，專案文件不算授權」。既有專案 PROJECT.md 裡記過的瀏覽器授權從此不再有效。
- 使用者指示 push `ft/workflow-cleanup` 並併回 main。
- 驗證：check_portability PASS；unittest OK。

## 2026-11-11 刪除 integrator 與全域重複角色
- 刪除 `.claude/agents/integrator.md` 與 manifest 的來源紀錄；README 的原生角色數改為 6。
- 使用者電腦的 `~/.claude/agents/`：刪除前逐檔比對，282 個與 `library/agents/` 逐位元相同才刪；剩 4 個 `impeccable-*`。要還原就從 `library/agents/` 複製回去。
- 驗證：check_portability PASS；unittest OK；sync 輸出 6 native roles。

## 2026-11-11 刪除已結案專案；補裝 implement-spec、retro、pr
- 使用者指示：舊專案都已結案，刪掉。移除 `projects/` 下 8 個資料夾（book-notes、book-reader-mobile、book-reader-ux、claude-cloud-portability、skill-install-handoff、skills-inventory、winter-ux-motion、workflow-hub），只留 workflow-autonomy。要找回就從 git 歷史（`c185aec` 之前）取。
- 使用者指示補裝 `implement-spec`、`retro`、`pr`：取自 mattpocock/skills 與既有 Matt skills 相同的 commit `59db609`，內容未改；同時複製到 `~/.claude/skills/`。
- 已知殘留：manifest 裡 ponytail 的 `fixed_evidence.path` 指向已刪的 `projects/claude-cloud-portability/records/package-review-v1.md`，該檔可從 `review_commit` `b9c7e23` 取回。
- 驗證：sync 輸出 29 skills；check_portability PASS；unittest OK。
- 未驗證：三個新 Skill 還沒實際跑過。

## 2026-11-12 外部 repo 專案的紀錄改放 `project/<slug>` branch
- 起因：template-upgrade 的紀錄被 commit 到本 repo `main`（3 個本機 commit，未 push）。使用者：「但那跟skill-workflow這個repo本體沒有關係呀 只是利用了方法工具，但更新的目標repo另有其他 要push也是另開branch」，並要求「不只要在記憶，也要更新在workflow的方法步驟裡」。
- 處理：3 個 commit 移到本機 branch `project/template-upgrade`，`main` 退回 `origin/main`（`4161ce1`）。
- 方法修改：`docs/WORKFLOW.md` 接案第 1 步加看 `project/*` branch，新增「紀錄 commit 在哪」；`docs/CLAUDE_CLOUD.md` 外部 repo 與保存兩段、`CLAUDE.md` 架構要點同步。

## 2026-11-13 主目錄固定停在 main，專案紀錄改用 worktree
- 起因：主目錄停在 `project/template-upgrade`，使用者每次想改 main 都得特別說要隔離。使用者同意改成 worktree，並等 template-upgrade 結束才執行。
- 處理：template-upgrade 已完成並 push（`project/template-upgrade` 的 `94f7c8a`），主目錄切回 `main`。
- 方法修改：`docs/WORKFLOW.md`「紀錄 commit 在哪」改成外部專案紀錄在 `../skill-workflow-project-<slug>` worktree 做；主目錄只放方法修改，可直接 commit，push 前先問。`CLAUDE.md` 架構要點同步。`docs/CLAUDE_CLOUD.md` 不改，因為雲端 session 每次都是新 clone，直接切 branch 就好。
- 補充（同日）：使用者同意把規則擴大到所有 Project，成果放在 `workspace/` 的也一樣，一律走 `project/<slug>` worktree，main 只放方法。WORKFLOW.md、CLAUDE.md 同步修改。
- 檢查 main 是否只放方法：刪掉 `.gitattributes`，它唯一的規則指向已刪除的 `projects/skills-inventory`。
- 刪除遠端 branch：`chore/merge-entry-cleanup`、`ft/workflow-cleanup`、`claude/inspiring-feynman-ied4yc`（三個都已全部進 main）。另依使用者指示放棄 nihongo-dojo-ios-app，刪除 `claude/nhk-n3-1-app-design-48gcth`（最後一個 commit 是 `a4ff394`，紀錄沒有進 main；外部 repo `nihongo-dojo-app` 沒動）。
- 依使用者指示刪除 `project/template-upgrade`（最後一個 commit 是 `94f7c8a`，只有 `projects/template-upgrade/` 的紀錄；程式碼在 `Rayyyyyyyyyyyyyyyyyyyy/template`）。規則補充：專案結束後刪掉 worktree 和 `project/<slug>` branch，最後一個 commit 記在這裡。

## 2026-11-13 依 Rieseberg〈How to be more ambitious〉補強完成線與驗收
- 起因：使用者以 `/goal` 指示「去找出這文章的全文，與實作方式，來優化更新現在這個 repo 裡面的方法」。這不是真實專案卡住，而是使用者明確要求，所以覆蓋方法凍結。
- 來源：原文 felixrieseberg.com（2026-10-13）與社群 Skill `robonuggets/be-ambitious`；重點和對照表在 `docs/references/rieseberg-ambition.md`。
- 方法修改（`docs/WORKFLOW.md`）：第 2 節完成線寫結果不寫做法，每條都要有外部判準，並用四問挖深；第 3 節角色庫要用方法和工具、不只換口吻，新增跨領域的「名詞改成動詞」與紅隊；第 4 節進迴圈前先接好驗證用的基礎建設；第 5 節與 `.claude/agents/reviewer.md`：reviewer 照外部判準重跑取證，不能用實作者的回報代替，「使用者判定」的判 UNKNOWN 並列入「已完成但未驗證」；PROJECT.md 完成線格式改成寫外部判準。`scripts/sync_methods.py` 的角色用法說明同步修改，並重新產生 `library/CATALOG.md` 與 `.claude/methods-manifest.json` 的雜湊。
- 沒有採用：「訂不合理的目標」（與「範圍擴大先問」相衝）；不安裝 be-ambitious Skill（規則已寫進 WORKFLOW，不多一個要維護的外部依賴）。
- 待觀察：下一個專案收尾時，看外部判準是否讓驗收 FAIL 的輪數或 UNKNOWN 變多，以及問使用者的次數有沒有增加。
- 獨立驗收（使用者指定 Fable 5.2）第 1 輪：3 PASS、2 FAIL。FAIL 1：WORKFLOW 第 5 節與 `.claude/agents/reviewer.md` 的證據標準不一致。FAIL 2：多處要執行者猜，包括往上一層算不算擴大範圍、「使用者判定」怎麼結案、「重要」沒有判準、沒切票時的第一張票、瀏覽器授權、四問 (1)–(3) 寫在哪。已逐項修正：範圍以使用者原話為界，往上一層的版本當選項問使用者；「使用者判定」判 UNKNOWN，列入「已完成但未驗證」；跨領域改成在方向／種子模式與第二種做法失敗時使用；reviewer.md 同步。
- 第 2 輪：4 PASS、1 FAIL。FAIL 是 LOG 還寫著第 1 輪的舊說法，已改正。順便補上殘留的含糊處：問了往上一層的選項後，等回覆期間先照原話範圍的完成線做。這兩處修改沒有再送第 3 輪，以 grep 和下列檢查確認。
- 驗證：sync_methods、check_portability PASS；unittest OK。

## 2026-11-13 方法修改改由 Fable 驗收
- 使用者指示：「用fable 只限於做把關推進workflow方法的優化迭代」。`CLAUDE.md`「方法凍結」那一條補上：方法修改的獨立驗收用 `reviewer` 加 `model: "fable"`，一般專案照舊用 sonnet。

## 2026-11-13 檢驗方法：同名 Skill 被全域版蓋掉；補記專案收尾數字
- 起因：使用者以 `/ask-matt 檢驗repo的方法` 要求檢驗，之後指示「第1點和第2點都修 也檢查其他」。方法凍結由使用者明確要求覆蓋。
- 發現 1：`/ask-matt` 載入的是 `~/.claude/skills/ask-matt`（Matt 原版），不是 repo 版。個人 Skill 會蓋掉同名的專案 Skill。內容不同的有 6 個。處理（都在使用者電腦的全域目錄，不在 repo；原檔備份在 `~/.agents/skill-backups/20261113-shadow-fix/`）：
  - `impeccable`（全域 4.6.0）、`setup-matt-pocock-skills`（全域是較舊的版本）：換成 repo 版，`diff -rq` 確認相同。
  - `ask-matt`、`grill-me`、`grill-with-docs`：repo 版是為這個 repo 改寫的，全域的原版別的 repo 還要用，所以不覆蓋；在全域版 frontmatter 後加一行「repo 有同名 SKILL.md 就改讀 repo 版」。
  - `ui-ux-pro-max`：全域版只差在腳本路徑寫絕對路徑，不必換；但它寫 `python`，這台電腦只有 `python3`，指令會失敗。改成 `python3`，實跑 `search.py` 有輸出。
  - 限制：重新安裝全域 Skill 會把這些修改蓋掉；`check_portability.py` 不檢查 Claude 的 Skill 發現，抓不到。
- 發現 2：template-upgrade 的收尾數字只在已刪除的 `project/template-upgrade`（`94f7c8a`，目前是本機懸空 commit）。補記在這裡：
  - 第 1 輪（票 01–11）：使用者被問 2 次；逐票驗收 FAIL 0 輪，獨立驗收 FAIL 0 輪。
  - 第 2 輪（票 12–31）：使用者被問 0 次；FAIL 輪 2 次（都是票 28）。
  - 第 3 輪（深色首頁）與合併發佈：該專案 LOG 沒有彙整數字；敘述裡有一次逐票 FAIL（票 35，修正後 PASS）。
  - 這些都發生在 11-13 的 Rieseberg 修改之前，可以當那次修改的對照基準。
- 方法修改：`docs/WORKFLOW.md` 第 1 節，刪 branch 時把收尾的兩個數字連同最後一個 commit 記到這裡。
- 檢查過、沒有改的：
  - `~/.claude/agents/` 現在有 287 個檔：4 個是 `impeccable-*`（10-19 寫入，11-11 刪除時留下的）；另外 283 個角色檔是 11-11 13:54–13:55 寫入的，晚於同日的刪除，其中 272 個與 `library/agents/` 同名檔相同、10 個不同、`engineering-electrical-engineer.md` 不在 library。來源不明，等使用者決定。
  - 6 個原生角色的 frontmatter 與 WORKFLOW 一致（只有 implementer 指定 `model: sonnet`）；`reviewer.md` 與 WORKFLOW 第 5 節的證據標準一致。
  - `library/agents/` 282 個角色檔加 INDEX；方法文件 68 個檔的相對連結 0 個失效。
  - 仍未處理：manifest 裡 ponytail 的 `fixed_evidence.path` 指向已刪的檔案；`implement-spec`、`retro`、`pr` 還沒實際跑過。

## 2026-11-13 方法修改的驗收改回 sonnet
- 使用者指示：「拿掉fable modal的調用好了，統一原本回到的review流程」。`CLAUDE.md`「方法凍結」那一條改成：方法修改的獨立驗收照 WORKFLOW.md 第 5 節開 `reviewer`（`model: "sonnet"`），不再用 Fable。同日稍早「方法修改改由 Fable 驗收」那一節作廢。
- 上一節（同名 Skill、收尾數字，`81a7c66`）的 Fable 驗收在這個指示之前已送出並跑完：6 PASS、1 FAIL。FAIL 是上一節對 `~/.claude/agents/` 的描述不精確（把 4 個 `impeccable-*` 也算成 11-11 寫入的角色檔），已改正。同時依它的備註補上第 3 輪票 35 的逐票 FAIL，並在全域三個 Skill 的轉向那一行註明路徑從 repo 根目錄算。這些修正和本節的 `CLAUDE.md` 修改改送 sonnet reviewer。
- sonnet reviewer 驗收 `41e2b34`、`6f1a162`：5 PASS、0 FAIL、0 UNKNOWN。

## 2026-11-13 reviewer 的模型比執行者高一級
- 使用者指示：「review 的agent modal 要用比執行的agent modal更高級」。上一節「驗收改回 sonnet」由這一節取代；Fable 仍然不用。
- 方法修改：`.claude/agents/reviewer.md` frontmatter 加 `model: opus`（implementer 維持 `model: sonnet`）；`docs/WORKFLOW.md` 切細派工開頭、逐票驗收、第 5 節寫明規則；`CLAUDE.md`「方法凍結」那一條改成照第 5 節。明確度關卡的 subagent 維持 sonnet，因為它模擬的是執行者會不會需要猜。
- Agent 判斷：主 session 自己動手的修改也用預設的 opus。主 session 跑在比 opus 更高的模型時，這種情況 reviewer 不會比執行者高；照規則要嚴格成立，就把修改切票交給 implementer 做。
- opus reviewer 驗收 `945599b` 第 1 輪：4 PASS、1 FAIL。FAIL：執行者是 opus 時文件沒說 reviewer 用什麼，主 session 自己動手的例外也沒說原因。已改寫第 5 節：opus 是上限，執行者是 opus 或主 session 自己動手時 reviewer 都用 opus，靠獨立的上下文。
- 第 2 輪（`355874f`）：3 PASS、0 FAIL、0 UNKNOWN。使用者指示「調整完再push」，push 到 `origin/main`。

## 2026-11-13 專業角色只留全域那份
- 使用者決定：「只留全域的那份，也用全域的方法，在readme裡面增加handoff需要另外安裝的的list 先preview有哪些role會比較常用到」。這推翻 11-08 的 Agent 判斷（角色放 `library/agents/` 以免每輪佔 context）與 11-11 的「全域角色刪掉」；代價是每個 session 的 subagent 清單多約 290 筆說明。
- 查到全域角色又出現的原因：使用者電腦裝了 Agency Agents 桌面 app（`/Applications/Agency Agents.app`），它會自動安裝並更新 `~/.claude/agents/`。
- 方法修改：刪除 `library/agents/`（282 個角色、INDEX、LICENSE；要找回從 `e943880` 取）。WORKFLOW 第 3 節、`CLAUDE.md`、`docs/CLAUDE_CLOUD.md`、`library/README.md` 改成：專業角色直接用 subagent 類型清單上的名稱開，不讀檔；清單上沒有就照 README 安裝，裝不了只用原生角色。README 新增「另外安裝」：安裝方式、沒裝的影響、12 個常用角色（依過去專案類型推估，沒有使用紀錄）。`sync_methods.py` 不再產生 INDEX；`check_portability.py` 印出全域角色數量，沒裝不算失敗。manifest 的 agency-agents 來源改註明裝在全域。
- `.claude/agents/LICENSE` 保留，6 個原生角色改寫自 agency-agents。
- opus reviewer 驗收 `7cf535d`：5 PASS、0 FAIL、0 UNKNOWN。順手修掉它指出的格式瑕疵（`sync_methods.py` 多一行空行）。未驗：雲端或新電腦上實際開專業角色。

## 2026-11-13 方法紀錄搬到 docs/METHOD_LOG.md
- 原本放在 `projects/workflow-autonomy/LOG.md`。專案已結案，`PROJECT.md` 刪除（內容可用 `git show 035fdb7^:projects/workflow-autonomy/PROJECT.md` 取回）。
- 原因：`projects/<slug>/` 依 WORKFLOW.md 只放在 `project/<slug>` branch，這個資料夾是 `main` 上唯一的例外。搬家後 `main` 上沒有 `projects/`，規則也就沒有例外了。
- 更新了 CLAUDE.md、WORKFLOW.md、`docs/references/rieseberg-ambition.md` 的引用。
