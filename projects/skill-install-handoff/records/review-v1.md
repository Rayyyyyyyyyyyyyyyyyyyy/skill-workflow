# Claude 技能安裝交接文件：獨立 Proof

判定：**PASS，七項必要驗收全部通過**。這只接受固定文件交付；不表示清單內技能已安裝、Claude 雲端原生載入或功能已通過。

## 綁定

- Project/task：`skill-install-handoff / write`，round 1。
- Reviewer：`/root/install_catalog_reviewer`；作者為 `/root/install_catalog_writer`，上下文與作者分開，未修改產品。
- 固定 submission commit：`7fd8c20a4128254001ef01d0d7cdb266d24e1e2c`；tree `5312fb69b619ed71eaa072e24e2d487129b7ac57`。
- submission digest：`48b4685fa017e5bcd3dfe809d3a1ab9500bd53c9381d32cc1f454c86c41f110b`。
- contract digest：`2c25307ea2258225313c887d96c27cdc5f0cc35bd38e239ffaa25a8ec5364681`；baseline digest：`52150bb2e1f1cb05786a7c12a4b9743f47bef03fec0910f4bfb7a15fcf9d2086`。
- 查核以原使用者改變後的要求為準：取消打包，列出安裝清單給 Claude 後續處理；排除 Codex 外掛／CLI 專屬工具，本次不安裝、複製角色庫或改 Flow。

## 實際查核

1. 在指定 detached worktree 核對 HEAD、四份提交檔 SHA-256 與固定 commit 的 bytes。差異恰為 README、雲端指南的一行入口、新安裝指南及 validation.md；沒有 Skills、Roles、runtime 或設定變更，`git diff --check base commit` 通過。
2. 從固定 supporting source 重算：已附 10、未附 29、Claude 同步 13、排除工具 6；未附集合恰為 15 Matt + Agency／Graphify／Impeccable 3 + 未確認來源 11。逐一對照文件名稱，沒有把同步／備份或上游新增項當成本次缺項。
3. Matt 表格恰有 15 個缺項，逐筆比對固定 commit `59db609eb1e18aaf59b63284d0e52255aff0c63c` 及目錄路徑。獨立透過 GitHub connector 取得未截斷 tree `905b82656daa8179a20c737db3aeed704f8be22c`，確認 21 個本機系列名稱的 SKILL.md 及根 LICENSE 存在。
4. 獨立讀取 21 份本機主檔，重算 SHA-256／Git blob SHA，與來源快照和遠端 tree 比較：20 份主檔一致，只有 `setup-matt-pocock-skills` 不同。文件正確把範圍限於主檔，沒有擴為完整套件等同性；六個上游未安裝入口另列，不是必裝。
5. 獨立讀取 Agency 固定 README（`4e3ac3c…`）：支持原生 Markdown 角色庫及 Claude Code 安裝形式；文件沒有把角色安裝混成已還原本機 loader。282 個本機角色數和七個既有別名以固定 source-facts 為本次盤點依據，沒有宣稱本次已安裝它們。
6. 獨立讀取 Graphify 固定 README（`0a8cd4e…`）：支持 Python 3.10+、runtime、project 註冊方式；文件保留新 repo／v8 及本機版本未知。讀取 Impeccable README：支持 `.claude/skills/impeccable`、runtime binary、project/global scope 與 hooks；文件明列可變 main 要在安裝前釘選，沒有承諾版本相同，也沒有要求接受 hooks。
7. 指南的四個相對參照與 README／雲端指南新增的兩個入口均可解析；對 baseline 未含的既有來源，以原 controller root 唯讀確認。GUIDE 指向 source-facts 與完整盤點，接手不依賴聊天；未來 GitHub session 仍需取得包含這些檔案的 branch／commit，現有 cloud guide 已說明。
8. 閱讀可直接交給 Claude 的任務：只處理缺項、保留十份既有方法／七個別名與快照追溯；明確限制全域覆寫、hooks、未知下載執行、瀏覽器、發布／付費等動作。安裝後依實際來源更新雜湊與適用檢查，Proof／固定計畫與權限不被繞過；安裝與執行／可用性驗證被分開。

## 逐項判定

| 驗收 ID | 判定 | 具體依據 |
|---|---|---|
| R1-check | PASS | 所有 10／29／13 名稱及六個排除項與固定輸入一致，15 Matt 缺項與六個未安裝上游入口分清。 |
| R2-check | PASS | 15 Matt 路徑及主檔差異獨立核對；Agency 角色庫／loader、Graphify runtime／改名、Impeccable 可變 main 與十一個 WAITING_ORIGINAL_SOURCE 均保留實際來源及未知。 |
| R3-check | PASS | 安裝接手任務與兩個入口可用；只文件交付，保留既有快照、固定 Flow／Role／Proof 和原操作界線，不授予自動全域或外部動作。 |
| PB-write-requirements | PASS | 固定四份差異完整交付安裝清單與可發現入口，沒有恢復已取消的打包工作，也沒有擅自選裝其他技能。 |
| PB-write-integrity | PASS | 文件來源、未知、版本限制與使用者意圖都保留；沒有修改原 Skills／資料／介面。工程功能修改不適用，有四檔差異證據。 |
| PB-write-verification | PASS | 本次在固定 commit 重新驗證 hash、集合、實際遠端 tree／README、相對連結及 whitespace；必要靜態檢查足夠，安裝／雲端／瀏覽器未執行被明示。 |
| PB-write-handoff | PASS | 安裝目標／缺來源狀態、依賴與權限、接手提示及證據入口完整；不把文件存在或本機驗收當作雲端安裝完成。 |

## 未執行與限制

沒有執行 installer、Skill、setup、runtime 下載、hooks、瀏覽器或 Claude 雲端 session，也沒有改動全域設定或發布。這次為文件修改，未跑程式功能測試；實際安裝、原生發現、版本選擇與十一項來源取得仍須由後續接手者在當次條件下處理。Impeccable 的 main 可變，本文不把本次讀取當成永久固定版本。

此報告只提供逐項查核結果；正式接受及安全回寫仍由控制程式處理。
