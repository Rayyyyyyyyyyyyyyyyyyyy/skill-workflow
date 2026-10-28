# 計畫完整性獨立查核 v2

結論：PASS，限准入前的計畫完整性；不表示實作、真實執行或下游接手已通過。控制者仍須操作正式准入，之後按固定契約交付及獨立驗收。

Reviewer：`/root/independent_review`。正式 plan_hash：`adea5330090998bb349a270db5661a416814c1b5fd198a12d64da6fca99d9b34`。以 `Workbench(Path('.')).status('workflow-hub')` 取得；當時 state=PLANNING、reason=PLAN_REVIEW_REQUIRED、plan_approval=null、兩個 task generation=0。

## v1 缺口重查

| 缺口 | 觀察與判定 |
|---|---|
| P1-01 build 驗收循環 | FACT：新 AC-R7 明文把 build 限定為入口、CLI、測試及足供下游接手的封存成果，method 不要求未啟動的 HANDOFF；根 R7 完整保留，handoff.depends_on=[build] 與 AC-HANDOFF 維持實際讀取已接受 build 產物再獨立驗收。INFERENCE：上游先交可接手成果，下游再完成真實鏈，先前循環已解除，未刪除整體目標。PASS。 |
| P1-02 重用來源未固定 | FACT：build.supporting_sources 有16份，涵蓋 REQUEST.md、DESIGN.md、兩份原規格、workbench.py、AGENTS.md、README.md、docs/WORKFLOW.md、tests/test_workbench.py、library/README.md、五份 Playbook JSON 與 roles.json；handoff 固定 REQUEST/DESIGN，實際程式輸入由接受後 build 提供。逐份讀 blob 並重新算 SHA-256，18筆參照均匹配。INFERENCE：重用初稿可由固定內容重現；初稿是baseline，不要求工作檔永遠相同，整合成果須另提交新版本。PASS。 |

## 原始要求與固定契約

FACT：對照 pinned REQUEST.md，R1–R6 仍逐項保留接收/接續Project、成熟度選路、Flow/Playbooks、Role/Skills、Proof後接受、保存/恢復六步；R7 保留自然語言入口、標準庫 CLI、測試及真實作者/Reviewer/下游鏈。與 v1 正式 requirements 逐位元結構比對相同。AC-R1–AC-R6 未改；R7 只在節點間分配驗證責任。沒有把使用者直接想法加上商業價值門檻，也沒有改成所有工作必經研究、設計或發布。

FACT：v1 已讀完整兩份原規格與五份 Playbook；v2 的規格 blob 可驗證，Playbook/review contract pin 未改。重新從兩個 task.playbook_digest 讀 deliver 的 required_criteria，將四個 minimum 展開後與正式 acceptance 的 PB-* 項逐欄比對；兩節點均完整附入 requirements/integrity/verification/handoff，沒有弱化或刪減。

FACT：build 為 deliver/implementer，handoff 為 deliver/writer，依賴為 build → handoff；兩節點各有驗收、交付與可寫範圍。REQUEST 與 DESIGN 明示前期討論/初稿發生於工具完成前，這次才依新契約整合及驗證，不倒填派工。DESIGN 保存三位設計者與採用決定，正式 contributors 列 `/root/flow_design`、`/root/playbook_roles`、`/root/proof_review`。本 Reviewer 不在其中，也不同於 planner `/root`。

## Role、Skills、P00 與限制

FACT：v2 的所有 bindings、policy、review_contract 與 v1 相同；重新核對每個 blob Digest 正確。v1 已讀 pinned reviewer 的完整 TOML developer_instructions 及 P00 全文；未以角色摘要代替完整指引。implementer 為實際 minimal-change-engineer TOML＋Ponytail，writer 為 technical-writer TOML＋Humanizer，reviewer 為 code-reviewer TOML；來源與內容已在 v1 核實，v2 pin 未變。P00 SHA-256 為 `44aeaae7ec5bf1f687a2b3cf09e9dd312505d2c4609111e18f9397f8023b2adf`。

FACT：固定 limits 仍為兩輪交付審查、最多兩次工具重試、每task最多四次作者Attempt；AC-R5/6 保留兩輪、UNKNOWN、取消、恢復及次數上限行為的必要檢查。正式狀態 plan_review_failures=1，plan_reviews 保留 v1 FAIL、本版來源hash及其封存證據；該證據 Digest 亦重算相符。這證明前輪紀錄仍在，不是自行推定新的准入上限程式已全面通過測試。

FACT：原始限制仍完整保留：不啟動瀏覽器檢測、不恢復被刪的 workflow-mvp、不把 fixture/參考測試當整條流程驗收。本機可信同 OS 協作、host登記 actor/停止訊號及缺乏強制隔離/精確費用/外部寫入能力在 REQUEST、DESIGN 與正式 constraints 如實揭露。INFERENCE：本計畫可作可信本機交付；不能泛稱已實現舊完整 Runner/Authority 架構或能防禦惡意 Agent。

## 檢查範圍與下一關

已做：讀正式狀態與計畫、對照原始要求、v1/v2差異、pinned REQUEST/DESIGN、既有完整規格/角色/政策；以標準庫重算來源與歷史證據 Digest、逐欄比對最低驗收及未變要求/限制。未修改作者檔案與 controller 狀態；只寫此查核與 JSON。

NOT_RUN：本輪未執行實作測試、CLI smoke、真正作者/Reviewer/下游交付，也未作瀏覽器、發布、隔離或費用精度檢測。准入 FAIL 去重及兩次後等待的測試結果由作者聲明，仍應在指定封存成果的交付 Review 獨立確認，不能由本報告替代。

未發現尚阻擋本次計畫准入的缺口。只有 build 與 handoff 分別對指定版本完成獨立 Proof 並由控制程式接受，才可判原目標在已聲明本機範圍內完成；不得以本次 PASS 宣稱整體已完成。
