# 本機 Skills 與 awesome-design-md 總覽

這次交付包含本機可讀 Skill 定義的完整盤點，以及 `awesome-design-md` 固定版本調查。**盤點的檔案／名稱數量不代表已啟用或已驗證的能力數量**；研究沒有安裝、移除、修改任何原始 Skill，也沒有使用瀏覽器。

## 本機盤點（FACT）

盤點時點：2026-10-29（Asia/Taipei）。全範圍共 **1,540 個定義路徑、1,537 個 canonical 路徑、851 個宣告名稱、997 種內容雜湊**；其中含 **628 份暫存、462 份備份**。[完整盤點報告](inventory/report.md)、[逐筆 JSON](inventory/skills.json)、[可篩選 CSV](inventory/skills.csv)

| 個人／共用來源 | 路徑數 | 組成 |
|---|---:|---|
| `~/.codex/skills` | 40 | 個人 35、system 5 |
| `~/.claude/skills` | 39 | 一般 23、同步 13、符號連結 3 |
| `~/.agents/skills` | 4 | 共用實際來源 |
| 三個根目錄聯集 | 83 | canonical 80；去重後 **57 個名稱、59 種內容** |

Claude 的三個符號連結指向共用 `.agents` 來源。全部 **57 個名稱、原始用途與實際路徑**見[常用來源清單](inventory/report.md#個人目錄中全部-57-個名稱)；同名不同內容的兩項是 `impeccable`、`skill-creator`，差異紀錄見 [duplicates.json](inventory/duplicates.json)，不據此自動刪除或合併。

個人／共用目錄之外，plugin 快取與 runtime bundle 有 **92 個路徑、63 個名稱**；它們和個人來源存在同名交集，不能直接相加成能力總數。當前 workflow repo 方法包另有 10 個名稱；marketplace、vendor、其他專案、task worktrees、備份與暫存均在完整清單分開分類。[分類與範圍](inventory/report.md#根目錄與統計口徑)

此次掃描涵蓋可讀使用者目錄及明列的 symlink roots；排除了 Library、Trash、node_modules、Git／控制資料等目錄，Photos Library／Trash 有拒絕存取紀錄。未窮舉系統目錄與任意 symlink，也未查核各定義是否被實際載入、啟用或成功執行；因此這是一份可追溯的檔案盤點。[掃描定義與排除範圍](inventory/skills.json)、[掃描錯誤](inventory/scan-home-errors.txt)

## awesome-design-md（FACT）

調查固定在 commit `fcc70284932276d085f01ef9f83edde90b1258cb`。完整未截斷 tree 有 **84 份 DESIGN.md、0 份 SKILL.md、0 個 preview HTML**；實讀 README、LICENSE 及三份設計範例，詳細來源／雜湊見 [sources.json](awesome-design-md/sources.json)。它提供第三方從公開網站分析的視覺參考文件，沒有 Skill 入口或安裝流程，不能當成各品牌官方完整產品規範。[調查報告](awesome-design-md/findings.md)、[固定 README](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/README.md)

| 實讀範例 | 文件描述的方向 | 固定來源 |
|---|---|---|
| Claude | 暖奶油底、珊瑚色動作、襯線展示字體 | [DESIGN.md](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/design-md/claude/DESIGN.md) |
| Linear | 近黑畫布、灰階層次、少量薰衣草藍 | [DESIGN.md](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/design-md/linear.app/DESIGN.md) |
| Stripe | 靛色動作、深海軍藍文字、漸層網格 | [DESIGN.md](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/design-md/stripe/DESIGN.md) |

README 提到每站附有 `preview.html`／`preview-dark.html`，但固定 tree 沒有這些檔案；不能把文件說明當作可用預覽已存在。repo 文件採 MIT 授權並按現況提供；授權及範例缺口的原始來源見[完整調查](awesome-design-md/findings.md)。

## 如何和現有方法搭配（INFERENCE／候選建議）

Skills 提供如何規劃、製作與查核的方法，所選 `DESIGN.md` 可提供該專案的視覺語言；本機 `claude-design`、`ui-ux-pro-max`、`design-taste-frontend`、`impeccable`、`popular-web-designs` 的實際分工比較見[方法對照](awesome-design-md/findings.md#fact和本機設計-skills-的分工)。

若之後採用，先為**該 Project**挑選／調整一份設計輸入，保留來源版本與通知，再固定到 design task；不要在集合根目錄放一份設計規範，默認影響所有 Projects。這是建議，沒有替使用者選定品牌、採用文件、安裝 Skill 或改動 Flow。

`design-taste-frontend` 的部分 house rules 與這些參考的漸層、靛紫色、奶油／陶土色可能衝突；應先確認該專案的視覺主準則與適用例外，再執行設計，避免兩套互斥規則同時生效。[具體對照與推論依據](awesome-design-md/findings.md#inference適合目前-flow-的接法)

## 驗證、交接與限制

本次整合核對已接受來源的固定 commits、接受紀錄及 12 份輸入檔 SHA-256，重新計算全域／個人／plugin 統計並檢查相對連結；詳細結果在 [integration-checks.json](integration-checks.json)。上游檔案保持原 bytes，沒有重掃或重跑任何 Skill。

整合前控制器產生的合併版本、來源順序、base／tree 與接受 digest 記於 integration-checks.json；新增總覽後的正式 submission commit／tree 由控制器封存，本文不以尚未產生的自身 commit 作自我驗收。交付仍須獨立 Reviewer 查核，接受後才由控制器逐檔核對 baseline 並安全回寫；來源有新修改就保留現場等待，不覆寫。

未執行 Skill 功能、UI 生成、品牌實站對照、瀏覽器預覽、安裝／移除、部署或發布。未核對其餘 81 份設計正文，也未確認本機所有快取的啟用狀態；後續版本或實際採用仍需按當次條件驗證。
