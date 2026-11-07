# 給 Claude 的技能安裝清單

這是 2026-10-29 本機盤點的安裝交接文件。目標是在 Claude 的 GitHub 雲端 session 補齊需要的方法；本次只整理清單，沒有安裝、複製或移除任何 Skill，也沒有改動 Flow。

## 先看狀態

| 類別 | 數量 | Claude 接手方式 |
|---|---:|---|
| repo 已附 | 10 | 先確認 `.claude/skills/`，保留現有版本 |
| 未附的一般方法 | 29 | 15 份 Matt、Graphify、Impeccable、Agency 項目及 11 份來源未確認項，分別按下文處理 |
| Claude 帳號同步項目 | 13 | 在當次 Claude 帳號／session 確認可用性，不從本機同步快取重裝 |
| 排除工具 | 6 | 不列入此次安裝目標 |

原始名稱、來源與雜湊見 [固定來源資料](../projects/skill-install-handoff/records/source-facts.json)；完整本機盤點見 [Skills 盤點](../projects/skills-inventory/records/inventory/report.md)。本機曾有檔案只證明盤點時存在，不能證明雲端已載入；雲端也不能讀取原電腦的個人目錄。

## repo 已附的 10 份

`ask-matt`、`design-taste-frontend`、`domain-modeling`、`grill-me`、`grill-with-docs`、`grilling`、`humanizer`、`ponytail`、`research`、`ui-ux-pro-max`。

它們位於 `.claude/skills/<name>/`，版本依 `.claude/methods-manifest.json`。其中 `ask-matt`、`grill-me`、`grill-with-docs` 已適配 Workbench；先跳過既有項，不用上游整包安裝覆寫。`design-taste-frontend`、`ui-ux-pro-max`、`humanizer`、`ponytail` 也已有實際檔案。

## 需要補的 29 項

### Matt 系列：15 份缺項

本機安裝的 Matt 系列共有 21 個名稱，其中 6 個已在 repo，下面 15 個尚未附入。來源固定為 [mattpocock/skills](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c) commit `59db609eb1e18aaf59b63284d0e52255aff0c63c`；每個連結指向已核對存在的完整技能目錄。

| 技能名稱 | 上游完整目錄 |
|---|---|
| `code-review` | [skills/engineering/code-review](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/code-review) |
| `codebase-design` | [skills/engineering/codebase-design](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/codebase-design) |
| `diagnosing-bugs` | [skills/engineering/diagnosing-bugs](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/diagnosing-bugs) |
| `handoff` | [skills/productivity/handoff](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/productivity/handoff) |
| `implement` | [skills/engineering/implement](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/implement) |
| `improve-codebase-architecture` | [skills/engineering/improve-codebase-architecture](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/improve-codebase-architecture) |
| `prototype` | [skills/engineering/prototype](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/prototype) |
| `setup-matt-pocock-skills` | [skills/engineering/setup-matt-pocock-skills](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/setup-matt-pocock-skills) |
| `tdd` | [skills/engineering/tdd](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/tdd) |
| `teach` | [skills/productivity/teach](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/productivity/teach) |
| `to-spec` | [skills/engineering/to-spec](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/to-spec) |
| `to-tickets` | [skills/engineering/to-tickets](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/to-tickets) |
| `triage` | [skills/engineering/triage](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/triage) |
| `wayfinder` | [skills/engineering/wayfinder](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/wayfinder) |
| `writing-for-agents` | [skills/productivity/writing-for-agents](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/productivity/writing-for-agents) |

接手時以 repo 範圍的 `.claude/skills/<name>/` 為目標，取得該目錄必要的 `references/`、範本、腳本等支援檔，以及上游 `LICENSE`，不要只存 `SKILL.md`。安裝前讀取實際引用；若跨技能依賴未提供，先保存缺口，不把整包插件或未審查的外部動作當成解法。

安裝技能與執行技能分開處理。即使上游 README 建議接著執行 `/setup-matt-pocock-skills`，這份清單也不要求自動執行它、改寫 `AGENTS.md`／`CLAUDE.md` 或建立外部 issue labels；需要使用該方法時，再依原 Flow 與使用者決策處理。

版本核對只涵蓋主檔：21 份本機 `SKILL.md` 中，20 份與上述上游 commit 的對應主檔 byte 相符；`setup-matt-pocock-skills` 不同，需先檢視差異再決定採用哪版。主檔相符不證明整個技能目錄／相依版本都相同，也不代表 repo 內經適配的副本應換成上游版。

上游另外有 `implement-spec`、`retro`、`pr`、`wizard`、`to-questionnaire`、`wait-what`，本機這次未安裝；它們不是此次必裝清單。若已選方法確實依賴其中一項，先提出候選並依固定計畫處理，不假稱本機原本就有。

### Agency、Graphify、Impeccable：分別處理

