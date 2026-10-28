# 本次設計討論的採用決定

## 來源

本對話的協作 Agent 最終報告：`/root/flow_design`、`/root/playbook_roles`、`/root/proof_review`。三者均先讀取 repo 的規格與適用原生角色，對下列方案交叉討論；本檔保存採用結論，不保存模型隱藏推理。

## 採用的共同結論

- 由現有 Codex 對話與協作 Agent 實際執行；標準庫 Python 控制正式狀態、固定計畫、封存及接受。這是可信本機協作，不是惡意 Worker 安全隔離。
- Project 保存原始目標；Flow 是固定工作計畫；Playbook 定義可委派/可驗收工作；Role 定義專業責任；Skills 是方法；Proof 以指定版本逐項查核。角色或技能不能授權發布、付費或自行派工。
- 作者工作採 clarify、research、design、deliver；review 作共用獨立查核契約，不形成遞迴 Reviewer。Prototype 作釐清/設計內有界方法。
- 需求清楚可直接 deliver；缺關鍵決策才釐清，缺事實才研究，既有設計不足才設計。選路由 Agent 提案並記理由，程式不假裝可靠理解自然語言。
- 需求覆蓋與 Playbook 最低 criteria 必須保留；Role/Skill/P00/實際使用的支援來源保存內容與雜湊。
- 作者與 Reviewer 的 host ID 不同；所有參與作者工作的人都列為 contributors。封存產物後，Reviewer 查固定版本；正式接受前重算實際證據/產物雜湊。
- 第一輪 FAIL 可一次補件；第二輪 FAIL 等待對齊。必要 UNKNOWN 先恢復同一 review/版本，已知 FAIL 不可抹掉；重啟或換 actor 不重置上限。
- 只有已接受上游才能解鎖下游。Checkpoint、等待原因、原始成果、版本、缺陷與下一步可在新工作階段讀回。
- 角色來源不是假名字：planner=Product Manager、researcher=Research Synthesist、designer=UI Designer、implementer=Minimal Change Engineer、writer=Technical Writer、reviewer=Code Reviewer；以實際載入的 native TOML 內容為準。
- 不無條件套用舊 implement/code-review 組合，避免 commit-only diff 漏未提交成果；新 review 直接對封存版本及完整 acceptance 查核。

## 實作邊界

不恢復使用者刻意刪除的 workflow-mvp。現有原規格及runtime-reference保留供設計追溯；舊Schema/參考測試不是新版API或新版完成證據。

本版不提供外部發布、付費、對抗惡意 Worker 的 OS 隔離、精確費用上限與跨主機恢復。需要此類能力的目標須另行處理缺口，不能靠把operations寫成local就宣稱完成。

## 待獨立驗證

此檔只記錄決定；程式行為、真實 Role/Skill 載入、交付語意與下游接手須分別有測試及獨立 Proof。
