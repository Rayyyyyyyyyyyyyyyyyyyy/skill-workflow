# Build 第二輪指定版本獨立查核

結論：11項PASS，沒有剩餘必要FAIL或UNKNOWN。第一輪D1已以真Git task隔離及整合後驗證解除；本判定只支持本次build提交，正式接受仍由控制者執行，未完成的handoff及Project整體不能由此宣告完成。

## 固定對象及獨立性

- Reviewer：`/root/independent_review`，未參與作者工作，且不在本版contributors清單。
- review_id：`25143b5ba30d45b8be53647392a9a68b`，round=2。
- submission_digest：`c9a51be8d5856c0e13e1eef5f5deed77f88456cdfc3f63a4f95b18bf1f555339`。
- contract_digest：`8846d1784bcf8b2c375c931388637fda8954f51ad49221fec06654bc8568044d`。
- baseline_digest：`5ba4fa11c8f7f9bb3fffc66ccb7a7fa222c254f87d450b068167fddf93a5f8be`。
- 原plan_hash：`adea5330090998bb349a270db5661a416814c1b5fd198a12d64da6fca99d9b34`，原11項與第一輪固定契約相同。
- Git base：`c670ae2dc345f3e2d870b60b57bf6840eee53c7c`；提交commit：`d75e09c36a945c6d82d4b59de2f6365f1743367c`；tree：`8980fffa679aad0b3a3a45d304859289fa425731`。
- Reviewer工作區：`/Users/ray.shao/workflow/projects/workflow-hub/tasks/build-review-25143b5ba30d45b8be53647392a9a68b`，實際HEAD為上列提交、detached且與作者目錄不同。

FACT：從完整packet解析原始要求、固定task/acceptance、所有來源參照；以submission.files的blob為權威，重算43份檔案Digest並與detached工作樹內容逐份核對，manifest與baseline亦重算相符。讀取packet完整原生Code Reviewer、P00及review Playbook；對照封存REQUEST、USER_GIT_TASKS、VALIDATION-v2、六份Playbook、七個Role設定、GitMaster補充原文、完整workbench.py/library/git_tasks.py、測試與入口操作文件。GitMaster封存TOML與實際安裝來源位元一致。固定sources仍是歷史baseline，不把可變路徑讀取當成pin。

FACT：原task保留兩份submissions；第一份仍為68ecc05e…，本版generation=2、round=2，第一輪FAIL及反例在提交中仍存在。沒刪驗收、沒重置輪次，也沒有增加Reviewer。

## D1重查與真實Git鏈

FACT：第一輪的雙作者同workspace反例已被新dispatch的每task/Attempt獨立branch/worktree取代。48案中的 `test_independent_tasks_run_together_in_distinct_git_worktrees` 明確讓兩個task同為RUNNING、操作同名shared.txt但各自保存不同內容，來源目錄不被修改；此非全域串行lock。

FACT：讀private Git實際metadata確認runtime作者worktree為tasks/git-runtime、branch=codex/workflow-hub/git-runtime-1、head=f7b223684d8be17a7a813d2f95e2c6651a26cb5b；tests/docs作者另在tasks/git-tests-docs、branch=codex/workflow-hub/git-tests-docs-1、head=6f0e5477e9800a24140aee1531b2e38053d11900。第三整合worktree為tasks/integration-v2，與上述兩者及Reviewer工作區皆不同。git-bootstrap及integration記錄的四個來源commit均在private repo可解析。實際本次建置/並行時序依host收據與其記錄歸因；Reviewer沒有把事後metadata宣稱為自己觀察到整段時序。

FACT：本版交付清楚標示host bootstrap的界線；舊controller尚無Git支援時由host建工作樹，再使用公開adopt-git綁定有效Attempt及固定base，沒有假稱舊dispatch早已做到。後續正常計畫由controller.initialize/start提供私有baseline與獨立worktree，多來源要求integrate、僅從已接受輸入commit開始；產物綁repo/base/commit/tree/changed_paths，Reviewer查固定提交而不是作者後續HEAD。

