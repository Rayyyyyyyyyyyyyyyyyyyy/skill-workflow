# Project 工作流程

這份文件定義當前入口與交接方式。共用 Playbook 定義在 [library](../library/)，專案正式狀態由 `workbench.py` 管理。原 `docs/playbook/` 保留較完整的目標架構；尚未落實的 Runner 隔離及外部操作能力不因本版出現而視為完成。

## 執行模式

現有 Codex 對話／協作 Agent 是實際執行者；可信控制者核對使用者授權、實際 host Agent 身分與停止訊號，再操作本機 Python 命令。`--actor` 與 `--stopped` 是控制者的紀錄，不是外部身分認證或 OS 程序終止機制。

控制程式使用 Python 標準庫與本機 Git，檢查結構、固定 Git 版本、必要證據與依賴；Agent 提供需求理解與語意查核。本版是受信任的本機協作：控制資料與作者同在一個 OS 帳號下，不能宣稱能隔離惡意 Agent。

本版交付研究、設計與本機工程／文件成果。發布、部署、付費及外部寫入不支援；若是使用者要求的必要終點，就保存能力缺口，不將本機成果當成整個目標完成。瀏覽器檢測維持逐次明確授權。

## 一、保存想法並選定 Project

先列出既有 Projects。使用者指定既有專案就接續；只有新目標才建立新 Project。歸屬不明且會影響既有成果時才詢問。

```sh
WORKBENCH_ROOT=/Users/ray.shao/workflow
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" list
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" new csv-export --idea "修正 CSV 空資料匯出漏掉標題列，交付本機可驗收版本"
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" status csv-export
```

Project 名稱是穩定識別。重送、補資料與恢復不靠另建專案解決；名稱碰撞不能覆寫既有資料。原始想法保留，後續釐清另存決策與補充。

專案位於 `projects/<slug>/`。`workspace/` 是一般專案的來源及安全回寫目錄；`.workflow/` 保存正式狀態、來源快照、私有 Git repo、提交與證據。作者只在每次派工提供的獨立 task worktree 工作，不直接修改來源目錄或控制資料。

控制命令一律指向原集合入口。即使 Agent 已進入 task worktree，也不要直接執行該 worktree 裡的 `workbench.py`，否則可能把隔離目錄當成另一個集合。下列命令沿用這個設定，實際值以派工包的 `controller_root` 為準：

```sh
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" status csv-export
```

`packet.controller_root` 是控制命令入口，`packet.source_workspace` 是來源／安全回寫目錄，`packet.workspace` 才是作者或 Reviewer 的隔離工作目錄。`--file` 指向的計畫／報告 JSON 依命令的呼叫目錄解析；准入報告 `evidence` 相對來源目錄，作者的 `--files` 相對作者 worktree，Review 報告的 `evidence` 相對 Reviewer worktree。這些根目錄不能混用。

## 二、依成熟度選路

Agent 先讀原始需求、決策與已有成果。需求足夠時應能說明目標、交付、驗收、限制，以及已確定的方向性決策；保存選路理由後直接前進。

| 情境 | 下一步 | 必須保留的依據 |
|---|---|---|
| 目標、交付與驗收清楚 | 直接安排適用的研究、設計或交付 Playbook | 需求映射；略過前置工作的理由 |
| 缺使用者才能決定的關鍵資訊 | 釐清後保存問題並等待 | 未決問題、方向影響與恢復條件 |
| 缺可查證的事實 | 研究 | 調查問題、來源要求與驗收範圍 |
| 需要具體可操作的答案 | 在適用 Playbook 內做有界原型 | 要回答的問題、原型限制與結論 |
| 既有設計不足以實作 | 設計 | 核心流程、必要狀態與工程接手要求 |
| 沒有適用方法、必要權限或資源 | 保存缺口並等待 | 缺少的能力、所需決策及已保存成果 |

選路是 Agent 的可追查判斷，CLI 不靠關鍵字宣稱理解自然語言。使用者直接提出的想法不受商業價值門檻阻擋；Agent 自行發現的機會不能冒用使用者來源開工，需另有商業評估與採納依據。

## 三、固定 Flow 與准入

Flow 是當次目標的工作計畫。每個作者節點引用一份適用 Playbook；Playbook 的內部階段不預設各自增加 Agent。

