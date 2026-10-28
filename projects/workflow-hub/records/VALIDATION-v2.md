# Build 第二輪：Git 小任務整合與驗證

這是控制者的整合紀錄，尚不是獨立審查或正式接受。原始六步、11項build驗收與第一輪缺陷均保留；沒有重置plan_hash、作者上限或審查輪次。

## 第一輪必要缺陷及使用者指示

獨立Reviewer實際重現共用workspace雙寫：第二作者覆寫檔案後，第一task會封存第二作者的內容。原提交因此被判FAIL，沒有接受；報告及重現保留於build-review-v1.md與對應證據。使用者隨後指示「拆小任務開git task啊」，保存於USER_GIT_TASKS.md。

## 這次實際做的Git工作

- Host從當前70份真實檔案建立私有baseline `c670ae2dc345f3e2d870b60b57bf6840eee53c7c`，包含未追蹤新檔，已刪檔仍不存在；沒有以來源舊HEAD代替當前內容。
- `/root/proof_review`在獨立branch/worktree實作runtime，commits `7b9267b8faf1a478eb7e8b7bb62f4402da88fb1c`、`f7b223684d8be17a7a813d2f95e2c6651a26cb5b`。
- `/root/flow_design`在另一branch/worktree實作測試、整合Playbook/Role與文件，commits `03c4d759b9ed255ed6d3d7f8a8a4b5ea6c138736`、`6f0e5477e9800a24140aee1531b2e38053d11900`。
- 兩作者工作區互不相同，實際並行工作；結束時各自worktree clean且工具命令全部退出。Root在第三個worktree依序cherry-pick，測試對象commit `b1f3e18af1d779ac07050940d4358f4f7c750347`。這是host bootstrap整合，沒有倒稱舊controller本來就會建立Git task。

## 已實作與驗證

1. 新任務使用私有Git baseline及每task/Attempt獨立branch/worktree，packet同時區分controller_root、source_workspace、實際workspace。
2. 每task限定allowed_paths；submission綁定base/commit/tree/changed_paths及內容雜湊，Reviewer使用固定commit的detached worktree。
3. 多來源交付明列integrate Playbook與integrator Role，來源須已接受；衝突WAITING且保留工作樹，整合後仍需獨立Proof。
4. apply先對來源逐檔預檢，基線與target皆不符就拒絕；不操作來源repo的HEAD/index/stash，重送已套用內容可辨認。
5. FAIL補件、checkpoint及prepare→deliver承接精確Git版本與接受紀錄；舊controller的active Attempt可用公開adopt_git接管，未派出的舊task只繼承原已准入scope。

Root對合併後的固定版本實際執行完整48個測試，全部通過（19.765秒）；命令、Python版本、輸出及exit code留在test-output-v2.txt。原40個控制行為案例保留，增加Git隔離/整合/衝突/固定版本/安全回寫與legacy接續等8個案例。

作者另以暫存專案檢查補件保留前版、prepare接受版本承接、衝突解決後同Attempt續行及舊controller接管；這些是作者回報的定點檢查，與Root直接執行的48案分開歸因。舊runtime-reference的41個測試證據保留於第一版VALIDATION/test-output，原參考元件未改，不將其和新版48案相加冒充完整流程通過。

## 回寫與後續

安裝待驗收版本只允許baseline到整合版本的實際差異，先逐檔CAS檢查；若來源已被修改則停止。實際回寫結果與來源HEAD/index保全會另存source-apply-v2.json。所有小任務及整合都未push、未部署或付費，也未執行瀏覽器。

第二輪仍須由未參與作者工作的Reviewer核對指定提交與全部11項驗收；build接受後才會派出真正handoff，不能預先稱整個Project已完成。

## 明確限制

本版為可信本機Agent協作；Git worktree隔開正常任務的可寫目錄，沒有提供同OS身分的惡意Worker安全隔離。回寫不是多檔原子交易，不能同外部writer並行回寫；備份必須包含project控制庫、private Git與blob，主repo的commit不等於完整執行資料備份。其餘Playbook的所有領域/正式環境品質、原完整規格23案例、發布、帳單、跨主機恢復均未宣稱驗證。
