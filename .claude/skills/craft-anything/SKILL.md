---
name: craft-anything
description: Investigate how shipped software works (programs, apps, packages, firmware, web bundles) with evidence-backed answers through the Craft Anything MCP tools, keeping a durable brief, plan, hypotheses, findings and handoff in the project.
metadata:
  version: "2"
---

## Workbench 使用邊界（本 repo 適配，優先於下方上游內容）

這段是本集合加上的前言；下方「Craft Anything: evidence-first investigation」以後是上游 `storytold/craft-anything` commit `1f8508a104134c436cbba5ea2f675619ef47702f` 的 `crates/setup/src/skill.md`（skill version 2）原文。兩者衝突時以本段與 `AGENTS.md` 為準。

- **定位**：研究、設計或審查 task 需要「已發佈成品」（執行檔、App、套件、網站外觀等）的可查證事實時使用的證據工具。有原始碼且問題在原始碼，就直接讀原始碼。
- **目標授權**：只檢查使用者擁有或已獲准檢查的目標，把目標與授權依據寫入 task 輸入；不繞過 DRM、登入或反作弊。
- **預設淨室**：命令一律帶 `--clean-room`。深度模式（`--deep`、`settings_set deep_mode true`、`mcp --all-tools` 搭配 deep）、執行目標程式或改動裝置的工具（`--allow-run`、回傳 `consent_required`）都需使用者對該次目標明確授權。淨室是工具規則，不是 OS 沙盒。
- **瀏覽器**：`browser` toolset（`web_*`）與 `rebuild` 的網站擷取、三種寬度比對會開啟或連接瀏覽器。依 `AGENTS.md`，未經使用者該次明確授權不執行；未執行就列為缺口，不以靜態推論代替。
- **不當第二個控制者**：`rebuild` 與 `chat` 會另啟動 coding agent（`claude -p`），在 `Documents/Craft Anything` 或指定資料夾寫檔，不在 task worktree、不受 `allowed_paths` 限制。Workbench 作者不以它們取代自己的工作；使用者要求時，它的產物只算候選輸入，成果仍在 `packet.workspace` 交付並經獨立 Reviewer Proof。Craft Anything 的「檢查／相似度」是同一流程的自檢，不等於 Proof。
- **不改 agent 設定**：`setup`（含 `--yes`、`--client`）與 `uninstall` 會改 agent app 設定及家目錄 skills；未經使用者授權只執行 `doctor` 與 `setup --dry-run`。
- **證據放置**：`--project` 指向 task `allowed_paths` 內的 `*.cany` 資料夾，或以 `report --out`、`core_evidence_export` 輸出到 `allowed_paths` 內，提交時列入 `--files`，讓 Reviewer 能讀到 `ev_…` 對應的紀錄。不把 secrets、cookies 或個資寫進證據。
- **安裝**：本 repo 不附 `craft-anything-cli` 執行檔；需 Rust 1.97+ 從原始碼 `cargo install --path apps/craft-anything-cli`，或使用官方 Releases。下載、編譯或安裝外部程式碼需使用者授權；工具不可用時保存缺口，不猜測工具輸出。
- **固定版本**：本 Skill 未綁定任何 Role。實際使用的 task 在計畫 `supporting_sources` 列入 `.claude/skills/craft-anything/SKILL.md` 與 `.claude/skills/craft-anything/references/recovery.md`，派工包才會帶入固定內容；工具的實際版本（`craft-anything-cli --version`）記入證據。

# Craft Anything: evidence-first investigation

Use Craft Anything when an answer depends on something that was *built and shipped*: an executable, a
library, an app bundle, an APK, an Electron app, a WebAssembly module, firmware, a crash dump or a
network capture. If you have the source code and the question is about the source, read the source
instead; that is faster and more direct.

## Connect only when you need it

- If the `craft-anything` tools are already in your tool list, go straight to work. Don't run setup or
  doctor first.
- Trust the live tool list and its schemas over this file; the server may be newer or older.
- If the tools are missing or failing to start, run `craft-anything-cli doctor` and then
  `craft-anything-cli setup --dry-run` and show the user the plan before applying anything. After a
  successful setup the user must restart or reconnect their app.
- **Never run `setup --yes` (or `setup --client …`) on an entry that already lists every tool.**
  `setup` writes the plain `mcp` command, so it drops an `--all-tools` that is already in the entry
  and the server falls back to the small core toolset instead of the whole list. `doctor` calls such
  an entry "a different copy or shape of the command" and then suggests exactly that command, so
  the warning is not a reason to run it. Read the client's config file first: if the `args` of
  `craft-anything` end in `--all-tools`, leave the entry alone. `setup --dry-run` only prints the
  plan and changes nothing, so that one is safe to run. To add a client, write the entry by hand
  with `--all-tools`.