准入前要有：

- 原始要求逐項對應驗收條件、驗證方法與證據要求。
- Playbook 的必要驗收項；不能刪減或把必要項改成可選。
- 明確節點、依賴、固定輸入、交付終點及每個 task 的精確 `allowed_paths`；多分支交付明列 integrate 節點。
- Playbook、Role、Skills、實際使用的支援檔案與政策的來源快照，包含內容 Digest。
- 回到原始需求的獨立完整性查核，及有限執行／審查額度。

```sh
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" plan csv-export --file plan.json
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" approve-plan csv-export --file plan-review.json
```

候選計畫先經結構檢查，再由獨立准入查核確認需求覆蓋、前置工作與驗收未弱化。結構合法不證明語意無遺漏。已有明確授權且沒有阻擋缺口時往下做，不要求使用者逐步批准。

Playbook 不呼叫另一份 Playbook，也不自行增加正式工作。新發現的工作只保存為候選提案；控制者評估影響後才改計畫。實質改變目標、範圍或正式驗收，必須保留歷史並重新准入，不能藉此清空輪次或額度。

### 最小計畫格式

以下是另一個簡單需求的格式示例：「依提供的想法寫一份包含目標、限制與下一步的 `brief.md`，交付本機版本」。`planner` 須填當次實際規劃 Agent 的 host ID；若有其他 Agent 參與規劃，將實際 host ID 列入頂層 `contributors`。這份範例不是已執行或已驗收的成果。

```json
{
  "scope": "deliver",
  "planner": "HOST_PLANNER_ID",
  "contributors": [],
  "routing": {
    "maturity": "ready",
    "reason": "原始要求已指定交付內容與檔案，可直接撰寫並逐項驗收",
    "missing_inputs": []
  },
  "operations": ["local"],
  "limits": {"max_rounds": 2, "review_retries": 2, "max_attempts": 4},
  "requirements": [
    {"id": "R1", "text": "brief.md 依原始想法列出目標、限制與下一步，不補造已確認的決策"}
  ],
  "tasks": [
    {
      "id": "write-brief",
      "playbook": "deliver",
      "role": "writer",
      "allowed_paths": ["brief.md", "proof"],
      "supporting_sources": [],
      "depends_on": [],
      "requirement_ids": ["R1"],
      "acceptance": [
        {
          "id": "AC1",
          "description": "brief.md 含目標、限制與下一步，各項內容可追溯至原始想法或明列為假設",
          "method": "Reviewer 對照原始想法逐項閱讀 brief.md，記錄對應位置與缺口",
          "requirement_ids": ["R1"]
        }
      ]
    }
  ]
}
```

`scope: prepare` 用於研究／釐清／設計的準備工作。這些工作全部接受後，Project 仍等待交付計畫，不會把原始交付目標標成 DONE。只有尚未開工的計畫，或已全部完成的 prepare 計畫，才可由 `plan` 接續下一版；已開始的 deliver 計畫不能覆寫或重置。需要實質改變已開始的交付契約時，保留原專案狀態與證據，先處理停止及結束，再建立有來源關聯的新工作。

`routing.missing_inputs` 表示這份計畫本身缺少的關鍵執行輸入，非原始想法的全部未知。模糊目標可先有一份能執行的 prepare／clarify 計畫，將方向性未知列入待釐清交付；若連釐清所需來源也不足，才保留非空 `missing_inputs` 等待，不能批准開工。

每份計畫最多 32 個固定 tasks；`max_rounds` 固定為 2，`review_retries` 是 0–2，`max_attempts` 預設 4 且只能設為 1–4。作者 Attempt 次數依 task 累積，pause／resume、重送、換 actor 都不歸零；耗盡時保留進度等待決策。這些是程式次數上限，不代表精確的 Token 或費用硬上限；host 的實際用量與可用額度仍須由控制者掌握。

Role／Skill 主檔以外，實際使用的參考文件或腳本須在准入前列入 task 的 `supporting_sources`，例如 `{"path": "實際本機路徑", "format": "text"}`。派工會提供其內容快照；不因已釘選 `SKILL.md` 就直接讀取或執行後來變動的支援檔案。所需來源缺漏時保存缺口，不能假稱整套依賴已固定。

