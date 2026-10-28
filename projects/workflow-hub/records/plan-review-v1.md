# 計畫完整性獨立查核 v1

結論：FAIL。這是准入前計畫查核，不是實作驗收，也不宣稱任何測試、封存成果或完整工作流已通過。

- Reviewer：`/root/independent_review`；未參與作者工作，未修改作者程式、測試、library 或正式狀態。
- 正式計畫：`5b4107dd13aefa0e47ad2d8023e36509d8a79bebf6cf3b5412ef35fba054e636`。
- 取得方式：`Workbench(Path('.')).status('workflow-hub')`；狀態為 PLANNING／PLAN_REVIEW_REQUIRED、plan_approval=null、所有 generation=0。
- 查核基準：records/REQUEST.md 原始六步與授權；正式 plan 而非僅 candidate JSON；docs/WORKFLOW.md；docs/playbook/PLAYBOOK_MVP_ARCHITECTURE_PROPOSAL.md 全文；PLAYBOOK_MVP_EXECUTION_FLOW.md 全文；library/playbooks/ 五份契約。

## 阻擋缺口

### P1-01：build 驗收依賴尚未能執行的下游

FACT：正式 plan.tasks.build 的 AC-R7 描述含「真實走完作者/Reviewer/下游鏈」，method 指定檢查「實際下游HANDOFF產物」。同一計畫的 handoff.depends_on=[build]，且 AC-HANDOFF 明定下游作者必須讀「已接受build」封存產物。

INFERENCE：若遵守原驗收，build 通過前尚不能執行 handoff，卻需要 handoff 的實際交付作為通過證據；單純 task DAG 無環不足以排除此驗收循環。先將 AC-R7 填 PASS 會把未執行下游當成已驗證，違反 R5 與 P00-03/07。

必要修正：R7 與整條真實鏈要求保留；build 的責任固定為可使用入口、CLI、操作說明與足供接手的封存交付；實際下游鏈與 HANDOFF 完成的判定留在已存在的 handoff 必要驗收。改完重新保存正式計畫、取得新 plan_hash 再查核，不可沿用本版報告。

### P1-02：已聲明重用的必要輸入沒有固定版本

FACT：plan.inputs 列出兩份 docs/playbook 規格與「本次三位agents的設計與初稿」，routing.reason 使用已有初稿作為直接進入整合的理由；兩個 task.supporting_sources 均為空。上述來源既無確定的初稿檔案位置，也未列入正式計畫的支援來源快照。REQUEST.md 保存了原始六步，但目前也是可變工作檔而非本次 pin 的來源。

FACT：docs/WORKFLOW.md 第三節明定「Role／Skill 主檔以外，實際使用的參考文件或腳本須在准入前列入 task 的 supporting_sources」。舊流程規格 2.2 的階段略過／重用要求保留既有產物 Digest、來源、版本及適用依據。這些要求不能因已釘選 Role/Skill 而視為滿足。

必要修正：將實際使用的原始要求紀錄、規格與重用設計／初稿列為可定位且固定內容的 supporting_sources；或明確區分僅供背景的來源，不拿無版本背景作為前置工作已完成或可略過的證據。前期工作在工具完成前產生的事實仍須保留，不倒填派工。新 pin 後重做准入查核。

## 其餘完整性查核

| 要求／面向 | 判定與依據 |
|---|---|
| 原始六步覆蓋 | FACT：R1–R6 與 REQUEST.md 六步逐項相符，build AC-R1–AC-R6 各有方法；未將成熟度判斷硬改為必經研究或設計。R7 補入實際可使用入口與接手鏈，未取代六步。上述 P1-01/02 仍阻擋整體准入。 |
| Playbook 定位 | FACT：五份契約皆有 purpose、適用條件、必要輸入、stages、stop_when、required_criteria 與 handoff_fields；不讓 Playbook 自行啟動其他工作。build/handoff 選 deliver，對工程整合與文件接手合理。 |
| 最低必要 criteria | FACT：從正式 plan 的 playbook_digest blob 讀 deliver，逐欄比對 required_criteria；build 與 handoff 各自附入 requirements/integrity/verification/handoff 四項，ID、description、method、requirement_ids 完整相符，沒有刪減或弱化。review 契約另行 pin。 |
| Role 與 Skills 來源 | FACT：implementer 使用 minimal-change-engineer.toml＋Ponytail；writer 使用 technical-writer.toml＋Humanizer；reviewer 使用 code-reviewer.toml。逐份核對來源檔與 blob 位元內容一致、SHA-256 正確，TOML 有完整 developer_instructions。查核者實際讀取 reviewer 完整 developer_instructions；未用角色摘要冒充載入。Ponytail/Humanizer 主檔未要求另讀支援資源。 |
| P00 | FACT：讀取 pin 的政策全文，sha256=44aeaae7ec5bf1f687a2b3cf09e9dd312505d2c4609111e18f9397f8023b2adf，blob Digest 正確。政策仍明示語意真實性與安全不能只靠 prompt 保證。 |
| 輪次、重試、作者上限 | FACT：正式 limits 為 max_rounds=2、review_retries=2、max_attempts=4。AC-R5/6 要求實際檢查兩輪、UNKNOWN、重試及作者上限；docs/WORKFLOW.md 明述更換 actor/重啟不歸零、第二輪缺陷等待對齊。這裡只確認契約存在，尚未驗證程式真的遵守。舊架構的 Token/費用硬限制、Runner 強制停止、隔離不是這三個計數可以證明的能力。 |
| 同 OS 能力限制 | FACT：REQUEST、正式 constraints 與 docs/WORKFLOW.md 如實說明可信同 OS 協作，actor/stopped 為 host 控制者紀錄，不是外部身份驗證、程序終止或惡意 Agent 隔離；local 範圍排除發布/部署/付費/外部寫入。未要求恢復使用者刻意刪除的 workflow-mvp。INFERENCE：可作本機受信任協作的有界交付，不代表舊兩份完整目標架構全數落實。 |
| Proof 獨立性與依賴 | FACT：計畫要求指定版本、獨立 Reviewer、逐項 Proof 後接受；handoff 只依已接受 build。查核者與 planner=/root 不同。P1-01 為目前不可執行處。 |
| 早期 Bootstrap 誠實性 | FACT：REQUEST 與 constraints 明示前期討論/初稿不是本工具派工；本次重新固定契約、整合及驗證。不應回填此前已通過本系統。P1-02 尚需固定其真實來源。 |

## 已做與未做

已做：讀取指定需求、完整規格與本機契約；讀取 pinned reviewer/policy；使用標準庫解析正式狀態、比對最低 criteria 及來源檔/內容 Digest。未操作正式狀態；僅寫此查核證據及 JSON。

NOT_RUN：未執行實作測試、真實作者／Reviewer／下游交付、發布或任何瀏覽器檢測。未確認程序隔離、強制停止、帳單上限或正式共用方法認證。尚無這些證據，不能由本報告推導它們已通過。

恢復條件：作者／控制者修正以上兩項，重新儲存未開工正式計畫，提供新 plan_hash 後才可查核下一版；保留本次 FAIL，不覆寫成 PASS。
