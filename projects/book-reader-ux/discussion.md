# book-reader-ux 討論紀錄

## 2026-11-02 使用者決策（impeccable critique 後提問）

- 優先方向：一致與文字。
- 書架定位：心得書放前排（維持 111 本，每層有心得的排前面並標示）。
- 範圍：全部 5 項，之後 polish 收尾；「全部依序執行」。
- 流程：沿用 winter 做法（外部 worktree，不走正式 plan/dispatch/accept）。
- 瀏覽器：授權本次全部驗收（本機 Playwright Chromium）。

## 作者預設（可被使用者推翻）

- R1 列表卡片直接開書頁，而不是在列表也播 3D 開書（列表沒有書脊作為起點）。
- 首頁介紹文案屬使用者原文，不改字，只調排版；「每本書的背後，連結著我自己的讀書心得」承諾大於現況一事交使用者決定。

## 執行紀錄
- 2026-11-02 R1 distill 5a3403b → 獨立審查 PASS（以 git archive 快照建置驗證；e2e 11/11）。建議採納：列表卡片加書籤記號（併入 R3）、從書頁返回保持列表檢視（併入 R5）。
- R2 clarify 5162aef 送審中。R3 delight 75629e1 + 列表記號。
- R2 clarify 5162aef → 獨立審查 PASS；應修 2 項（奇數頁結尾未標「完」、空結果按鈕後焦點掉到 body）已修。
- R3 delight 75629e1+983f800 → 獨立審查 PASS（書籤尾端屬於該書按鈕，保留）。
- R4 layout fe12773 → 獨立審查 FAIL：桌機分類列被擠出（意義・心靈不可見）。已修：書架/列表移到搜尋旁、桌機分類換行、手機搜尋獨立一行。待使用者確認：移除小標「A Reading List · 選書清單」、「14 篇讀書筆記」改為篩選標籤「讀書筆記 14」。
- R5 adapt + 上述修正同一 commit，送審。

### 2026-11-02 收尾
- R5 審查（31ebfcc）PASS，含 R4 複審 PASS；三項 should-fix 已於 f8ce3a3 修（清除搜尋保留焦點、手機 chip 列尾留白、焦點鎖限 stage-ui）。
- R6 polish 0942ec7：審查 FAIL 3 處小字（chip 數量 3.95、列表分區數量 2.67、「完」3.41）→ f8ce3a3 修正，另修單本書頁 meta 與清除搜尋連結（4.08→5.17）。實測 chip 數量 4.78、書頁 meta 4.78。
- 已知限制：重新整理或「完整書頁」→返回後，會多出一次無效的返回（R5 should-fix 2，未修）。
- 最終：astro check 0 錯誤、e2e 12/12、build 成功。新 commits 未推送。未驗證：Safari/iOS、實機螢幕閱讀器。

## 2026-11-03 接續與更正

更正上方與 `contract.md` 的過期內容（原文保留）：

- 使用者確認：`feat/immersive-bookshelf` 由使用者本人合併進 `main` 並推送（reflog：2026-11-02 15:00 fast-forward，至 `f8ce3a3`）。
- 使用者確認同意：移除小標「A Reading List · 選書清單」；「14 篇讀書筆記」改為篩選標籤「讀書筆記 14」。
- 契約記載的 worktree 與 branch 已不存在，程式以 `main` 為準。
- 使用者提出新目標：補上讀書心得與書本摘要；做法未定。首頁文案「每本書的背後，連結著我自己的讀書心得」暫不更動。
- 規格補同步在 book-reader 的 `ft/spec-sync-ux` branch，尚未合併。
