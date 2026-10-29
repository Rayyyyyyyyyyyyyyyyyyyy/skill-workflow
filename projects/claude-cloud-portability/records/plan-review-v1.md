# Claude cloud portability — independent plan admission v1

Verdict: **FAIL** (one concrete input-version blocker; no implementation reviewed).

Reviewer: `/root/claude_portability_review`, a separate agent/context from planner `/root`. This agent only performed read-only reconnaissance and this admission review; it has not authored the plan or product. Source role: full installed Code Reviewer instructions, plus P00 and current deliver/review Playbooks.

## Bound inputs and original coverage

- Formal plan hash: `c4e88009c9221c161271451519a26b6ef53b520eb304eb60cbde5b88d3e47d10` (read from original controller `status`, not computed from candidate JSON).
- Original request: `projects/claude-cloud-portability/PROJECT.md`; user clarification supplied with review assignment: use Claude cloud sessions that clone GitHub, and package only this repo's used Skills.
- R1 covers Claude entry, session handoff, AGENTS protections, Playbook/Role/Skills/Proof.
- R2 covers actual used Roles/Skills, both grill wrappers, support files/licenses and local-path/tool-entry portability.
- R3 covers dynamic paths and the distinction between published files and missing local SQLite/blobs/private Git/worktrees.
- R4 covers an empty-personal-HOME relocation experiment, real plan/dispatch source loading, existing tests and truthful cloud/browser NOT_RUN limits.
- Controller-expanded acceptance contains all four unchanged mandatory `deliver` criteria (`PB-package-requirements`, `integrity`, `verification`, `handoff`). One author task has an explicit writable scope and no dependency cycle. A single task needs no integrate node.
- Local preparation and static/runtime relocation checks are authorized and do not require a live Claude cloud run or a browser. No deployment, credential transfer, global installation or external publication is added to the plan.

## Blocking finding: migration input contents are not pinned

**FACT:** The formal task's `supporting_sources` contains only writing-for-agents and skill-creator. Formal role bindings snapshot only implementer and reviewer. The private baseline contains `library/roles.json` path descriptors but no `.claude/` or migration-source manifest/content. Confirmed through public `status` plus read-only listing of the private baseline tree.

**FACT:** R2 requires copying the actual seven Roles, seven bound Skills, grill-me/grill-with-docs wrappers and necessary support/license files from external personal directories. The full source contents needed for that work are not in the approved baseline or the task's sealed sources. The current `library/roles.json` only names mutable paths for the other profiles.

**INFERENCE:** An author would have to read unpinned external inputs after admission to produce the portable package. That conflicts with `docs/WORKFLOW.md` section 3's requirement to fix reused inputs and the task's actual reference/script sources before work starts. This matters here because preserving *actual* installed methods and their provenance is a central deliverable, rather than an incidental implementation choice.

**Required recovery:** Before execution, make the migration-source content and provenance fixed, accessible input (for example, explicitly snapshot all actually copied text/support/license sources through the controller, or include a safely staged source bundle with content digests in a newly captured baseline). Include any essential official Claude documentation extract used for format/version decisions. Keep the existing R1–R4 and Playbook minimum criteria; do not weaken acceptance to allow unpinned sources. Then resubmit the not-yet-started plan for independent admission.

## Checks deferred to delivery

The plan correctly promises to test fresh-clone-like operation without the old HOME. Delivery still has to prove native Claude entry/skill/agent formats, wrapper tool adaptation, support-file closure, license preservation, browser restriction precedence, safe empty-DB handling and truthful actual-cloud limitations. A source manifest alone will not prove those behaviors.

No product files, plan, formal controller state or Git index were modified by this review. Browser and actual Claude cloud testing: **NOT_RUN**.
