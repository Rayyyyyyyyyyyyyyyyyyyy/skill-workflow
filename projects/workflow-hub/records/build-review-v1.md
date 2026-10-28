# Build 指定版本獨立交付查核 v1

結論：FAIL。本輪完整查核11項，8項PASS、3項FAIL，沒有UNKNOWN。發現一個須補件的資料完整性缺陷D1；其他必要項已完成判定，不需再新增Reviewer。查核完成不代表正式接受、發布或整個Project完成。

## 固定對象與身份

- Reviewer：`/root/independent_review`，未參與作者整合工作；submission.contributors含 `/root`、`/root/flow_design`、`/root/playbook_roles`、`/root/proof_review`，不含本Reviewer。
- review_id：`66cef08e6dd040cfb30dfd2452d56f4f`；round=1。
- submission_digest：`68ecc05e5c8ba6417d683ee854f8a9139469f6a9d6f2f2980ed2397964a59fc5`。
- contract_digest：`8846d1784bcf8b2c375c931388637fda8954f51ad49221fec06654bc8568044d`。
- baseline_digest：`5ba4fa11c8f7f9bb3fffc66ccb7a7fa222c254f87d450b068167fddf93a5f8be`。

FACT：以records/build-review-packet.json的submission.files為權威，從projects/workflow-hub/.workflow/blobs複製25份提交檔案到 `/private/tmp/workflow-build-independent-v1`。逐檔重算SHA-256、核對manifest內容與Digest、acceptance基準Digest，以及16份supporting_instructions的內容與其pin一致；沒有以可變同名工作檔替代提交。讀取完整packet Reviewer原生指令、P00、review Playbook；reviewer無附加skill。原始REQUEST/兩份規格已在前兩次計畫Review完整閱讀，這次對照封存REQUEST、DESIGN、實際workbench.py、完整tests、入口及操作文件、作者VALIDATION與逐命令log。

## D1 — 同一工作區允許雙作者，造成覆寫與錯誤來源歸屬（P1）

FACT：封存workbench.py:354–375的dispatch只檢查當前task為READY、次數與上游DONE；未檢查同Project已有RUNNING作者。_workspace與_packet對同Project所有task給同一workspace，沒有task個別路徑分隔或其他互斥。BEGIN IMMEDIATE只序列化資料庫交易，不能讓已核發兩個作者的工作區寫入自動互斥。

FACT：使用封存tests的公開fixture在暫存Project建立兩個沒有相依的deliver task，透過公開API批准計畫後，先派build再派document，兩次均成功且兩task同為RUNNING、workspace字串相同。第一作者寫artifact.txt，第二作者在同一允許工作區寫同名檔後，第一作者以原有效Attempt submit；其封存內容實際為 `author-two output`。沒有偽造stopped以外的OS能力、直接改正式狀態或越界寫入。執行結果與完整路徑保存於build-review-concurrency-v1.json；暫存Project已清理。

INFERENCE：這是正常控制入口造成的共享資源碰撞，不依賴惡意Agent繞過CLI；可能丟失第一作者成果，或把別的task產物封存成第一task的成果。可信同OS與無惡意隔離的限制不會解除控制者自己發出的兩個有效寫入者之間的完整性責任。固定Flow節點無環亦不代表可安全共用可寫工作區。

要求依據：原架構§2「單一主機、單一控制程式與有界順序執行」；原流程§3不變條件1「同一受影響資源不能同時有兩個可寫入的Attempt」；本次PB-build-integrity要求保留既有資料及必要錯誤處理。當前文件沒有把同工作區並行列為可忽略的已知限制。

最小必要修正：在控制邊界防止兩個作者同時持有相同或重疊工作區的寫入資格。至少拒絕本反例中同Project第二次dispatch，保持第二task未派工且不扣Attempt；亦應考慮workspace='.'維護Project共用集合根目錄的情況。先完成host確認的submit/pause/cancel，釋放前一作者之後才可派下一作者。新增一個公開行為回歸證明拒絕與安全釋放，不需要引入平行執行框架。補件仍是新版本與第二輪，保留本次原版與缺陷。

## 驗證證據及其範圍

FACT：在封存副本上執行 `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`，Python 3.14.0，exit=0，40tests通過。逐項輸出保存在build-review-test-v1.txt。測試setUp還需既有runtime-reference/config及policies，從現存未變元件複製到temp供fixture使用；P00文字與packet精確相同。這是明列的測試環境前提，並未把未封存參考檔冒稱本次交付檔。