計畫存入時，控制程式會附入 Playbook 的最低驗收項，ID 形如 `PB-write-brief-<criterion>`。這些項目和自訂 `AC1` 一起查核；不要自行使用 `PB-` 前綴，也不能只審自己寫的驗收條件。

### 准入查核報告

准入 Reviewer 必須是未參與規劃的另一位 Agent，不能是 `planner` 或頂層 `contributors` 中的任何人。它讀原始想法、候選計畫及必要 Playbooks，確認覆蓋與驗收合理性，寫出實際查核檔。下例示範查出缺口時的報告形狀，`approve-plan` 會拒絕這份 FAIL；只有當次獨立查核實際通過，才以 `status: PASS` 提交。

```json
{
  "plan_hash": "<plan 或 status 輸出的實際 plan_hash>",
  "reviewer": "HOST_PLAN_REVIEWER_ID",
  "status": "FAIL",
  "reason": "示例：原始要求有一項限制尚未被候選計畫覆蓋",
  "evidence": "proof/plan-review.md"
}
```

證據檔須已存在於當次工作區，且包含實際檢查、要求對應及判斷理由。`plan_hash` 必須取自存入後的正式計畫，不能對原始 JSON 自算後沿用；控制程式還會加入來源快照與最低驗收項。缺關鍵輸入時不能批准，保存問題及答案後再修訂未開工計畫。

查核也要排除驗收循環，例如要求「本節點正式接受前，Project 必須已 DONE」會使接受永遠無法成立。重用既有程式、文件或證據時，須固定實際輸入內容與來源快照，不能只附上會變動的路徑；對應文字來源可列入 `supporting_sources`。這些語意問題由獨立 Reviewer 實際查核，程式的結構檢查不代替判斷。

`approve-plan` 收到有效且有實際證據的 FAIL 時，會先封存報告與證據到正式狀態的 `plan_reviews`，累計 `plan_review_failures`，再回傳錯誤；這代表「拒絕准入且缺陷已保存」，不是沒有留下紀錄。同一份 FAIL 報告重送不重複計數。第一次失敗保存為 `WAITING / PLAN_REWORK_REQUIRED`；累計兩次准入失敗後為 `WAITING / PLAN_ALIGNMENT_REQUIRED`，停止自動修訂與准入，等待目標對齊。計數跨重啟及計畫修訂保留，不能用換計畫、換 Agent 或後補 PASS 歸零。准入失敗與交付後的兩輪審查是分開的計數。

### 維護集合本身

一般 Project 省略 `workspace` 即使用專案自己的 `workspace/`。若工作是改造這個 repo，可在計畫頂層加：

```json
{
  "workspace": ".",
  "allowed_paths": ["AGENTS.md", "README.md", "workbench.py", "docs/WORKFLOW.md", "library", "tests", "projects/workbench-bootstrap/records"]
}
```

這是合併進完整計畫的片段，不能單獨准入。它將來源／安全回寫目錄設為集合根目錄，作者仍在由這份來源快照建立的 task worktree 工作。頂層 `allowed_paths` 限定來源範圍，各 task 再列自己的 `allowed_paths`；依需求給精確路徑，不把整個根目錄開放，也不把 `.workflow/` 或 `.git/` 當成果提交。

## 四、配置角色並執行

```sh
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" dispatch csv-export implement --actor HOST_AUTHOR_ID
```

控制者以實際 host Agent ID 登記作者。命令產生 Attempt、獨立 branch 與 worktree，後續 Checkpoint、停止與提交都綁定它；只有依賴已滿足、狀態及額度有效的工作才能啟動。互不相依的小任務可同時 RUNNING，不以全域串行鎖代替工作區隔離。範例中的 `implement` 是計畫自行命名的 task ID，並非固定命令或 Playbook ID。

作者讀取 dispatch 輸出中 `packet` 的原始需求、固定契約、必要輸入、`playbook`、完整 `role_instructions`、全部 `skill_instructions`、`supporting_instructions` 與 `policy`。這些是准入時的內容快照，不能只看 Role 名稱或以目前外部檔案代替固定版本。Role 提供專業責任、Skills 提供方法，跨 Playbook 派工由控制者負責。來源缺失或版本不明就回報缺口，不用臨時編的角色描述代替已宣稱載入的角色。