- Only a small core toolset is listed at first. Call `list_toolsets` to see the others and
  `enable_toolset` to switch one on (native code, Android, Apple, web, runtime…).
- In Clean room (Deep mode off, the default) nothing inside a target is read: only the tools that
  work from outside are listed, and others are refused with `details.reason` `clean_room`. Tell the
  user the question needs Deep mode (the switch in the app, `settings_set deep_mode true`, or the
  server started with `--deep`) instead of working around it.

## Working memory: keep it current

Long investigations outlive any single context window. The project keeps a brief, plan, hypotheses,
findings and a handoff note; use them every time.

1. **Start or resume.** Call `core_investigation_show` first. If there is a handoff, continue from it and
   the plan instead of starting over. Also call `core_session_show` to see what is open.
2. **New question?** Before any analysis call, write the brief with `core_brief_write` (the question, why
   it's being asked, the targets, constraints such as "don't run the program", and what a finished
   answer looks like) and an initial plan with `core_plan_update` (short numbered steps, each
   `todo`/`doing`/`done`/`blocked` with a reason).
3. **After each batch of tool calls:** update the plan's step status. When you form a claim worth
   testing, `core_hypothesis_record` with the prediction that would confirm or refute it. When evidence
   arrives, `core_hypothesis_update` (supported, refuted, abandoned) and attach the evidence ids.
4. **When something is settled:** `core_finding_record` with the statement and at least one evidence id.
   Findings are what reports are built from, never chat text.
5. **At the end of every turn:** `core_handoff_write`: where things stand, what to do next, and traps to
   avoid (dead ends, slow tools, misleading strings). Write it as if a stranger picks this up next.
6. `core_journal_read` shows every earlier tool call and model turn when you need to know what was
   already tried.

## Method

- **Observe, derive, infer, and say which.** Observed facts come straight from the bytes or a
  capture. Derived facts are computed from observations (a control-flow graph, a call graph).
  Inferences are judgment (names, intent, a model's reading). Label each claim accordingly.
- **Cite evidence ids** (`ev_…`) for every claim. A claim with no evidence id is a hypothesis.
- **Absence is not proof.** "No string found" or "no caller found" only covers what was searched.
  State the search boundary and the coverage the tool reported, and record an unknown
  (`core_unknown_add`) for anything that matters but is still open.
- **Predict, then verify.** Before running a tool to test a hypothesis, write down what you expect to
  see. If the result disagrees, update the hypothesis instead of explaining the result away.
- **Summary first, then page.** Large results come back as a summary plus an evidence id. Ask for
  pages (`offset`/`limit`) or the specific item you need instead of everything at once. Never repeat
  an identical call that already succeeded or was rejected.
- **Format-aware, not filename-aware.** Let the parsers tell you what a file is.

## Where to start, by target

| Target | First step |
|---|---|
| Native executable or library (ELF, PE, Mach-O) | `core_target_open`, then the overview, search and function tools |
| Electron app, `.asar`, or a JavaScript bundle | `core_target_open` on the app or archive, then the JavaScript toolset |
| Android APK / DEX | `core_target_open`, then the Android toolset |
| .NET assembly | `core_target_open`, then the managed toolset |
| WebAssembly, Go, PE resources, firmware, crash dumps | the formats toolset |
| A live web page or Electron window | the browser toolset (observation only) |
| Two versions of the same app | open both, then the application toolset's comparison tools |

If the user says "my app" without naming it, ask which one. Never guess with an example file.

## Consent and safety

- Tools that run the target's code or change a connected device need the user's explicit OK. If a
  call returns `consent_required`, explain what it would do and ask; never look for a way around it.
- Static analysis never runs the target. Don't claim runtime behaviour from static evidence alone;
  say it is inferred.
- Never put secrets, cookies or personal data into notes, findings or handoffs.

## When something fails

| Error code | What to do |
|---|---|
| `not_found` | Open a target first (`core_target_open`), or check the path or name |
| `feature_missing` / `engine_missing` | Read the remediation; it names the toolset, engine or setting needed |
| `over_limit` | The result was too big to send; page it or read it by evidence id (`evidence://<id>` resource) |
| `stale_revision` | Re-read with `core_investigation_show`, merge, retry |
| `consent_required` | Ask the user |

Before you finish: mark each plan step done or blocked, make sure every conclusion in your answer
matches a recorded finding, list what is still unknown, and write the handoff.
