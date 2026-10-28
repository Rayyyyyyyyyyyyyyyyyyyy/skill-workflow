# 下一個工作階段從這裡開始

這個 folder 是 Project 集合：收到想法後建立或接續 Project，依成熟度選 Flow，由 Agent 按 Playbook／Role／Skills 做事，以固定版本 Proof 驗收，保存並接續。Python／本機 Git 管理正式紀錄；CLI 不自行理解自然語言、呼叫模型或在背景常駐。

## 接手版本與入口

上游 `workflow-hub/build` 已由 `/root/independent_review` 第二輪 11 項 PASS，controller 已接受：

- Commit：`d75e09c36a945c6d82d4b59de2f6365f1743367c`；tree：`8980fffa679aad0b3a3a45d304859289fa425731`。
- Submission：`c9a51be8d5856c0e13e1eef5f5deed77f88456cdfc3f63a4f95b18bf1f555339`。
- 接受所據 Review：`6a2e324f59437f81bb26501b1b58a8c10886cf06d98d15e6198507dee800f6ea`。

固定入口是該 build 內的 [AGENTS.md](../../../AGENTS.md)、[WORKFLOW.md](../../../docs/WORKFLOW.md)、[共用契約](../../../library/README.md)與 [roles.json](../../../library/roles.json)。先讀這些入口，不恢復已刪除的 `workflow-mvp`。私有版本庫是原 root 的 `projects/workflow-hub/.workflow/git`；以指定 commit 為準，不以來源舊 HEAD 或作者可變分支替代。

## 開始新想法或接續 Project

原集合根目錄是 `/Users/ray.shao/workflow`。即使身在 task worktree，控制命令始終指向原入口：

```sh
WORKBENCH_ROOT=/Users/ray.shao/workflow
PYTHONDONTWRITEBYTECODE=1 python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" --help
PYTHONDONTWRITEBYTECODE=1 python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" status workflow-hub
```

你可直接說「我想做……」或「接續某專案，先看上次停在哪裡」。Agent／可信控制者依六步操作：

1. 先 `list`；既有目標用 `status <slug>` 接續，新目標才 `new <slug> --idea "原始想法"`，同名不覆寫。
2. 交付、驗收與關鍵決策足夠就直接 deliver；缺方向決策用 clarify、缺事實用 research、設計不足用 design。保存選路理由；原型是釐清／設計內有界方法。
3. 按 WORKFLOW 的 JSON 範例 `plan`，固定 requirements、依賴、每 task 的 `allowed_paths`、驗收與來源；由不同於 planner／contributors 的 Agent 寫實際完整性查核證據，才 `approve-plan`。
4. `dispatch` 登記真實 host 作者 ID；讀 packet 完整 Role、Skills、支援來源、P00、Playbook 與固定輸入，在自己的工作樹執行。
5. 控制者確認作者停止才 `submit --stopped`；另一位非作者／contributor 以 `review-start` 逐項查全部 acceptance（含 `PB-`），以實際證據 `review`，由 `accept` 判定。
6. 受阻先存 Checkpoint、原因與下一步；全部必要成果接受、完成必要整合及安全 `apply` 後，Project 才能 DONE。以上變更命令是下次工作的操作方式，本 handoff 作者未執行。

## 六份 Playbooks、七個 Roles

| Playbook | Role／原生角色 | 配置 Skills |
|---|---|---|
| clarify | planner／Product Manager | grilling、domain-modeling |
| research | researcher／Research Synthesist | research |
| design | designer／UI Designer | UI UX Pro Max、Design Taste |
| deliver（工程） | implementer／Minimal Change Engineer | ponytail |
| deliver（文件） | writer／Technical Writer | humanizer |
| integrate | integrator／Git Workflow Master | 無額外 Skill |
| review | reviewer／Code Reviewer | 無額外 Skill |

Playbook 是工作／交接契約，Role 承擔專業責任，Skill 提供方法，皆不核發發布或派工權。設定及最低 criteria 見 [library](../../../library/)；實際原生 TOML／Skills／支援檔案在准入時封存內容與雜湊。缺來源就保存缺口，不假稱已載入。

## 工作區、Git 與 Proof

`packet.controller_root` 是控制入口，`source_workspace` 是輸入／安全回寫目錄，`workspace` 是當次作者或 Reviewer 的隔離 worktree。`--file` 相對命令呼叫目錄；准入證據相對 source，作者 `--files` 相對作者 worktree，Review `evidence` 相對 Reviewer worktree。不要直接跑工作樹裡的入口副本，也不在 source 共用目錄寫作者成果。

