# 共用 Playbooks 與角色

`playbooks/*.json` 是工作契約的來源；`roles.json` 指定實際角色指引與 Skills 的repo 相對來源。工作入口與命令見根目錄 README，執行、Proof、恢復及權限規則見 `../docs/WORKFLOW.md`。

## 選擇工作

| Playbook | 何時選用 | Role |
|---|---|---|
| clarify | 需求種子要討論培養，或有會改變目標、範圍或驗收的關鍵歧義 | planner |
| research | 下一步缺少可查證事實 | researcher |
| design | 需要新介面，且既有設計不足 | designer |
| deliver | 輸入與契約足夠，能完成工程或文件交付 | implementer／writer |
| integrate | 多個已接受的小任務提交需整合成共同交付 | integrator |
| review | 對指定成果或候選契約做獨立查核 | reviewer |

Agent 提出適用的 Flow；控制層核對契約、依賴、版本及准入條件。Playbook 只執行自己的工作並交付成果、缺口或候選提案，由控制層安排其他 Playbook。原型可作 clarify／design 內的方法；不因此自行派生新 Job。

可並行的小任務各自使用固定基線的 Git branch/worktree，不共用作者工作目錄。多來源共同交付明列 integrate 節點，只整合已接受的固定 commits；衝突等待並保留工作樹，整合後再由獨立 Reviewer 查核。個別 task 接受不代表整體 Project 已完成。

清楚的需求可直接 deliver。略過前置工作須有足以覆蓋必要輸入及交付的依據；找不到適用工作就保存能力缺口。此版本涵蓋上述工作，發布、付費、外部寫入及其他領域工作須另有適用契約與授權。

## 契約與 Proof

每份 Playbook 的 `required_criteria` 都是最低驗收，會與任務原始要求共同成為固定基準。Task 追加具體要求，不能刪減最低項。`required_inputs`、階段及 `handoff_fields` 供 Agent 與 Reviewer 核對語意完整性；欄位存在本身不能證明內容足夠。

review 是共用查核契約，供獨立 Reviewer 執行；不以 reviewer 再派另一位 reviewer 形成遞迴審查。查核報告回到控制層處理接受、補件或等待。研究得到 UNKNOWN 可以是完整研究的結論；必要操作未驗證仍是驗收未完成。

## 載入與釘選

Role 在 `.claude/agents/*.md`，Skills 在 `.claude/skills/<name>/`；`roles.json` 的相對路徑一律以原集合根目錄解析。派工前讀取完整 Role／Skill 指引，保存實際內容及 SHA-256 快照。這些檔案同時可供 Claude 發現與控制程式釘選，不依賴使用者家目錄。缺少來源就回報能力缺口，不自行換角色或假稱已載入。

快照只涵蓋實際讀入的檔案。Skill 要使用其他文件、腳本或 Hooks 時，先確認適用性及操作範圍，再將實際使用檔案加入本次版本依據；主 `SKILL.md` 的雜湊不表示整套上游套件已被審查。進行中的工作使用自己的固定版本，不隨上游更新默換內容。

角色與 Skills 提供專業及方法，仍受使用者要求、固定契約、P00 與當次工具權限約束。designer 的兩份 Skills 形成單一設計交付。reviewer 不強制綁定只審已提交 Git 內容的方法；它依本次成果快照與逐項契約查核。

這些契約供本機 Agent 協作試跑與累積證據，不宣稱通過全部領域或正式環境評測。來源快照能證明載入內容與版本，不能證明 Agent 已理解，也不提供同一作業系統內的惡意 Worker 隔離。

## 可搬移的方法包

`.claude/methods-manifest.json` 記錄實際包入的檔案雜湊、來源版本與適配項目；授權隨來源保留。`python3 scripts/check_portability.py` 查核完整性、相對來源與必要執行工具，不安裝套件、不開瀏覽器、不驗證 Claude 平台已載入。

這次只包含本 repo 綁定的七份 Skills、七個 Roles，以及 grill-me、grill-with-docs、ask-matt 入口；沒有搬整台電腦的個人 Skills、MCP、登入資料或插件快取。需要其他方法時另行評估與釘選來源。兩份 UI Skill 的執行支援、資料和素材保留，上游測試／evals 與 Codex UI metadata 不納入。

更新方法時核對上游差異與授權、修正 repo 路徑及 wrapper，再更新 manifest 的對應雜湊與適配紀錄；已有正式計畫仍用原快照，不能默換。
