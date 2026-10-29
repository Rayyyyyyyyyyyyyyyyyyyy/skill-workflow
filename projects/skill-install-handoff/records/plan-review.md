# 安裝交接清單計畫准入查核

判定：**PASS**。這是文件交付的准入判定，不代表任何 Skill 已安裝、來源完整功能已驗證，或正式交付已接受。

## 綁定與獨立性

- Project：`skill-install-handoff`；正式狀態 `PLANNING`，作者 task 尚未派工。
- 正式 `plan_hash`：`6f97256577679a4be532bf06aab3801864b90d81d42f3561bca1e24bd8ab6f96`，取自原集合 `Workbench.status`，不是對原始 JSON 自算。
- Planner：`/root`；Reviewer：`/root/install_catalog_reviewer`，未參與計畫或產品撰寫。
- 原始要求以 `PROJECT.md` 及使用者最新指示為準：取消打包，改列已安裝技能交給 Claude 處理；沿用排除 Codex 外掛／CLI 專屬工具條件。

## 原始要求覆蓋

| 要求 | 計畫對應 | 實際准入觀察 |
|---|---|---|
| R1：完整清單及分類，包含 Agency／Matt | `R1-check` | 固定 source-facts 有 repo 已附 10、未附 29、Claude 同步 13 的完整名稱；21 個本機 Matt 名稱中 6 個已附、15 個未附，上游另有 6 個未安裝入口被分開列出。集合可重算，沒有把備份／插件快取或上游新增項冒充已安裝。 |
| R2：可追查重裝來源與未知 | `R2-check` | 固定資料逐項列 Matt 路徑／commit 與主檔比對結果，Agency 註明角色庫及本機 loader 不同，Graphify 指向改名後 repo，Impeccable 的版本等同性列 unknown；11 個未確認來源項被保留。文件交付不以這些未知全部解除為前提，也不承諾每項皆可重建。 |
| R3：Claude 可用安裝指示及範圍 | `R3-check` | 交付包含獨立安裝指南與現有 README／雲端指南入口，要求只處理缺項、保留既有固定快照與 Flow／Role／Proof、不默換或全域覆寫，遵守原瀏覽器／操作授權；本次 allowed_paths 僅三份文件與本 Project records，不包含 Skill／Role 安裝目錄。 |

## Playbook 與輸入完整性

- 使用 `deliver`／`writer` 符合這次文件目的；四項 `PB-write-*` 最低驗收均保留，與 R1–R3 合計七項，沒有刪減最低門檻。
- 單一 task、空依賴，沒有平行成果整合缺口或要求 Project DONE 才能接受本節點的循環。
- 完成終點是已查核的本機安裝交接文件，不是 Claude 未來實際安裝成功或雲端執行；未知來源會以缺口列出，沒有縮減原交付。
- 正式計畫已固定 writer／humanizer、reviewer、P00、review contract 及所用支援來源。`source-facts.json` 雜湊為 `69cba09fb0aa033215a24fa1c57597d44f7703c9b9bf557a1317e2677b21ec81`，與正式 blob／目前檔案相同；writing-for-agents 來源也逐位元組核對相符。
- Source-facts 是本次作者可用的完整分類／來源輸入；真正上游內容與安裝方法是否被正確表達，仍須交付後對固定文件獨立查核。
- 計畫明列 local 操作、兩輪審查、最多兩次工具恢復與四個作者 Attempts；沒有安裝、瀏覽器、發布、付費或遠端寫入授權。

## 限制

本次只查准入契約與固定輸入，沒有撰寫／修改產品文件、安裝或執行 Skill，也沒有重新測試任何 Claude 雲端能力或操作瀏覽器。此 PASS 不能替代後續指定成果版本的 Proof。
