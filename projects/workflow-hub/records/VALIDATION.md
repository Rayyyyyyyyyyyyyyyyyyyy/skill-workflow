# Build 作者整合與驗證紀錄

日期：2026-10-28（Asia/Taipei）。作者／整合者：`/root/proof_review`。本任務的角色是 implementer／Minimal Change Engineer，並非獨立 Reviewer。

- Project：`workflow-hub`；task：`build`。
- Attempt：`84dddca412e5492ead50532acc5ed781`。
- 准入計畫：`adea5330090998bb349a270db5661a416814c1b5fd198a12d64da6fca99d9b34`。
- 工作契約：`8846d1784bcf8b2c375c931388637fda8954f51ad49221fec06654bc8568044d`。
- 驗收基準：`5ba4fa11c8f7f9bb3fffc66ccb7a7fa222c254f87d450b068167fddf93a5f8be`。

這是作者的可追查驗證紀錄，不是正式接受。獨立 Reviewer 尚須對封存版本逐項查核，控制者接受 build 後，handoff 節點才能啟動並驗證實際下游接手。這裡不把尚未執行的下游或完整 Project 標為完成。

## 工作來源與本輪實際整合

使用者已確認的六步及這次授權保存於 `REQUEST.md`，採用的設計保存於 `DESIGN.md`。初期討論、初稿及部分測試產生於工具完成之前；本次將它們明列為 bootstrap baseline 重新釘選及整合，沒有倒填它們已由新工具派工。

已完整讀取 build-dispatch packet 中的原始要求、11 項驗收、deliver Playbook、原生 Minimal Change Engineer 的完整角色指引、Ponytail、P00，以及支援來源。16 份 supporting_sources 的內容與 packet 內 SHA-256 相符。它們是重用的輸入 baseline；整合後成果會另行封存，不將工作檔覆寫回初稿。

准入 Reviewer v1 實際回報 FAIL：build 驗收提前要求尚不能啟動的下游產物，且重用來源未釘選。v2 改為 build 交付接手所需版本，真正下游驗證留在 handoff；重用需求、設計及初稿也加入快照。`plan-review-v1.*` 保留 FAIL，`plan-review-v2.*` 保留准入 PASS。准入 PASS 只支持計畫完整性，不代表交付驗收。

這輪整合只在控制程式及測試補強真實輸入邊界。新增兩個公開 API 回歸案例後，第一次實際執行得到 5 個 TypeError：非字串 Role、依賴 ID、task／acceptance 的 requirement ID、review acceptance ID 在 dict／set 操作前未驗證。於原有五條驗證補上字串檢查後，錯誤輸入改為 WorkflowError，交易拒絕且原 Project 狀態保持不變。未新增相依套件、通用框架或外部操作能力。

## 實際執行的驗證

逐條命令、工作目錄、環境、stdout、stderr、exit code 保存於 `test-output.txt`。本輪所有已列檢查 exit code 均為 0。

| 檢查 | 環境與實際結果 | 證據範圍 |
|---|---|---|
| 新版公開行為測試 | Python 3.14.0；40 個測試通過 | Project 保全、准入、成熟度、依賴、Role／Skill／支援來源快照、Proof、恢復與次數限制 |
| Python 靜態解析 | `workbench.py` 與 `tests/test_workbench.py` 兩檔 AST 解析通過 | 語法；不代表行為或安全完整 |
| JSON 解析 | 10 份 library／plan／review JSON 通過 | 檔案可解析；不等同語意完整性 |
| 來源可用性 | 13 筆設定的 Role／Skill 來源可讀；原生 TOML 含 developer_instructions | 本機來源可取得及格式，不代表所有角色已通過真實領域評測 |
| P00 | 政策原檔與既定 SHA-256 相符 | 政策內容釘選 |
| 當前入口連結 | AGENTS／README／WORKFLOW／library README 的 9 個本機 Markdown 目標存在 | 當前入口；不把原設計中指向已刪 MVP 的歷史連結列成可執行能力 |
| CLI smoke | 從另一個工作目錄，以絕對 script 路徑及暫存 `--root` 執行 help／new／list／status，四項成功 | 標準庫命令能在指定集合根目錄使用；暫存專案已清理 |
| 舊契約／P00 參考測試 | 既有 Python 3.13 與本機套件快取；26 個通過 | 僅 runtime-reference 的既有行為 |
| 舊持久化參考測試 | 同上；15 個通過 | 僅 durable-runtime 的既有行為 |