作者只修改 `packet.workspace` 內屬於 task `allowed_paths` 的檔案。控制者先從來源目錄的當前實際檔案建立受控 Git baseline；選定範圍中的未追蹤新檔會被保存，使用者已刪除的檔案不從舊 HEAD 復活。來源 repo 的 HEAD、index、未提交修改與刪檔不 reset、不 stash、不 stage。

每個 task／Attempt 使用自己的 `codex/` branch 與 worktree，不能把其他作者工作樹當輸入。Git Role 的一般分支建議仍受固定契約約束；不擅自 rebase 到未驗收的可變來源，也不 fetch／push 外部遠端。Git 工作樹隔離避免正常協作互相覆寫，不等於同一 OS 帳號下的敵意程式沙箱。

## 五、提交、Proof 與正式接受

```sh
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" submit csv-export implement --attempt ATTEMPT_ID --files OUTPUT_PATH --stopped
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" review-start csv-export implement --actor HOST_REVIEWER_ID
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" review csv-export implement --file review.json
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" accept csv-export implement
```

先由控制者確認作者停止，再封存實際成果及 Git `repo`、`base_commit`、`commit`、`tree`、`changed_paths`。Reviewer 使用另一個 Agent／上下文，在指定 submission commit 的 detached worktree 查核原始要求、固定契約、驗收基準與整份差異；不改看作者後續可變 HEAD，也不只依賴作者摘要。若多位 Agent 參與作者工作，提交時以 `--contributors` 記錄實際參與者，查核者不得是其中之一。

Proof 需回答三層問題：

| 查核層 | 內容 |
|---|---|
| 證據有效 | 檔案可解析，Digest、來源、成果版本與驗收基準相符 |
| 契約符合 | 每項必要交付、限制與驗收都有證據及判定 |
| 目標達成 | 成果解決原始問題，推論、假設、反證與未驗證範圍明列 |

每項必要驗收有 PASS／FAIL／UNKNOWN 及依據。測試 log 只支持已測行為。合規研究得到未知結論可以是合格交付；缺少原契約要求的必要操作驗證則不能通過。

只有控制程式接受指定版本後，節點才完成；下游只接收已接受成果的固定 Git commit 與封存參照，不沿用上游作者身分、寫入權或 QA 結論。多個小任務要成為共同交付，還必須整合、重新驗收與安全回寫。

| 結果 | 後續 |
|---|---|
| 必要項全部通過 | 接受本版，保存紀錄，允許符合計畫的下游接手 |
| 第一輪有必要缺陷 | 保存原版與缺陷，安排唯一一次自動補件，產生新版本 |
| 第二輪仍有必要缺陷 | 保存對齊包並等待目標對齊，不自動第三輪 |
| 必要查核 UNKNOWN | 保留同一 review／版本與已知缺陷，待受阻條件解除；不暗中換件或先補件 |
| 缺檔、錯版本或身分不符 | 拒絕接受，保存錯誤與恢復線索 |

補件輪次與工具故障重試分開保存，換 Agent 或重啟不歸零。工具恢復、額度增加不自動解除已耗盡的固定上限。

### Review 報告格式

`review-start` 回傳固定的 `review_id`、`round`、`reviewer`、`submission_digest`、`contract_digest`、`baseline_digest`、完整 `acceptance` 及 Reviewer 的 `packet`。查核者須讀完整角色、政策與 Review 契約；綁定欄位直接取自該次輸出。

以下只展示單項欄位，提交前必須依當次 `acceptance` 產生每項且恰一份 `checks`，包括所有 `PB-` 最低項目；不能拿這個單項骨架當完整報告，也不能批次填 PASS。

```json
{
  "review_id": "<review-start.review_id>",
  "round": 1,
  "reviewer": "<review-start.reviewer>",
  "submission_digest": "<review-start.submission_digest>",
  "contract_digest": "<review-start.contract_digest>",
  "baseline_digest": "<review-start.baseline_digest>",
  "stopped": false,
  "evidence": {"E1": "proof/review.md"},
  "checks": [
    {
      "acceptance_id": "<當次 acceptance.id>",
      "status": "UNKNOWN",
      "reason": "填入這一項實際受阻的檢查、原因與恢復條件",
      "evidence_refs": ["E1"]
    }
  ]
}
```

