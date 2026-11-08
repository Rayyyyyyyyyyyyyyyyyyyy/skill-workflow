# 工具目錄

由 `scripts/sync_methods.py` 產生；新增或修改 Skill／Role 後重跑，不要手改。
每接一個任務先掃過這份目錄，挑出這次用得上的 Skill 與角色，記到 PROJECT.md 的「工具」欄；做到一半需要別的就再加。

## Skills（`.claude/skills/`，Claude Code 會自動發現；用 Skill 工具或 `/名稱` 呼叫）

| Skill | 用途 |
|---|---|
| `ask-matt` | Pick the workflow mode, Skills and Roles for an idea, direction or goal. |
| `code-review` | Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's doc… |
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportuniti… |
| `design-taste-frontend` | tasteskill v2, the anti-slop frontend skill. Art direction for websites, distilled from a study of 247 curated gallery sites (One Page Love… |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throw… |
| `domain-modeling` | Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or edi… |
| `grill-me` | A relentless interview to sharpen a plan or design. |
| `grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. |
| `grilling` | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' tri… |
| `handoff` | Compact the current conversation into a handoff document for another agent to pick up. |
| `humanizer` | Rewrite, edit, and polish AI-generated or stiff text so it sounds natural, specific, and human while preserving meaning. Use for copywritin… |
| `impeccable` | Use to design, redesign, critique, audit, polish or animate a frontend: websites, landing pages, dashboards, app UI, components, native iOS… |
| `implement` | Implement a piece of work based on a spec or set of tickets. |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. |
| `ponytail` | Lazy senior dev mode: the smallest change that fully solves the task, and a reply a busy human understands in one read. Use on any coding t… |
| `prototype` | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right… |
| `research` | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants… |
| `setup-matt-pocock-skills` | Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before f… |
| `tdd` | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integrat… |
| `teach` | Teach the user a new skill or concept, within this workspace. |
| `to-spec` | Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already… |
| `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the co… |
| `triage` | Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs. |
| `ui-ux-pro-max` | UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, reviewing, or fixing interfaces… |
| `wayfinder` | Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve the… |
| `writing-for-agents` | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. |

## 平台可能提供的 Skills（依當次 session 實際清單為準）

| Skill | 用途 |
|---|---|
| `deep-research` | 多來源研究並寫成完整報告 |
| `docs / docx / pdf / pptx / xlsx` | 產生或讀寫文件、簡報、試算表、PDF |
| `skill-creator` | 建立或改進 Skill 並跑評測 |
| `dataviz` | 做任何圖表或資料視覺化前先讀 |
| `built-in-browser / chrome-browser / computer-use` | 操作瀏覽器或桌面（需授權，見 AGENTS.md） |
| `code-review / security-review / simplify` | Claude Code 內建的審查與精簡 |

## 原生角色（`.claude/agents/`，可直接當 subagent_type 使用）

| 角色 | 用途 |
|---|---|
| `designer` | 依產品情境產生可由工程接手的流程、操作狀態、資訊結構與一致視覺方向。 |
| `implementer` | 在指定工作範圍完成工程交付，保留既有資料與介面，使用對應行為與風險的最小有效驗證。 |
| `integrator` | 在獨立 Git task worktree 整合已接受的固定提交，保留來源與衝突，對整合版本重新驗證，安全回寫時保護來源既有修改。 |
| `planner` | 將原始想法整理成有來源、範圍、交付終點與驗收依據的工作契約；把關鍵決策交回使用者。 |
| `researcher` | 依原始問題追查一手證據，區分事實、推論、假設與未知，交付可追溯研究。 |
| `reviewer` | 在獨立上下文逐項查核指定成果與證據；回報符合、缺陷與未知，不修改作者成果或自行批准交付。 |
| `writer` | 依受眾與使用情境完成文件交付，保留原始意圖、可查核事實、來源與限制。 |

## 專業角色庫（`library/agents/`，共 282 個）

完整清單與一行說明在 [agents/INDEX.md](agents/INDEX.md)，用關鍵字搜尋最快：`grep -i "frontend\|react" library/agents/INDEX.md`。

要用某個角色時，開一個 subagent，請它先完整讀該角色檔，再以那個角色完成指定任務；同一任務可以組好幾個角色分工或互相審查。

| 分部 | 數量 | 例子 |
|---|---:|---|
| academic | 6 | Anthropologist, Geographer, Historian, Narratologist, Psychologist, Statistician |
| design | 10 | Brand Guardian, Image Prompt Engineer, Inclusive Visuals Specialist, Persona Walkthrough Specialist, UI Designer, UI Finish-Gate Reviewer … |
| engineering | 65 | AI Data Remediation Engineer, AI Engineer, API Platform Engineer, ATS Validator Architect, Autonomous Optimization Architect, Backend Architect … |
| finance | 5 | Bookkeeper & Controller, Financial Analyst, FP&A Analyst, Investment Researcher, Tax Strategist |
| game-development | 21 | Blender Add-on Engineer, Economy Designer, Game Audio Engineer, Game Designer, Godot Gameplay Scripter, Godot Multiplayer Engineer … |
| gis | 13 | 3D & Scene Developer, GIS Analyst, BIM/GIS Specialist, Cartography Designer, Drone/Reality Mapping Specialist, GeoAI/ML Engineer … |
| healthcare | 3 | Clinical Evidence Agent, Healthcare Innovation Strategist, Sovereign Health Systems Agent |
| marketing | 37 | AEO Foundations Architect, Agentic Search Optimizer, AI Citation Strategist, App Store Optimizer, Baidu SEO Specialist, Bilibili Content Strategist … |
| paid-media | 7 | Paid Media Auditor, Ad Creative Strategist, Paid Social Strategist, PPC Campaign Strategist, Programmatic & Display Buyer, Search Query Analyst … |
| product | 6 | Behavioral Nudge Engine, DX Engineer, Feedback Synthesizer, Product Manager, Sprint Prioritizer, Trend Researcher |
| project-management | 7 | Experiment Tracker, Jira Workflow Steward, Meeting Notes Specialist, Project Shepherd, Studio Operations, Studio Producer … |
| research | 1 | Research Synthesist |
| sales | 9 | Account Strategist, Sales Coach, Deal Strategist, Discovery Coach, Sales Engineer, Offer & Lead Gen Strategist … |
| security | 12 | AI-Generated Code Security Auditor, Application Security Engineer, Security Architect, Blockchain Security Auditor, Cloud Security Architect, Compliance Auditor … |
| spatial-computing | 6 | macOS Spatial/Metal Engineer, Terminal Integration Specialist, visionOS Spatial Engineer, XR Cockpit Interaction Specialist, XR Immersive Developer, XR Interface Architect |
| specialized | 59 | Accounts Payable Agent, Agentic Identity & Trust Architect, Agents Orchestrator, Automation Governance Architect, Business Strategist, Change Management Consultant … |
| support | 6 | Analytics Reporter, Executive Summary Generator, Finance Tracker, Infrastructure Maintainer, Legal Compliance Checker, Support Responder |
| testing | 9 | Accessibility Auditor, API Tester, Evidence Collector, Performance Benchmarker, Reality Checker, Test Automation Engineer … |