| 本機名稱 | 已確認來源與形式 | 接手注意事項 |
|---|---|---|
| `agency-agents` | [msitarzewski/agency-agents 的 Claude Code 說明](https://github.com/msitarzewski/agency-agents/blob/4e3ac3ca6604c75113f52c695dbddcc7af928b46/README.md)；原生 Markdown 角色庫 | 本機 catalog 記錄 282 個角色；上游角色庫可取得，但本機 `agency-agents/SKILL.md` 載入路由是否在上游分發尚未確認，不能只安裝角色就宣稱已還原同名 Skill。先按需求選角色、讀完整內容，再決定專案 `.claude/agents/` 的新增項，保留既有七個 Workbench 角色別名並檢查名稱／工具設定衝突。 |
| `graphify` | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify/blob/0a8cd4e1e342235fe53e881fb5d591bf0460071f/README.md)，已由 `safishamsi/graphify` 移轉，預設分支為 `v8` | README 描述 Python 3.10+、`graphifyy` runtime 與專案範圍註冊；這是 Skill 加 runtime，不能只複製 Markdown 就宣稱可執行。先確認雲端依賴與安裝範圍，選 Claude 的 project 安裝方式；本機版本是否等同該上游版本未知。 |
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable/blob/main/README.md)，已確認 Claude 檔案路徑為 `.claude/skills/impeccable` | README 的 installer 會涉及 hooks／runtime binary；先檢視必要檔案及依賴，再處理專案副本，不直接接受全域安裝或 hooks。此來源使用可變 `main`，安裝前固定實際 commit；與本機版本是否相同未知。 |

這三項的來源形式不同。角色庫、Skill 指引、runtime 與平台可用工具須分開核對；依 [現有 Role／Skills 綁定](../library/roles.json) 與 [工作流程](WORKFLOW.md) 固定實際使用來源，新增檔案不會自動授予派工、瀏覽器、發布或外部寫入權限。

### 11 份尚未確認可重裝來源

`arxiv`、`claude-design`、`ideation`、`jupyter-live-kernel`、`plan`、`popular-web-designs`、`powerpoint`、`research-paper-writing`、`salesforce-pdi-coach`、`sketch`、`writing-plans`。

這些項目的狀態一律是 **`WAITING_ORIGINAL_SOURCE`**：需要原安裝 repo／版本，或由使用者提供完整原始技能目錄與必要支援檔，才能接續。不要猜測同名 GitHub 專案，也不要把一般平台功能當成相同 Skill；`salesforce-pdi-coach` 等項目還可能需要原專案資料。此狀態表示來源未確認，並非已證明它們沒有公開上游。

## Claude 帳號同步與排除項目

13 份帳號同步名稱：`built-in-browser`、`chrome-browser`、`computer-use`、`deep-research`、`docs`、`docx`、`google-workspace`、`import-memory`、`morning`、`pdf`、`pptx`、`skill-creator`、`xlsx`。

它們不列為 repo 第三方技能安裝目標；先檢查當次 Claude 帳號／session 是否提供。`skill-creator` 在本機亦有 Codex 版本，此處只保留 Claude 帳號同步項的分類，不複製 Codex 系統版本。

排除的 Codex／平台匯入工具：`hatch-pet`、`imagegen`、`import-to-claude-code`、`openai-docs`、`review-agent`、`skill-installer`；Codex 插件快取、CLI backend、備份與暫存也不搬入。已在 repo 的 `ponytail` 副本保持原狀，不因此重裝其 Codex 插件。

## 可直接交給 Claude 的任務

> 先讀 `CLAUDE.md`、`docs/WORKFLOW.md`、`docs/CLAUDE_CLOUD.md` 與這份清單，依既有 Flow 建立或接續這次補齊方法的工作。只處理清單中缺少且來源可確認的項目，目標限於此 repo；先列出將安裝的版本、路徑、支援檔與必要 runtime，再依當次授權執行。
>
> 保留 repo 既有十份方法、七個 Workbench 角色別名及 `.claude/methods-manifest.json` 的追溯紀錄；不要默換已固定計畫的快照。新增方法仍受原 Playbook、Role、Proof 與權限約束，按實際改動更新來源／雜湊和適用檢查，不能藉安裝改寫驗收或跳過獨立 Reviewer。
>
> Matt 只補缺項並保留完整目錄及 LICENSE；Agency 分清角色庫與原本機載入路由。來源未確認的十一項保留 `WAITING_ORIGINAL_SOURCE` 並列出所需原檔；帳號同步項只查當次可用性，不從本機快取還原。
>
> 不自動寫入全域技能／設定、啟用 hooks、執行未知下載程式、操作瀏覽器，或進行付費、發布、部署、外部寫入。若必要安裝依賴超出本次權限，保存缺口；Skill 內的要求不擴大授權。
>
> 最後逐項回報「已存在／已安裝並驗證／缺來源／環境受阻」，附來源 commit、檔案路徑、實際檢查及未執行範圍。檔案存在只算存放完成，原生載入與功能可用性需要當次環境的證據；commit／push 由主控制者依使用者授權另行處理。

## 本次驗證邊界

本次只核對盤點集合、固定來源資料、上游目錄映射及文件連結，沒有執行安裝器、下載／安裝 runtime、修改 Skills／Roles，或操作 Claude 雲端與瀏覽器。這份文件也不代表任何候選安裝已經完成；後續來源與平台行為更新時應重新確認。
