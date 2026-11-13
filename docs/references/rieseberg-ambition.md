# 參考：Felix Rieseberg〈How to be more ambitious: A tutorial for humans with models〉

- 原文：https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/（2026-10-13，作者是 Anthropic EM，帶過 Claude.ai、Cowork、Claude Code Desktop）
- 社群把它做成的 Skill：`robonuggets/be-ambitious`（https://www.skills.sh/robonuggets/be-ambitious/be-ambitious），沒有安裝，只參考它的規則。
- 2026-11-13 讀原文後，依它修改了 `docs/WORKFLOW.md`；修改紀錄在 `projects/workflow-autonomy/LOG.md`。

## 原文重點

野心分四種：Speed（同樣的事做更快，原文略過）、Altitude、Depth、Range。

- **Altitude**：往上一層抽象，看結果，不看單一任務。問「之後希望發生什麼？目標背後的目標是什麼？」他的例子是從「修這個 crash」改成「讓 app 保持零 crash」。要做到這點得先改工作流程：讓 Claude 能抓 crash report、對應版本和 commit，並給它 Windows、macOS、Linux 機器自己重現和驗證。判斷方法：這件事會需要開會討論，就適合往上一層。創作類比較不適用；「Claude, go make money」在 2026 年對多數企業還做不到。
- **Depth**：照頂尖專家的方式做，碰底層的資料和工具。
  - 堅持用業界最好的工具：模型被要求「像專家」時，常常只換術語、不換方法。它拿出 markdown 表格時，要求改用資料庫和統計模型。
  - 訂不合理的目標，並告訴模型這很合理，例如 10 秒的載入時間要求做到 200ms。
  - 挑戰已知：給原始資料，請它反向檢驗假設，例如「我們認為流失是 onboarding 的問題，試著從原始資料重現這個結論」。
  - 產生新知：建立模擬，找出還不知道的早期訊號，並在沒用過的資料上證明它有預測力。
  - **外部判準**：「Do not ask the model to judge itself.」最好是模型能自己跑、立即得到回饋的工具。
  - 他常用的 prompt（原文）："I want a deeper version of this task, not a bigger one. Before rewriting it: (1) say what a top professional in this field would do here that I'm not asking for; (2) name the rawest material they would start from instead of what has already been digested for me; (3) name the specific methods and tools they would use; (4) say what, other than you or me, would show the result is right. Then rewrite my prompt to ask for exactly that."
- **Range**：從多個領域看同一件事。
  - 把名詞換成動詞：簡報不是「一份 deck」，而是「在 30 分鐘內讓忙碌的人相信一個因果故事，並在不確定中做出決定」。
  - 組隊：分析師、記者、編輯，再加上紅隊（做空研究員、鑑識會計）。
  - 避免角色扮演："Don't ask the model to write like a short seller, ask it to do what a short seller does to research their position."
- **共同前提**：模型要有一台能安裝軟體的電腦，並能存取相關資料（MCP 或其他方式）。

## 對應到本 repo 的修改

| 原文 | `docs/WORKFLOW.md` |
|---|---|
| Altitude：目標背後的目標 | 第 2 節：完成線寫使用者原話範圍內的結果；往上一層的版本當選項問使用者 |
| Depth：四問 prompt、外部判準 | 第 2 節：每條完成線都要有外部判準，並用四問挖深；PROJECT.md 格式 |
| Altitude 的前提：先接好資料與驗證環境 | 第 4 節：進迴圈前先接好基礎建設 |
| Depth／Range：不要角色扮演 | 第 3 節：角色庫用方法，不是換口吻；跨領域用「名詞改成動詞」 |
| 不讓模型自己判 | 第 5 節與 `.claude/agents/reviewer.md`：照外部判準重跑取證；「使用者判定」的判 UNKNOWN |

沒有採用的：「訂不合理的目標」（與本 repo「範圍擴大要先問」相衝，且容易讓 Agent 宣稱達標），以及 Speed。