FACT：封存README/WORKFLOW及integrate契約明文要求Reviewer查整份Git差異；submission.files是明列產物索引，完整提交樹及19份changed_paths同樣被固定，回寫的是接受後終端commit的允許差異。已讀取全部新增/變更程式與相關文件，未只看作者摘要或--files清單。

INFERENCE：D1正常作者共用目錄互覆的根因已解除；Git私有物件庫的共用不等於共用作者工作目錄。此隔離只防正常協作互覆，不推廣成同OS惡意Agent隔離。

## 整合、恢復與來源保全證據

FACT：新公開測試覆蓋兩個來源各自接受後整合，個別PASS及整合accept均不提前完成Project；終端整合Proof與安全apply後才DONE。衝突留下WAITING/GIT_MERGE_CONFLICT、衝突檔與所有作者目錄，沒有先覆寫來源。整合後的完整48案在本Reviewer指定提交上再次執行通過。

FACT：另在temp使用同份封存test helper做三項獨立定點檢查：(1)兩個已接受來源衝突，解決並git add後resume仍使用原Attempt，提交/Proof/apply後來源為解決版；(2)第一輪FAIL後新Attempt的base等於原拒絕提交commit，保留原檔案後產生第二版，round=2且兩份submission均在；(3)prepare接受後等待delivery，新plan的首task帶前次固定commit及接受receipt。三項皆PASS，記錄在build-review-targeted-v2.json；這是控制行為測試，未把fixture的PASS稱為真實產品語意Proof。

FACT：apply先檢查所有差異目標的baseline/target內容及mode、拒絕symlink/使用者新內容，再逐檔替換；來源修改測試確認任一目標衝突時不先寫其他檔。來源Git的HEAD/index沒有被reset/stash/stage，保留staged/unstaged/untracked及刪檔的測試通過。真實主repo目前HEAD與index SHA亦重新核對為bootstrap的26f593210f5e8c37a14ae795aa6b203f0e6178ea、eaea3723534e75eb55e9949b25d01b2efe8a7a05595aae4f9647ce48ea1525e9；source-apply-v2收據的保全聲明有此限定範圍支持。

限制：逐檔回寫不是多檔原子交易，host須排除回寫期間其他來源writer；中途程序/硬體故障需依紀錄核對已變動範圍，不能宣稱回滾或盲重跑。Git/SQLite/blob均需備份；這些限制已寫入成果。沒有把host收據當OS程序樹Supervisor、也沒有把SHA一致性當語意真實性保證。

## 實際執行的驗證

FACT：在上述detached worktree，以Python3.14.0執行 `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`，48tests，19.909秒，exit=0；逐項輸出在build-review-test-v2.txt。檢查原始測試diff確認40個既有方法未刪，修改主要是工作目錄/新apply終點配合及新增8案，不是改弱預期來遮D1。

本Reviewer新增證據共4檔，全部列入report.evidence：本報告、build-review-test-v2.txt、build-review-git-v2.json、build-review-targeted-v2.json。JSON報告本身依控制者要求放在controller根目錄records，沒有放進Reviewer工作區混成作者交付。

NOT_RUN：未重跑沒有新疑點的舊runtime-reference41案；它們與新48案分開歸因，不相加冒稱原完整規格23案例皆通過。未做瀏覽器、發布/部署/外部寫入/付費、敵意Worker沙箱、精確帳單或跨主機災難恢復。本輪一次ps程序盤點被受管理環境拒絕；自己的同步subprocess returncode、完成log及已退出工具結果可支持本次命令結束，不宣稱完成獨立OS程序樹驗證。這不構成此CLI交付的必要UNKNOWN。

## 11項驗收

### AC-R1 — PASS

new仍保存原idea且拒絕同名覆寫，原REQUEST保留；Git baseline從當前選定來源bytes建立，包含新檔/既有未提交內容且保留刪檔，不取來源舊HEAD。獨立48案中的Project保全、重啟、來源Git staged/unstaged/untracked/deletion案例通過。

### AC-R2 — PASS

AGENTS/WORKFLOW及clarify/research/design/deliver維持成熟度選路，missing_inputs不派作者；prepare完成仍等待delivery。獨立測試及定點prepare→deliver檢查確認已接受commit與receipt承接，沒有把釐清成果當原目標完成。

