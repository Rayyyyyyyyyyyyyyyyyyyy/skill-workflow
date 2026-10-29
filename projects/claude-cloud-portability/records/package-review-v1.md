# Claude cloud portability — independent delivery review v1

Overall: **FAIL**, one packaging blocker. Source portability and local control behavior passed their scoped checks; the copied Ponytail method is missing its upstream MIT copyright/permission notice.

Reviewer `/root/claude_portability_review` is a separate agent/context from author `/root` and has not authored the product. Review workspace is the controller-provided detached worktree. No author files, acceptance criteria, controller state or main Git index were changed.

## Bound object and raw inputs

- Submitted candidate commit: `ea11ffbbf9979fac1679f5b43496202e395a742e`; reviewer `git rev-parse HEAD` matched it.
- Review ID: `01f4ffde8aa9495484397dba156bd5cb`, round 1.
- Submission digest: `a55224e8eeb8b942d00744012c40010b4a8c110e88fb32625edb1a48af810fa7`.
- Contract digest: `c38bdeb23c6742912c0d3aed42851d7b8e0f5c35a25c510fa018e1f2c20dfffe`.
- Baseline digest: `a4b6b875c4147a536d63b5358d4bdadd11e9f6d332cab58f792ad1060a2d69c4`.
- Original idea and R1–R4 read from the actual review packet. Prior admission approval does not stand in for this delivery review.
- Read actual candidate diff against `1f57666f3fc1f682639e191381aef41fb8a966c2`, entry and workflow/cloud documents, Role binding, all wrapper instructions, portability checker/test implementation and manifest. Compared packaged method bodies to the packet's sealed supporting instructions, rather than only author's summary.

## One blocking defect

**F1 — Ponytail's upstream license notice is absent from the redistributed method package.**

FACT: `.claude/skills/ponytail/SKILL.md` copies the full upstream skill and contains only `license: MIT` at line 10. No Ponytail license file is present anywhere in the 104 shipped method files. `.claude/methods-manifest.json:171–179` records only Ponytail's SKILL.md and claims runtime support/data/licenses retained; `library/README.md:40` similarly says licenses accompany their source.

FACT: The installed upstream plugin has a package-level LICENSE outside the skill subfolder: `/Users/ray.shao/.codex/plugins/cache/ponytail/ponytail/5.3.2/LICENSE`. I read the actual file in this review, prompted by the controller's concrete source pointer, and computed SHA-256 `fb1bc6909ac3ef82d5c22106e32ef682b0cff66788fa915fb9b53b15c9d2f3ab`. Its copyright/permission notice requires inclusion with copies or substantial portions. Neither that notice nor its author copyright appears in the candidate. The bare frontmatter label does not preserve those source terms.

INFERENCE: This directly fails R2's explicit license-preservation requirement and the deliver integrity/requirements minima. It is a concrete missing redistribution artifact, independent of whether runtime tests pass.

Required fix: preserve the exact upstream LICENSE with the packaged Ponytail skill, record its original source/digest and shipped-file hash in the method manifest, and recheck the package. Do not modify method behavior, widen the original requirements or replace the license with a summary. Exact source text is captured below as immutable review evidence for the bounded rework.

## Actual independent verification

I reconstructed the test input independently using `git archive` of main commit `6dfe977d0dc53a90fb7a7ef7d93bdb1ffed1857c`, then overlaid `git archive` of the fixed candidate commit. Both archives were extracted into a fresh directory with spaces, using safe data extraction. This supplies unchanged runtime/tests absent from the task's intentionally narrow baseline; it does not read the author's mutable workspace.

Temporary reconstruction: `/var/folders/fh/6chnhm7x76l6dbxgghp4qw2w0000gp/T/claude-independent-review-7czouj0g/fresh full repository`. Every subprocess received an empty HOME and `PYTHONDONTWRITEBYTECODE=1`.

