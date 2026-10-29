# awesome-design-md 調查

`awesome-design-md` 適合當作專案的視覺參考輸入。它提供不同網站設計語言的 `DESIGN.md` 分析文件；在這次固定版本中沒有 `SKILL.md`、執行引擎或安裝流程，因此應和執行方法的 Skills 分開看待。[README](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/README.md)、[完整檔案樹](https://api.github.com/repos/VoltAgent/awesome-design-md/git/trees/84becd0fc3b6c3646093fcf65d4d62637e09aabc?recursive=1)

## 問題、範圍與來源品質

- 調查問題：這個 repo 實際提供什麼、如何使用、和本機既有設計 Skills 如何分工，是否值得加入目前 Flow 的候選輸入。
- 查核日期：2026-10-29（Asia/Taipei）；固定 commit `fcc70284932276d085f01ef9f83edde90b1258cb`，其提交日期為 2026-10-28T15:45:37Z。
- 納入：固定 README、LICENSE、未截斷的完整 Git tree；實讀 Claude、Linear、Stripe 三份設計文件；讀取五份本機設計 Skill 的完整主檔作為比較資料。
- 排除：星數與排行不作適用性證據；沒有讀完其餘 81 份設計正文，也沒有檢查原品牌當下網站、執行預覽、下載字型或執行來源中的命令。
- 權重：Git tree 與實際文件是「該版本包含什麼」的一手證據；README 是作者對用途與能力的說明，不能證明生成品質。第三方品牌分析仍是作者的觀察／詮釋，不當作品牌官方設計規範。

來源路徑、五份實讀遠端文件的 Git blob SHA／SHA-256、五份本機主檔 SHA-256、84 份設計路徑與統計存於 [sources.json](sources.json)。GitHub 回傳的五份文字已重新計算 Git blob hash，全部與固定 tree 對應，沒有只記一個可變 main URL。[固定提交](https://github.com/VoltAgent/awesome-design-md/commit/fcc70284932276d085f01ef9f83edde90b1258cb)

## FACT：實際內容

完整 tree 回應 `truncated: false`，共 260 個 entries，其中 173 個 blob 檔案、84 份 `design-md/*/DESIGN.md`、0 份 `SKILL.md`。內容涵蓋 Claude、Linear、Stripe、Vercel、Notion、Apple、Figma 等品牌／網站；這是不同設計語言的參考集合，不是本機已安裝的 84 個 Skills。[完整檔案樹](https://api.github.com/repos/VoltAgent/awesome-design-md/git/trees/84becd0fc3b6c3646093fcf65d4d62637e09aabc?recursive=1)

三份實讀文件均以 `version: alpha` 的 YAML 前置資料列出語意色彩、字級、間距、圓角與元件；正文再描述排版、表面層級、響應行為與迭代注意事項。不同文件有差異，不能因 README 列出共同章節，就假定所有 84 份同樣完整。[Claude 文件](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/design-md/claude/DESIGN.md)、[Linear 文件](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/design-md/linear.app/DESIGN.md)、[Stripe 文件](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/design-md/stripe/DESIGN.md)

| 實讀範例 | 文件描述的方向 | 不能據此宣稱的能力 |
|---|---|---|
| Claude | 暖奶油底、珊瑚色主動作、襯線展示字體、深色產品展示面板 | 該文件明列 Claude 聊天介面、訊息工具／上傳／歷史側欄、部分表單驗證與動畫不在萃取範圍，不能直接當完整聊天 App 規格 |
| Linear | 近黑畫布、灰階表面、少量薰衣草藍、產品畫面主導的行銷構圖 | 明列行銷站未含 light theme，部分表單錯誤與產品內標籤色盤未涵蓋，不能當完整 issue tracker UI 系統 |
| Stripe | 靛色動作、深海軍藍文字、漸層網格、細字重與數字排版 | 前置名稱寫成 `Stripi-Inspired-design-analysis`，屬 inspired interpretation；不能把數值、可用性或其響應／字型說明直接視為 Stripe 官方保證 |

以上每列依據為對應範例的前置資料、正文與 Known Gaps（若有）；不是對三個品牌實站的獨立量測。[Claude](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/design-md/claude/DESIGN.md)、[Linear](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/design-md/linear.app/DESIGN.md)、[Stripe](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/design-md/stripe/DESIGN.md)

## FACT：README 與 tree 的差異

README 的檔案表說每個網站包含 `preview.html` 與 `preview-dark.html`；但這次固定版本的完整 tree 中找不到任何 preview HTML，實際是 Markdown 文件集合。因此不能告訴使用者 clone 後已有那些預覽可開，或拿未執行的預覽當成設計品質證據。[README 檔案表](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/README.md#whats-inside-each-designmd)、[完整 tree](https://api.github.com/repos/VoltAgent/awesome-design-md/git/trees/84becd0fc3b6c3646093fcf65d4d62637e09aabc?recursive=1)

## FACT：使用方式與授權

README 建議選一個網站的 `DESIGN.md`，放到自己的專案根目錄，明確要求 Agent 依它做設計；不需要為這些文字安裝 Skill。這是作者建議的使用方式，並不保證所有 Agent 都會自動載入名為 `DESIGN.md` 的檔案。[使用說明](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/README.md#how-to-use)

repo 的 LICENSE 為 MIT、copyright 2026 VoltAgent，條文要求保留適用的著作權及許可通知；README 另明示分析文件按現況提供，作者不主張擁有各站視覺識別。這些說明不等於本次已替任何商標、logo 或專有字型確認取得權利；Claude／Linear／Stripe 範例也各自談到專有字型或替代方案。[LICENSE](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/LICENSE)、[README 授權說明](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/README.md#license)、[Claude 字型與缺口](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/design-md/claude/DESIGN.md)

## FACT：和本機設計 Skills 的分工

以下是讀取本機完整 Skill 主檔後的功能比較；不是執行過各 Skill 的品質測試。來源的實際路徑與內容 SHA-256 在 sources.json，作為這次盤點時點的資料依據。

| 既有方法 | 主檔實際要求／提供 | 與 DESIGN.md 的關係 |
|---|---|---|
| [claude-design](/Users/ray.shao/.codex/skills/claude-design/SKILL.md) | 先確定目標、工作流程、畫面結構、視覺層級與操作狀態，再依既有系統實作 | 可用所選 DESIGN.md 作視覺方向輸入；需求、流程與狀態仍由專案決定 |
| [ui-ux-pro-max](/Users/ray.shao/.agents/skills/ui-ux-pro-max/SKILL.md) | 以本地搜尋／資料提供 UX、色彩、字型、圖表與技術棧建議，區分新系統與單點問題 | 可補齊參考文件以外的操作／可用性問題；不能在已有固定設計決策時任意覆寫 |
| [design-taste-frontend](/Users/ray.shao/.agents/skills/design-taste-frontend/SKILL.md) | 有方向抽選、主題概念、構圖、素材、house rules 與瀏覽器檢查；既有品牌可明確保留 palette/type 並對特定規則例外 | 與選定品牌參考可能衝突，需先界定視覺主準則，不能同時把兩套規則都當無條件最高準則 |
| [impeccable](/Users/ray.shao/.agents/skills/impeccable/SKILL.md) | 依現有產品與 DESIGN.md／surface brief 做規劃、製作、批評或精修；固定 brief 優先，採有限驗證回合 | 適合在已決定方向後使用專案化的 DESIGN.md；實際工具與瀏覽器步驟仍受本次授權約束 |
| [popular-web-designs](/Users/ray.shao/.codex/skills/popular-web-designs/SKILL.md) | 依頁面目的研究當代範例，抽取模式並適配自己的產品與既有元件 | 此 repo 可提供一批候選參考；固定歷史分析不能代替當下實站研究 |

## INFERENCE：適合目前 Flow 的接法

將它視為 design task 的參考輸入，比再增加一套同時控制畫面風格的 Skill 更貼合現有分工：Skills 提供如何設計與查核的方法，所選 DESIGN.md 提供該次想採用的視覺語言。這個判斷來自固定 tree 中沒有 Skill 入口，以及上述方法已覆蓋規劃／製作／檢查。

建議先挑一份與產品用途相符的參考，將想保留與要調整的部分寫成自己的專案 DESIGN.md；記錄原 URL／commit 與來源通知，再把該檔加入正式計畫的固定輸入。是否採用、採哪份仍是候選決策；本次沒有替使用者選定品牌或改動 Flow／安裝任何東西。

一個具體衝突是：`design-taste-frontend` 的 page house rules 排除漸層、靛／紫色、奶油底配陶土色；三份參考卻分別採用這些元素或近似元素。它的既有品牌例外可處理明確的品牌約束，但「借用某品牌參考」本身不會自動變成使用者的既有品牌。先確認專案 brief 與適用例外，能避免 Agent 一邊套用參考、一邊把參考最重要的特色刪掉。[本機 house rules／Special cases](/Users/ray.shao/.agents/skills/design-taste-frontend/SKILL.md)、[Claude 參考](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/design-md/claude/DESIGN.md)、[Stripe 參考](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/design-md/stripe/DESIGN.md)

## UNKNOWN／未執行

- 尚未驗證任一 Agent 用這些文件生成 UI 的效果，也未核對所有 token 與現行品牌網站一致；不能由 repo 受歡迎程度或文件細節推導實作正確性。
- 沒有執行文件中的 npm／lint 建議、下載或執行任何外部程式；沒有安裝、移除或更新本機 Skills。
- 沒有操作瀏覽器、預覽、截圖或跑視覺驗證，也沒有修改既有產品或替使用者發布成果。
- 研究結論只涵蓋指定 commit 的檔案結構、三份範例與已讀本機 Skill 指引；後續版本應重新查核 tree、正文及來源。

本交付可支持「把它列入視覺參考候選，按專案挑選」的決策；不能支持「已整合／已安裝、會自動生出正確 UI、或能替代既有需求討論／可用性查核」的宣稱。