`round` 也取自當次輸出，不固定為 1。`evidence` 將證據 ID 對應到 Reviewer detached worktree 內的實際檔案；若直接引用已封存成果，可用 `submission:<提交時的相對檔名>` 作為 `evidence_refs`。每項都要有證據及具體理由。控制者確認 Reviewer 真正停止後，才把 `stopped` 設為 `true` 並送交；上例的 `false` 會被拒絕。

### Git 整合與安全回寫

需要合併多條成果分支時，在固定計畫加入 `playbook: integrate`、`role: integrator` 的 task，`depends_on` 列出來源小任務，並定義整體驗收及整合可寫範圍。來源 task 必須已接受；控制命令在新的整合 worktree 依固定順序合併其固定 commits。各分支個別通過後，Project 仍未完成。

整合衝突保存為 `WAITING / GIT_MERGE_CONFLICT`，保留衝突檔、Git 狀態、來源及 Attempt；不覆寫來源目錄或清理作者分支。host 在這個整合 worktree 解決衝突並 `git add` 後，才以 `resume` 登記處理依據、完成 merge 並接續同一 Attempt；不能跳過未整合的來源。

整合後仍須 `submit`、獨立 `review-start`／`review` 及 `accept`。最後只有全部必要 tasks 已接受、選定 leaf 包含固定整合成果時，才執行：

```sh
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" apply csv-export combine
```

`apply` 逐檔核對來源目前內容仍等於 baseline，再套用已接受 commit 的允許差異；包含原本不存在與應刪除檔案的狀態。任一來源途中被使用者修改，保存 `WAITING / SOURCE_CHANGED` 並拒絕覆寫，不先寫其他檔案。成功回寫不操作來源 `.git`，來源 HEAD、index 與無關未提交修改保持原狀。單一小任務同樣要安全回寫後，才把原 Project 標成 DONE。

回寫先預檢全部目標，再逐檔替換，不是多檔原子交易。host 須避免回寫期間另有來源寫入者；程序若在替換途中失敗，保留現場並核對哪些檔案已變動，不宣稱已全部撤回或盲目重跑。預檢與檔案替換不提供敵意 OS 寫入競態的強制隔離。

如果 host 已在控制程式尚無 Git 支援時建立 branch/worktree，須用明確的 `adopt-git`／接管事件核對現有 Attempt、私有 repo、基線及路徑後接續，保存 bootstrap 來源；不能直接改 SQLite，或宣稱舊派工早已建立隔離。

```sh
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" adopt-git csv-export implement --attempt ATTEMPT_ID --worktree EXISTING_TASK_WORKTREE --base-commit FIXED_BASE_COMMIT
```

## 六、保存、等待與接續

```sh
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" checkpoint csv-export implement --attempt ATTEMPT_ID --files PARTIAL_OUTPUT --note "已定位原因，尚未修正"
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" pause csv-export implement --attempt ATTEMPT_ID --note "等待必要資料" --stopped
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" status csv-export
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" resume csv-export implement --note "必要資料已補足"
```

恢復先讀正式狀態、最後可靠 Checkpoint、缺口及固定版本。新執行建立新 Attempt，舊 Attempt 不重新有效；已提交待驗收的工作接續原版本，不重跑作者。

`--stopped` 只能在控制者收到真實 host 停止／完成訊號後使用。未知退出狀態不能另派同一資源的寫入者。Checkpoint 只保全已登記的檔案與進度，不保證恢復未保存內容或模型內部狀態。

```sh
python3 "$WORKBENCH_ROOT/workbench.py" --root "$WORKBENCH_ROOT" cancel csv-export --reason "使用者取消" --stopped
```

取消先停止作者／Reviewer，保留部分成果、證據與原因；取消不會撤回已發生效果。晚到報告不能令終態重新執行。

## 進度與完成

查詢要能看見當前工作、等待原因、有效 Attempt、審查輪次、指定版本、已接受成果、缺口與下一步。Project 完成取決於固定交付終點、全部必要工作、整合後 Proof 與安全回寫，不憑最後一位 Agent 的回覆或檔案存在判定。

本機測試驗證控制行為；真實 Agent 試跑另外驗證角色／技能載入、交付品質、獨立審查及下游接手。兩者分別保留範圍，不能互相替代。