| Independent command/check | Actual result |
|---|---|
| `python3 scripts/check_portability.py` | Exit 0; manifest/path checks PASS; Python 3.11+, Git and Node available; tool explicitly lists discovery/cloud/network/browser as unchecked. |
| `python3 -m unittest discover -s tests -q` | Exit 0; **51 tests in 23.794s, OK** (48 original plus 3 portability tests). |
| `python3 .claude/skills/ui-ux-pro-max/scripts/search.py 'keyboard focus' --domain ux -n 1` | Exit 0; returned Focus States from ux-guidelines.csv. |
| `node .claude/skills/design-taste-frontend/scripts/draw.mjs --list sectors` | Exit 0; listed 22 sectors from packaged data, no browser. |
| Method provenance/closure | All 104 method files exactly covered by manifest. Seven Role bodies match the sealed original developer_instructions with only declared metadata/preface added. Unadapted Skill support/data/assets match pinned content. UI skill changes are precisely the declared Python/repository-path replacements. |
| Native metadata/wrappers | Seven unique Role names and descriptions; ten Skill entrypoints have expected name/description frontmatter. grill wrappers read actual sibling sources instead of calling a missing harness-specific Skill tool. ask-matt routes only to shipped methods. |
| Original safety and continuity | CLAUDE imports AGENTS; shared browser/data/operation/verification protections remain. Docs preserve separate author/reviewer contexts, actual host identity/stop evidence, controller packets, task workspace restrictions and fixed-source Proof. |
| Published vs local state | Docs require the branch containing these files, distinguish ignored DB/private Git/tasks from tracked handoff files, do not equate empty `list` with overwrite permission, and do not claim `adopt-git` is cross-machine import. Historical workbench records remain historical. |

The new tests exercise real Role/Skill loading through plan/dispatch in a relocated repository, under fixture actors clearly documented as control tests. Failure tests exercise a missing support file, modified Skill digest, absolute source and source symlink. These are useful behavior checks; they are not real Claude native activation or independent semantic acceptance by fixture agents.

Primary platform documents were read during review: [memory/imports](https://code.claude.com/docs/en/memory), [Skills](https://code.claude.com/docs/en/skills), [subagents](https://code.claude.com/docs/en/sub-agents) and [cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web). They support the repository layout, import approach and distinction between ordinary repository cloud sessions and Project cloud threads. Those references do not establish that a live session has loaded this particular package.

## Every required criterion

| acceptance_id | Result | Concrete basis |
|---|---|---|
| R1-check | PASS | Actual CLAUDE/AGENTS/workflow entry preserves the six-step contract, discussion methods, independent Proof and shared safety protections; native layout matches primary docs. Actual platform loading remains explicitly untested. |
| R2-check | **FAIL** | Sources, roles, wrappers and runtime support are packaged and portable, but F1 omits Ponytail's required upstream license notice. |
| R3-check | PASS | Current operational roots are dynamic; fresh-clone guidance distinguishes tracked records from unavailable official state and provides safe handoff/identity/worktree boundaries. |
| R4-check | PASS | Independent fixed-input/empty-HOME reconstruction passed checker, all 51 tests and representative Python/Node support commands. No cloud/browser success is claimed. |
| PB-package-requirements | **FAIL** | F1 leaves the explicit R2 endpoint incomplete despite other original requirements being covered. |
| PB-package-integrity | **FAIL** | F1 drops applicable source redistribution notice, while candidate docs claim licenses retained. Existing source/runtime preservation and browser safeguards otherwise pass. |
| PB-package-verification | PASS | Necessary local checks have actual candidate-bound evidence; script behavior and failure cases are exercised; cloud/browser and other external limitations are named. Green tests do not override F1. |
| PB-package-handoff | PASS | Entry paths, usage, provenance manifest, actual checks, publication requirement and remaining environment limitations are documented without relying on author chat or declaring formal acceptance. |

No additional blocking defects were found in this review. Nonblocking note: the adapted UI Skill still says to invoke by full path while examples are repository-relative; examples work from the documented repository root. This wording can be aligned when that Skill is next edited and is not a reason to expand this repair.

## Frozen missing source notice (defect evidence, not a product fix)

Source: installed Ponytail 5.3.2 package LICENSE path above. SHA-256: `fb1bc6909ac3ef82d5c22106e32ef682b0cff66788fa915fb9b53b15c9d2f3ab`.

```text
MIT License

Copyright (c) 2026 DietrichGebert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Untested scope / authority

Actual Claude cloud launch, native automatic discovery, host identity/completion receipts, GitHub authentication and cloud filesystem/network policy: **NOT_RUN**. Browser, deployment, publishing, payment and cross-machine live-state recovery: **NOT_RUN**. None is relabeled PASS. This review reports findings only; the original controller decides acceptance under its fixed two-round process.