新版可重現命令，在集合根目錄執行：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 workbench.py --help
python3 workbench.py list
python3 workbench.py status workflow-hub
```

新版控制程式只用 Python 標準庫，最低版本為 3.11；本次實際測試版本為 3.14.0。40 個行為測試使用暫存 Project，複製真實 Playbook 結構，將 Role／Skill 來源替換為明示的暫存文字 fixture，因此測試可攜且不依賴個人的家目錄。真實原生角色、Skill 及 P00 載入，另由本次正式 build packet 支持；不能把 fixture 當作角色語意品質證明。

預設 Python 的 `jsonschema` 可用性檢查回報 False。舊參考測試需要此套件，因此使用既有 Python 3.13 及既有 uv 快取內容，未安裝或修改全域環境。兩組參考測試的精確 interpreter／PYTHONPATH／命令均留在 test-output。**舊版 41 個測試與新版 40 個測試是不同範圍，不能相加後宣稱完整 Flow 或原 23 個案例全部通過。**

## 原始要求與 11 項 build 驗收對應

以下是作者提供的查核依據，最終判定由獨立 Reviewer 對提交版本作出。

| 驗收 | 對應成果與觀察 |
|---|---|
| AC-R1 | AGENTS／WORKFLOW 的新建及接續入口；new／list／status 的實際 smoke；同名 Project 保留原始想法與檔案、路徑保護、SQLite 重開測試。本次真實 `workflow-hub` 已由控制者建立。 |
| AC-R2 | WORKFLOW 的成熟度選路及理由、clarify／research／design／deliver 適用條件；清楚需求直接交付、缺輸入不啟動作者、prepare 完成仍等待 delivery 且可接續計畫的測試。CLI 不假裝理解自然語言，選路由 Agent 提出並查核。 |
| AC-R3 | 五份 Playbooks 均保留必要輸入、階段、停止條件、最低驗收及交接欄位；測試驗證漏原始要求、DAG 成環、未知 Playbook／Role、漏最低驗收均被拒絕，只有接受後上游能解鎖下游。 |
| AC-R4 | 本作者實際讀取 dispatch 中的 Minimal Change Engineer、Ponytail、P00；Role／Skill／支援來源變動後仍載入釘選內容的測試；缺來源或政策被改時拒絕准入。Role 名稱及 actor ID 本身不授權工具操作。 |
| AC-R5 | 固定 submission／contract／baseline／review 綁定，逐項有證據才可接受。測試涵蓋作者及歷史貢獻者不能自審、缺／重複驗收、虛構證據、過期版本、封存內容竄改、工作區後改不替換原提交，以及兩輪退出。本次交付的獨立 Review 與正式接受仍是下一關。 |
| AC-R6 | Checkpoint、pause／resume、重開 SQLite、舊 Attempt 拒絕；UNKNOWN 恢復同一 review／輪次、已知 FAIL 不被改寫；兩輪、兩次工具重試、四次作者 Attempt 上限在重啟及換 actor 後保留。准入 FAIL 實際保存、重送去重，跨計畫及重啟不重置兩次失敗上限。取消後晚到 PASS 不能接受。 |
| AC-R7 | AGENTS 自然語言工作入口、README 使用方式、WORKFLOW 的計畫／提交／審查／恢復命令、標準庫 CLI 及測試、build-files 檔案清單，足供下游查找本版成果。此 build 不引用尚未產生的 HANDOFF 當成已通過；真正下游鏈由計畫 handoff 節點驗收。 |
| PB-build-requirements | R1–R7 對應上列成果與限制；原始六步、Playbook／Role／Skill／Proof 分層保留，未把所有目標硬改成先研究、設計或發布。 |
| PB-build-integrity | 新增 Project 不覆寫既有資料；正式變更使用 SQLite 交易、相對路徑與符號連結拒絕、內容雜湊及來源快照。本輪修正限 JSON 邊界驗證與測試；使用者既有刪檔、原規格及參考元件保留。沒有聲稱它能保護同 OS 帳號免受惡意作者修改。 |
| PB-build-verification | 上述最小有效測試、靜態檢查、CLI smoke 及實際輸出已保存；新版與舊參考範圍分開，初次回歸失敗與修復記錄如實揭露。 |
| PB-build-handoff | 下游可從封存清單取得入口、控制程式、完整契約與來源綁定設定、測試、原始要求、設計、准入前兩輪查核及本驗證紀錄；控制者接受後，會以固定版本作下游輸入，無須把作者聊天當唯一來源。 |

## 未執行與限制

- 未開啟或操作瀏覽器，也未執行 Playwright／Puppeteer；本次是 CLI／文件工作，沒有瀏覽器驗收需求。未聲稱 UI 或視覺操作已通過。
- 未執行發布、部署、付費、外部寫入、帳單精度、跨主機恢復或對抗惡意 Worker 的測試。這些不是本次允許的交付能力。
- 同一 OS 帳號下，Agent 能繞過 CLI 改檔；本版是可信本機協作。actor／stopped 是控制者根據 host 實際訊號登記的紀錄，不是強身份認證或程序強制終止。雜湊提供一致性查核，不提供語意真實性保證。
- 自然語言覆蓋、Role 專業表現及 Proof 是否真正支持主張仍需要獨立語意判斷。本次沒有證明所有任意想法、所有 Playbooks 或原完整架構的 23 個案例均可執行。
- Role／Skill 設定指向本機安裝位置；換環境須確保實際來源可用。缺來源時應保存能力缺口，不以虛構角色替代。
- Checkpoint 只保全已登記的檔案及進度，不保證恢復未保存內容、程序、模型內部狀態或不存在的外部效果。
- build 與整個 Project 的獨立接受、實際下游 HANDOFF 在本作者完成時尚未進行；不能由本報告推定完成。

## 下一步

本作者完成後由控制者依真實 host 完成訊號封存 build-files 所列版本，另行派獨立 Reviewer 依完整 11 項 acceptance 查核。接受 build 後再啟動 handoff，讓下游實際讀取已接受的封存成果、產生 HANDOFF，並走自己的獨立 Proof。Reviewer 若指出缺陷，依原兩輪及已保存版本處理；本作者不自行批准交付。