每 task／Attempt 使用獨立 `codex/` branch/worktree，無依賴者可並行。baseline 取當前選定來源 bytes，含未追蹤新檔；已刪檔不從舊 HEAD 復活，來源 HEAD／index／既有修改不 reset、不 stash、不 stage。Submission 固定 base／commit／tree／changed_paths 與產物雜湊；Reviewer 在該 commit 的 detached worktree 檢查整份差異。

多分支交付明列 integrate task，只整合已接受 commits，組合後重新測試與獨立 Proof。Proof 逐項確認證據有效、契約符合及原始目標達成；缺件判 FAIL，工具／環境阻擋才 UNKNOWN。最後 `apply` 預檢 baseline／目標內容後回寫允許差異，來源途中改變就等待，不覆蓋。

## 保存與恢復

先查 status 的 task、reason、Attempt、round、accepted inputs 與 Checkpoint，不直接改 SQLite。

| 狀態／原因 | 下一步 |
|---|---|
| `PLANNING`／`PLAN_REWORK_REQUIRED` | 查准入缺陷，修訂未開工計畫後獨立查核；累計兩次 FAIL 成 `PLAN_ALIGNMENT_REQUIRED` 等待對齊 |
| `RUNNING`／`AWAITING_REVIEW` | 核對真實 host 狀態；前者暫停先 Checkpoint，後者接續指定 submission，不重跑作者 |
| `REVIEW_BLOCKED` | 同 review／版本在原重試額度內恢復，保留已知 FAIL，不暗中換件 |
| `GIT_MERGE_CONFLICT` | 保留整合 worktree，解衝突並 stage 後 resume，同 Attempt 接續；不覆寫 source |
| `GOAL_ALIGNMENT_REQUIRED`／`DELIVERY_PLAN_REQUIRED` | 前者第二輪仍有缺陷，不能第三輪；後者 prepare 已接受，需承接固定輸入安排 deliver |
| `SOURCE_APPLY_REQUIRED`／`SOURCE_CHANGED` | 查 accepted leaf 與來源差異，安全回寫前不 DONE；來源改動不得強制覆蓋 |

每 plan 最多 32 tasks；每 task 兩輪驗收、最多兩次查核恢復、最多四次作者 Attempt。重啟、換 Agent、pause／resume 不歸零。`--stopped` 只由可信控制者依 host 真正停止訊號登記。終態不被晚到報告重啟，取消不撤回已發生效果。

## 證據、限制與此刻下一步

本 writer 已讀固定 Technical Writer／humanizer／P00／deliver 契約與 REQUEST／DESIGN，核對 43 份上游檔案雜湊，並讀正式接受的 Review 與封存證據，而非僅轉述作者摘要：

- Root 的 [48 案 log](test-output-v2.txt)通過；獨立 Reviewer 對 `d75e09…` 再跑同 48 案通過（19.909 秒），不相加成 96 案。原 40 案保留，新 8 案覆蓋 Git 隔離、整合、衝突、固定 Review、安全回寫及 legacy 接續。
- Reviewer 另驗三案：衝突同 Attempt 接續、第一輪 FAIL 從固定前版補件、prepare commit／receipt 承接。Git／來源保全見 [整合紀錄](git-integration-v2.json)、[回寫紀錄](source-apply-v2.json)與 [驗證說明](VALIDATION-v2.md)；檔內待審查文字是歷史，接受以本頁 receipt／controller 為準。
- 獨立證據在原 Project `.workflow/blobs/`；status 的 `tasks.build.review.report` 可查雜湊。48 案 log blob 為 `e2391348b7acf4e51d1ee1ad0f53ee7a6cf57b7119bb047394566d232e90fe24`，三案定點 blob 為 `bebce39451ff44f5829e4c4bcfc503ece939237cc03e5b69aa07ef785bc2bb5a`。

本版是可信本機協作，不提供同 OS 惡意 Worker 隔離或身分認證；apply 是全目標預檢後逐檔替換，不是多檔交易，不應與外部 writer 並行回寫，中斷須核對現場。備份須含控制庫、私有 Git 與 blobs。未驗證／不支援：全部原規格 23 案、各領域普遍品質、瀏覽器、發布／部署／付費、精確費用上限、跨主機恢復；舊參考 41 案不與新版相加。

撰寫時只讀查詢為 build=DONE、handoff=RUNNING（Attempt `a313617b05b246d0b0f6e88309479a35`，round 0）、Project=RUNNING；之後一律重新查 status。此檔未驗收，不宣告 handoff 或 Project 完成。本 writer 只做雜湊、`--help`／`status` 與本機連結檢查，未重跑 suite、未開瀏覽器、未 submit／review／accept／apply。下一步由 controller 封存此檔，未參與撰寫的 Reviewer 查全部 5 項 acceptance，接受後才處理最後安全回寫。
