# craft-anything-integration

## 目前狀態（2026-11-07 查核）

- 狀態：方法包已附入 repo（opt-in Skill）；等使用者決定是否綁定 Role、是否在雲端環境安裝 CLI。
- `workbench` 顯示 `PLANNING`：這次直接修改集合本身的方法包與文件，沒有走 `plan`／`approve-plan` 正式流程（理由見下方「選路」）。
- 上游版本：`storytold/craft-anything` commit `1f8508a104134c436cbba5ea2f675619ef47702f`（2026-11-07 clone）。
- 未驗證：`craft-anything-cli` 沒有編譯或執行過（這次 session 編譯外部程式碼的請求被權限拒絕）；Skill 在真實 Workbench 派工中的載入與使用；任何瀏覽器、深度模式或 `rebuild` 行為。

## 原始想法

幫我看 craft anything 這個 GitHub repo 的內容，能不能幫我融入 workflow

進度與接續：在集合根目錄執行 `python3 workbench.py status craft-anything-integration`。
正式狀態與版本保存在 `.workflow/`；成果預設放 `workspace/`。

## Craft Anything 是什麼（依上游 README、docs 與原始碼）

- 純 Rust 的「淨室」逆向／研究引擎，早期 alpha，MIT 或 Apache-2.0 雙授權。桌面 App（egui）、`craft-anything-cli` 與 MCP 伺服器共用同一引擎。
- 約 320 個工具（引擎 302 個、17 個 toolset：native、Apple、formats、.NET、Android、Java、adb、browser、JavaScript、runtime、Frida、application 比對、projects、build 等），每個都是 CLI 子命令也是 MCP 工具；檢查本身不需要 AI。
- 主流程 `rebuild`：研究 → 建置 → 檢查 → 就緒。建置階段在背景執行使用者自己的 `claude -p`，並以自家 MCP 的 `core_action_approve` 當權限工具；網站會在三種寬度擷取並比對相似度。
- 淨室（預設）只看外部可見的東西；深度模式才讀程式碼、檔案與網頁原始碼。上游明說淨室是工具規則，不是 OS 沙盒。
- 證據紀錄附信心度、涵蓋範圍與限制；`*.cany` 專案資料夾保存 brief、plan、hypotheses、findings、handoff 與 journal。
- 上游自帶官方 Skill（`crates/setup/src/skill.md` + `skill_recovery.md`），`craft-anything-cli setup` 會把它寫進家目錄 `~/.claude/skills/` 等位置。

## 和 Workflow 的對應

| Craft Anything | 本 Workflow | 處理 |
|---|---|---|
| 證據紀錄（observed／derived／inferred、`ev_…`、unknowns） | P00 實證政策：事實／推論／假設／未知 | 直接相容：作為 research／design task 的證據工具 |
| brief → plan → findings → handoff | Project 原始想法、計畫、Proof、HANDOFF | 只當 task 內的工作記錄；正式狀態仍在 `workbench.py` |
| `rebuild` 自己的研究→建置→檢查迴圈 | planner → 作者 → 獨立 Reviewer → accept → apply | 不併入：它是第二個控制者，寫在 task worktree 以外，檢查是自檢 |
| 網站擷取、三寬度比對（瀏覽器） | 瀏覽器需逐次明確授權 | 預設不執行，缺口保留 |
| 深度模式、`--allow-run` | 敏感與破壞性操作先確認 | 需使用者對該次目標授權 |
| `setup`／`uninstall` 改 agent 設定 | 不擅自改環境 | 只允許 `doctor`、`setup --dry-run` |

## 這次做了什麼

- 新增 `.claude/skills/craft-anything/`：`SKILL.md`（上游原文前加一段 Workbench 使用邊界）、`references/recovery.md`（原文）、`LICENSE`（上游 MIT 原文）。
- `.claude/methods-manifest.json` 新增 `skill:craft-anything` 來源、上游雜湊、適配說明與三個檔案雜湊。
- `docs/CLAUDE_SKILLS_INSTALL.md` 補一行指向本紀錄。
- 沒有改 `workbench.py`、`library/roles.json`、Playbooks，也沒有安裝 CLI 或 MCP 設定。

## 選路

需求已足夠：使用者要「看內容」及「融入 workflow」。研究由主對話直接讀上游 repo 完成；融入採最小、可撤回的做法——附入上游官方 Skill 並寫明本 workflow 的邊界，不綁定 Role。是否讓每個 researcher 派工都帶這份 Skill、是否在雲端環境裝 CLI，屬方向性決策，留給使用者。

## 在計畫中使用

需要檢查已發佈成品的 task，在 `supporting_sources` 列入：

```json
"supporting_sources": [
  {"path": ".claude/skills/craft-anything/SKILL.md", "format": "text"},
  {"path": ".claude/skills/craft-anything/references/recovery.md", "format": "text"}
]
```

並在 task 輸入寫明：目標與授權依據、淨室或深度模式（深度需授權）、是否授權瀏覽器、證據輸出路徑（須在 `allowed_paths` 內，例如 `proof/craft/`）。驗收可要求每項結論引用匯出的 `ev_…` 證據，未執行的工具列為 UNKNOWN 或缺口。

## 待使用者決定

1. 是否把 `craft-anything` 綁到 `researcher`（之後每次 researcher 派工都會帶入），或維持逐 task 以 `supporting_sources` 帶入（目前做法）。
2. 是否在雲端環境安裝 `craft-anything-cli`（需 Rust 1.97+ 從原始碼編譯，或下載 Releases；都要執行外部程式碼），以及要不要在 repo 加 MCP 設定。
3. 是否允許某些 task 使用深度模式、瀏覽器擷取或 `rebuild`；預設全部不允許。

## 驗證

- `python3 scripts/check_portability.py`：PASS（含新檔雜湊）。
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q`：51 tests OK。
- 本次 Claude Code 雲端 session 在新增檔案後自動列出 `craft-anything` Skill（只證明被發現，不證明實際使用效果）。
- 上游原文保留：以 diff 確認 `SKILL.md` 去掉前言後與上游 `skill.md` 一致；`recovery.md`、`LICENSE` 雜湊與上游相同。
