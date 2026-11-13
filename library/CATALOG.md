# 工具目錄

由 `scripts/sync_methods.py` 產生；新增或修改 Skill／Role 後重跑，不要手改。
每接一個任務先掃過這份目錄，挑出這次用得上的 Skill 與角色，記到 PROJECT.md 的「工具」欄；做到一半需要別的就再加。

## Skills（`.claude/skills/`）

「呼叫」欄寫「Skill 工具」的，直接用 Skill 工具呼叫；寫「讀檔」的，這個 Skill 關掉了模型自動呼叫，要直接完整讀 `.claude/skills/<名稱>/SKILL.md` 再照做（使用者也可以自己打 `/名稱`）。
Matt 工程系列（to-spec、to-tickets、triage、wayfinder、implement）的 issue tracker 設定已經寫在 `docs/agents/`：票放在 `projects/<slug>/` 的本機 Markdown，不必另跑 setup-matt-pocock-skills。

| Skill | 呼叫 | 用途 |
|---|---|---|
| `ask-matt` | 讀檔 | Pick the workflow mode, Skills and Roles for an idea, direction or goal. |
| `code-review` | Skill 工具 | Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's doc… |
| `codebase-design` | Skill 工具 | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportuniti… |
| `design-taste-frontend` | Skill 工具 | tasteskill v2, the anti-slop frontend skill. Art direction for websites, distilled from a study of 247 curated gallery sites (One Page Love… |
| `diagnosing-bugs` | Skill 工具 | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throw… |
| `domain-modeling` | Skill 工具 | Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or edi… |
| `grill-me` | 讀檔 | A relentless interview to sharpen a plan or design. |
| `grill-with-docs` | 讀檔 | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. |
| `grilling` | Skill 工具 | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' tri… |
| `handoff` | 讀檔 | Compact the current conversation into a handoff document for another agent to pick up. |
| `humanizer` | Skill 工具 | Rewrite, edit, and polish AI-generated or stiff text so it sounds natural, specific, and human while preserving meaning. Use for copywritin… |
| `impeccable` | Skill 工具 | Use to design, redesign, critique, audit, polish or animate a frontend: websites, landing pages, dashboards, app UI, components, native iOS… |
| `implement` | 讀檔 | Implement a piece of work based on a spec or set of tickets. |
| `implement-spec` | 讀檔 | Implement the result of /to-spec and /to-tickets in code. |
| `improve-codebase-architecture` | 讀檔 | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. |
| `ponytail` | Skill 工具 | Lazy senior dev mode: the smallest change that fully solves the task, and a reply a busy human understands in one read. Use on any coding t… |
| `pr` | Skill 工具 | Use when writing a PR body. |
| `prototype` | Skill 工具 | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right… |
| `research` | Skill 工具 | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants… |
| `retro` | 讀檔 | Conduct a retrospective on a coding session. |
| `setup-matt-pocock-skills` | 讀檔 | Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before f… |
| `tdd` | Skill 工具 | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integrat… |
| `teach` | 讀檔 | Teach the user a new skill or concept, within this workspace. |
| `to-spec` | 讀檔 | Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already… |
| `to-tickets` | 讀檔 | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the co… |
| `triage` | 讀檔 | Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs. |
| `ui-ux-pro-max` | Skill 工具 | UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, reviewing, or fixing interfaces… |
| `wayfinder` | 讀檔 | Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve the… |
| `writing-for-agents` | Skill 工具 | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. |

## 平台可能提供的 Skills（依當次 session 實際清單為準）

| Skill | 用途 |
|---|---|
| `deep-research` | 多來源研究並寫成完整報告 |
| `docs / docx / pdf / pptx / xlsx` | 產生或讀寫文件、簡報、試算表、PDF |
| `skill-creator` | 建立或改進 Skill 並跑評測 |
| `dataviz` | 做任何圖表或資料視覺化前先讀 |
| `built-in-browser / chrome-browser / computer-use` | 操作瀏覽器或桌面（需授權，見 CLAUDE.md） |
| `security-review / simplify` | Claude Code 內建的安全審查與精簡（`code-review` 指的是 repo 內 Matt 的版本） |

## 原生角色（`.claude/agents/`，可直接當 subagent_type 使用）

| 角色 | 用途 |
|---|---|
| `designer` | 依產品情境產生可由工程接手的流程、操作狀態、資訊結構與一致視覺方向。 |
| `implementer` | 在指定工作範圍完成工程交付，保留既有資料與介面，使用對應行為與風險的最小有效驗證。 |
| `planner` | 將原始想法整理成有來源、範圍、交付終點與驗收依據的工作契約；把關鍵決策交回使用者。 |
| `researcher` | 依原始問題追查一手證據，區分事實、推論、假設與未知，交付可追溯研究。 |
| `reviewer` | 在獨立上下文逐項查核指定成果與證據；回報符合、缺陷與未知，不修改作者成果或自行批准交付。 |
| `writer` | 依受眾與使用情境完成文件交付，保留原始意圖、可查核事實、來源與限制。 |

## 專業角色（全域 `~/.claude/agents/`，不在 repo 裡）

agency-agents 的專業角色裝在全域，session 的 subagent 類型清單上就有名稱和一行說明，直接用名稱開；派工時寫明要它用哪些方法與工具（不是只換口吻）。安裝方式與常用角色見根目錄 README「另外安裝」。