FACT：作者test-output保存同樣40tests、AST/JSON/來源/連結/CLI smoke與41個舊參考測試的分開範圍，VALIDATION如實記錄初次5個TypeError及修復，未用fixture或舊參考測試冒充真實角色品質或完整原23案例通過。真實packet載入與本次獨立Review屬額外真實鏈證據；下游HANDOFF尚未啟動，本報告沒有將它填作完成。

NOT_RUN：未重跑無新疑點的舊參考測試；未開瀏覽器、未發布/部署/外部寫入/付費，未驗證OS隔離、程序樹強制停止、精確帳單或跨主機備份恢復。以上限制與本次CLI/文件交付一致，沒有將它們判成PASS。D1屬已確定缺陷，非工具受阻UNKNOWN。

## 逐項判定

### AC-R1 — PASS

new拒絕同名覆寫、slug/檔案越界；SQLite保存原始idea與狀態。已封存REQUEST及真實workflow-hub packet保留原始需求；獨立重跑同名保全/持久化/CLI測試通過。

### AC-R2 — PASS

AGENTS/WORKFLOW及clarify/research/design/deliver適用條件保留成熟度選路；程式要求routing理由並阻擋missing_inputs；prepare接受後仍等待delivery。對應公開測試獨立通過，未冒稱CLI可理解自然語言。

### AC-R3 — PASS

五份Playbook有必要輸入/階段/停止/criteria/交接；plan驗證DAG與原始要求映射並附入最低項，dispatch只使用已DONE上游固定submission。獨立測試確認未接受上游不能解鎖。共享資源安全缺陷另列PB-build-integrity，不能由DAG合法推定安全。

### AC-R4 — PASS

正式packet及supporting內容具有實際原生Role/Skill/P00快照，非虛構角色摘要；作者VALIDATION聲明完整載入，Reviewer實讀packet完整角色/政策。來源變動後仍使用pin及缺來源拒絕測試獨立通過，未把fixture當角色語意評測。

### AC-R5 — PASS

submission manifest、baseline與25檔Digest核實；review綁定6欄、每acceptance恰一check及實際evidence，accept重算manifest/成果/review證據，只在全PASS才DONE；自審/歷史貢獻者/缺件/舊版本/竄改/兩輪測試獨立通過。此判定支持機制，本輪仍須由控制者接受。

### AC-R6 — PASS

checkpoint/pause/resume保持檔案及舊Attempt失效；UNKNOWN同review/版本恢復且已知FAIL不能改寫；2輪/2重試/4作者上限跨重啟保留。准入FAIL去重與跨plan保留亦由公開測試確認。host停止紀錄屬可信本機收據，未冒稱OS強制終止。

### AC-R7 — PASS

AGENTS自然語言入口、README、WORKFLOW完整命令與CLI可用，封存包含程式/library/tests/REQUEST/DESIGN/VALIDATION/逐命令log與manifest。build只交可接手版本，實際HANDOFF尚待build接受後驗收，作者未虛報下游或整體完成。

### PB-build-requirements — FAIL

六步與R1-R7有實作對應，但共享工作區可同時派兩個作者，違反原規格同一資源不得雙寫及MVP有界順序執行要求；此安全缺口未被可信同OS限制豁免。詳D1反例。

### PB-build-integrity — FAIL

D1：dispatch第354–375行只鎖定單一task，未排除同工作區另一RUNNING作者。合法無依賴tasks可同時RUNNING且workspace相同；獨立反例中第二作者覆寫artifact.txt後，第一task提交封存了第二作者內容，有資料覆寫及來源歸屬風險。

### PB-build-verification — FAIL

獨立從封存副本執行40個測試皆通過，作者log與限制可追查；但新確認D1正常控制入口反例未通過且缺對應回歸，必要共享資源完整性仍未解決，不能以既有40tests全部通過取代。

### PB-build-handoff — PASS

指定版本封存清單包含操作入口/控制程式/五份契約/roles設定/tests/原始要求/設計/准入歷史/驗證與未解範圍，下游可以依blob Digest取得，無須作者聊天。交接必須攜帶D1缺陷及本次FAIL，不能將其當成已接受版本。

## 停止與後續

所有本Reviewer執行的命令均已退出，沒有背景程序、有效exec session或pending工具。此報告與JSON及兩份review證據完成後凍結，不再修改作者成果或正式狀態。JSON stopped保持false；控制者取得本Reviewer完成訊號後才可設true並送交。第一輪必要FAIL應依控制程式保存缺陷及安排唯一一次補件；不能直接接受或先讓handoff讀未接受版本。
