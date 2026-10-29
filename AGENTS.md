# Project 工作入口

這個 repo 是 Project 集合與共用工作體系。收到新想法、接續專案或操作工作狀態時，先讀 [docs/WORKFLOW.md](docs/WORKFLOW.md)，再執行對應流程。

## 共用護欄

- 未經使用者對該次明確授權，不開啟或操作任何瀏覽器做檢測、預覽、除錯或截圖，包含 headless／Playwright／Puppeteer。可執行靜態、單元、建置及 API 檢查；必要瀏覽器驗收未執行就保留缺口。
- 涉及金鑰、權限、持久資料或破壞性操作時，保護敏感資訊、在可信邊界驗證並保留既有資料；影響範圍或必要語意未定時先確認，交代恢復限制。
- 依實際訊號處理等待、空結果、失敗恢復、成功與重複操作；保留可恢復輸入，維持鍵盤及輔助科技可操作性。
- 使用對應需求與風險的最小有效驗證；區分已修改、本機已驗證與外部環境未驗證，明列失敗及未執行項目。

## 每次工作的六步

1. **建立或接續 Project**：先查現有專案；使用者指定專案就接續，只有新目標才建立新 Project。保留原始想法及後續補充，不覆寫既有專案。
2. **判斷成熟度**：目標、交付、驗收與關鍵決策足夠就直接做；記錄選路理由。使用者要討論或想法仍是種子時，走 clarify／planner，以 grilling 分輪培養需求並保存決策；其他關鍵缺口才進研究或原型，不能替使用者回答方向性決策。
3. **組成 Flow**：從 `library/` 選擇適用 Playbooks，固定依賴、輸入、驗收與交付終點。Playbook 內的新工作需求只形成候選，不自行增加 Job。
4. **配置 Role 與 Skills**：讀取實際角色及技能指引，依控制程式輸出的版本快照執行。Role 承擔專業責任，Skill 提供方法；兩者不授予派工、發布或付費權。
5. **用 Proof 驗收**：提交指定版本與實際證據，由不同作者的 Reviewer 獨立查核。透過控制程式接受交付；檔案存在、Agent 說完成或自填 PASS 都不等於完成。
6. **保存並接續**：中斷或受阻時保存 Checkpoint、缺口與下一步。接續先讀正式狀態及固定版本，不重跑已接受的工作、不重置審查輪次。

## 操作規則

- 正式狀態由原集合的 `workbench.py` 管理；即使在 task worktree 內，控制命令也必須指定派工包的 `controller_root`（原入口絕對路徑及 `--root`），不以工作樹內的副本建立另一個集合，不直接修改 `.workflow/`。
- 使用 [P00 實證政策](runtime-reference/policies/P00-GROUNDED-ANSWER.md)：以可追查證據支持結論，區分事實、推論、假設與未知；回報實際完成及未執行範圍。
- 原始要求與 Playbook 的必要驗收不可被作者刪減。修改要求或正式驗收時，保留原紀錄並重新准入。
- 作者與 Reviewer 使用不同 Agent／上下文；Reviewer 取得原始要求、固定成果與基準，不只讀作者摘要。
- 確認實際 Agent 已停止後才使用 `--stopped`。未知退出狀態須保存並等待，不能把租約、聊天結束或等待逾時當作退出證明。
- 瀏覽器檢測需使用者對該次檢測明確授權；未授權時可做靜態、單元、建置及 API 檢查，必要瀏覽器驗收記為未完成。
- 本版支援本機交付。發布、部署、外部寫入及付費不在執行範圍；需要這些能力的目標保存缺口，不能縮小措辭後宣告原目標完成。
- 小任務各用控制命令提供的獨立 Git branch/worktree，只在 `packet.workspace` 及 task `allowed_paths` 工作；可並行任務不共用作者目錄。來源 `source_workspace` 不是作者工作目錄。
- 多分支交付使用明確 integrate task，整合已接受固定 commits，衝突等待並保留工作樹，整合後重新 Proof。所有必要 task 接受且逐檔 baseline CAS 安全回寫後才完成 Project；來源有新修改就等待，不覆寫。
- 保留來源 repo HEAD、index、既有未提交修改與刪檔；不 reset、不 stash、不 stage 主 repo。Git worktree 避免正常協作互覆，不宣稱敵意 OS 隔離。

## Claude 與換環境

Claude 的入口為 `CLAUDE.md`，GitHub 雲端或新電腦先讀 [雲端接手](docs/CLAUDE_CLOUD.md)。Role／Skills 使用 repo 內固定版本；搬移前後以 `scripts/check_portability.py` 查核。不要把缺少本機狀態的歷史 Project 當成新專案覆寫。

## 文件範圍

`docs/WORKFLOW.md` 是當前入口與操作契約。`docs/playbook/` 保留原完整目標設計；其中已刪除實作的連結不代表目前可執行能力。`runtime-reference/` 是獨立參考元件，不直接作為新工作完成的證據。
