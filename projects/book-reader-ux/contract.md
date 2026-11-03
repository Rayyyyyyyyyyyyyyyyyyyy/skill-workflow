# book-reader-ux 交付契約

來源：PROJECT.md 原始想法 + discussion.md 決策；依據 `critique/2026-11-02T02-20-27Z__site-src-pages-index-astro.md`（25/40）。

## 執行方式與已知缺口

- workbench.py 只接受專案 workspace 或集合根目錄（workbench.py:223），book-reader 是外部 repo。使用者選擇沿用 winter 做法（2026-11-02）：直接在外部 worktree 開發，不經 workbench 正式准入／接受；每項由獨立子代理審查。
- 工作目錄：`/Users/ray.shao/book-reader-ft-immersive-bookshelf`，branch `feat/immersive-bookshelf`，基準 `e0cac3c`。
- 不修改讀書心得原文、私人素材、書籍資料（`site/src/content/books/`、`讀書心得/`、`is-me/`）。不推送、不合併 main，除非使用者另行要求。
- 瀏覽器：使用者授權本次全部驗收以本機預覽站（localhost）+ Playwright Chromium 執行 e2e 與截圖；不操作使用者的 Chrome。Playwright WebKit 不渲染 CSS 3D，Safari／iOS 仍需人工驗收。

## 需求（依序執行）

- R1 distill：列表檢視與書架的「開一本書」一致。列表卡片直接連到 `/book/<slug>`，移除列表專用 2D modal；全站 CTA 用語一致。
- R2 clarify：
  - 心得結尾頁提供下一步：「下一本有心得的書：《…》→」（開啟該書）與收回書架。
  - 「意義・心靈」書架計數改為與其他分類一致（「N 本」）。
  - 底部計數器以頁表示（書名頁／頁碼範圍／完），螢幕閱讀器唸出「頁」。
  - 搜尋無結果時以中文說明並給可行動建議（清除搜尋／看全部）。
- R3 delight：每層書架內有心得的書排前面（各自依高矮），其餘依高矮；有心得的書脊加書籤記號，「讀書筆記」切換旁有同一記號作圖例；無心得的書第二跨頁左頁不留白。
- R4 layout：桌機 1280×860 與手機 390×844 首屏可見第一層書架的書脊；「只看有心得」「書架／列表」與分類集中為同一組篩選；只看有心得時書架不留大片空木格。
- R5 adapt：手機單頁模式點書頁左側往回翻；手機上點背景不收書（以 ×、Esc、返回收書）；開書推入一筆歷史（網址不變），瀏覽器返回＝收書；書架可橫捲有視覺提示；開書時焦點鎖在書內；書脊焦點框在淺色書脊上清楚可見。
- R6 polish：偵測器標出的真實低對比文字（ONE HUNDRED、書架數量、英文分類名、作者、頁碼、藏書票小字）達 WCAG AA（4.5:1，大字 3:1）；不改判為誤報的裝飾（書脊 3D 面、條紋紙紋、米色系）。
- R7 不退化：既有 e2e（依意圖更新後）全過、`astro check` 0 錯誤、build 成功；書頁、RSS、sitemap、OG 照常；減少動態效果仍有效；使用者已核准的書架視覺方向（米色頁面、暖木書架、排版式封面、網址不變）保留。

## 驗收方式

每項完成後：`astro check`、`npm run test:e2e`、桌機與手機截圖；由未參與實作的子代理對照本契約與 diff 獨立審查（PASS／FAIL／UNKNOWN 逐項附證據），FAIL 必修後再審，最多兩輪；之後 commit。