### AC-R3 — PASS

六份Playbook現包含integrate，各有明確必要輸入/階段/停止/criteria/交接；DAG、最低criteria及已接受上游gate保留。正常並行作者有不同Git branch/worktree，整合只從固定已接受來源開始，衝突WAITING並保留，同一Attempt解決後續行；組合後需獨立Proof及apply。

### AC-R4 — PASS

正式packet的原生Reviewer/P00/review完整內容實讀，歷史作者Role/Skills快照與pin保留；新增integrator綁實際Git Workflow Master，封存TOML與安裝來源bytes一致，7個Role配置未冒稱全部領域品質已證明。角色及技能不授權遠端操作，工作區及controller入口明確分離。

### AC-R5 — PASS

第二輪manifest、43個blob/工作樹內容、baseline及Git base/commit/tree/changed_paths核對相符；Reviewer在指定提交的獨立detached worktree審整份差異。review/accept保留6欄綁定、每項證據、不同作者、自審/舊版本/竄改拒絕；真實本輪獨立Review未提前當接受或下游完成。

### AC-R6 — PASS

原有checkpoint/pause/resume、UNKNOWN同版本恢復、兩輪/兩重試/四作者上限測試保留並通過；真實task generation2/round2與第一版FAIL/submission仍在。另驗證補件從第一版commit建新branch並保留兩版，prepare承接固定版本，整合衝突同Attempt恢復；adopt-git公開接管而未直接改狀態。

### AC-R7 — PASS

入口、CLI、文件均交代controller_root/source_workspace/packet.workspace及Git需求；43檔封存包含程式、6契約/7Role配置、測試、原要求、Git追加指示、來源/整合/回寫紀錄、第一輪證據與新驗證。下游可由已接受固定commit接手；未要求或宣稱尚未執行的HANDOFF完成。

### PB-build-requirements — PASS

六步及R1–R7的節點責任保留；依使用者追加Git小任務指示修正D1，實際兩作者分離branch/worktree與第三整合工作樹可查，沒有以全域串行lock替代。原11驗收/plan_hash、第一輪FAIL及第二輪綁定均保留；本PASS限build交付，不含尚未接受的handoff或Project整體。

### PB-build-integrity — PASS

D1已修正：新dispatch每Attempt唯一branch/worktree，回歸證明同時RUNNING作者可各寫同名檔而不互覆；fixed Git版本接受後經整合Proof及逐檔預檢回寫。測試保留來源HEAD/index與既有staged/unstaged/untracked/deleted內容，來源途中變動時全檔預檢拒絕；真實來源HEAD/index與bootstrap receipt相同。非多檔原子/同OS非敵意隔離限制如實揭露。

### PB-build-verification — PASS

獨立對d75e09固定worktree重跑完整48tests，exit0、19.909秒；原40個測試方法未刪，新8案覆蓋Git隔離/整合/衝突/固定Review/安全回寫/legacy。再獨立跑三個恢復/補件/prepare定點案例皆PASS，實際log與版本固定；舊41參考測試未重跑且不相加冒稱完整23案例通過。

### PB-build-handoff — PASS

封存可重現入口、完整程式與契約、固定Git來源及整合commit/tree、逐命令驗證、限制與下一步；接手者從accepted build commit建立自己的worktree並讀原始要求，不用作者聊天作唯一依據。真實handoff節點仍待本版正式接受後啟動，來源apply與整體DONE另有明確gate。

## 停止及下一步

Reviewer未修改作者程式、測試、正式驗收或controller狀態。所有本次驗證命令已退出，沒有背景程序或待完成工具；本報告與三份新證據寫入後凍結。report.stopped先為false，控制者取得本Reviewer完成訊號後才可改true送交。

本輪沒有剩餘必要缺陷；只可由控制者按固定第二輪接受此build提交。其後真正handoff必須讀已接受固定commit、產生自己的交付並獨立驗收；全部必要task接受且安全回寫前，Project仍未完成。本PASS不是發布或擴權授權。
