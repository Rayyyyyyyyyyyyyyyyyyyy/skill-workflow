---
target: 首頁書架與開書閱讀 UX
total_score: 25
max_score: 40
na_heuristics: 
p0_count: 0
p1_count: 2
target_identity: "file:/Users/ray.shao/book-reader-ft-immersive-bookshelf/site/src/pages/index.astro"
target_fingerprint: "sha256:8677d220cb23de00a25d494cf26834ffc9a106a621078d363a93a4081ae04f48"
target_path: /Users/ray.shao/book-reader-ft-immersive-bookshelf/site/src/pages/index.astro
timestamp: 2026-11-02T02-20-27Z
slug: site-src-pages-index-astro
---
# UX 評估：首頁書架 + 開書閱讀（dual-agent）

| # | 原則 | 分數 | 主要問題 |
|---|---|---|---|
| 1 | 系統狀態可見 | 3 | 底部計數器算跨頁、頁腳算頁數，對不上 |
| 2 | 貼近真實世界 | 3 | 有心得的書沒有「書籤」標示 |
| 3 | 控制與自由 | 3 | 開書不進瀏覽器歷史，返回會離站 |
| 4 | 一致性 | 2 | 列表檢視另一個 2D modal、不同 CTA |
| 5 | 防錯 | 2 | 手機誤觸暗區收書；單頁無法點擊往回 |
| 6 | 辨識而非回憶 | 2 | 14 本有心得的書在書架上看不出來 |
| 7 | 彈性與效率 | 3 | 無「直接跳到心得」 |
| 8 | 美感與簡約 | 3 | hero 佔滿首屏；只看有心得時木格空 |
| 9 | 錯誤復原 | 2 | 搜尋 0 結果只有英文 Nothing here yet. |
| 10 | 說明 | 2 | 沒提示書脊可點；觸控無 hover |
| 合計 | | 25/40 | 可接受 |

設計獨特性：authored（書脊主色、直書全形標點、高矮排序、排版封面＋藏書票、同一本書抽出）。hero 是通用編輯風。
偵測器：CLI 0；瀏覽器 16/22/11，主要 low-contrast（ONE HUNDRED 2.4:1、21 本 2.7:1、作者 2.8:1、頁碼 2.8:1、英文分類 3.4–4.1:1）；nested-cards/wide-tracking/cream/stripes 判為誤報。

## Priority issues
1. [P1] 有心得的書在書架上看不出來 → 書籤絲帶/燙金記號＋圖例（delight）
2. [P1] 書架在首屏之外 → 縮 hero、篩選集中（layout）
3. [P2] 列表檢視與書架兩種開書體驗 → 統一（distill）
4. [P2] 手機閱讀易中斷：無法點擊往回、誤觸收書、返回離站 → 左 1/3 往回、只用×/下滑收書、history（adapt）
5. [P2] 「完」頁死路、「意義・心靈 11 篇筆記」數字誤導、計數器與頁碼不一致（clarify）

## Persona red flags
- Jordan：不知道書脊可點；「14 篇讀書筆記」像統計不像按鈕；hero 文案承諾過多
- Casey：書架橫捲無提示；分類 chips 切掉；13 頁不能點回
- Sam：書脊焦點框淡色看不到；開書焦點未鎖（Tab 漏到 body）；計數器唸「2 / 7」無「頁」；方向鍵不看焦點

## Minor
只看有心得時木格空；無心得書第二跨頁左頁空白；列表實拍封面 vs 書架排版封面；搜尋空狀態英文；開啟跨頁左頁高 4px

## Questions
1. 為何預設展示 111 本而不是 14 本有心得的在前？
2. 3D 書是閱讀器還是書頁入口？
3. 什麼讓人下週回來？
