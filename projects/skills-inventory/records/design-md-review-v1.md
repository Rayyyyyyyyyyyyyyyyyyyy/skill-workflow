# awesome-design-md — independent research review v1

Verdict: **PASS**, all five task criteria. This verifies the submitted research and its sources; it does not certify generated UI quality or complete the parallel local inventory task.

Reviewer `/root/claude_portability_review` is independent of the research author. Read the raw Project idea, formal R2/R3 and all five acceptance criteria from the actual packet, plus the pinned reviewer role/policy/review contract. Used the controller's detached workspace and inspected the two actual submitted files, not only author summaries.

## Bound object

- Candidate commit: `4bea70cdb1860ab0d20db94f51cb5d3a4a0f53e7`; reviewer HEAD matched.
- Review ID `04058979b8894dbba2eb9c759ffc981b`, round 1.
- Submission digest `ecc028e70a1822226090dfbaa6ae4ebeb88e081d3921a1e32c6f5eea9dff2438`.
- Contract digest `d7c639e047c6a8b17a32576dedf262de41c3f21274e15a924c7b2a7a3e260270`.
- Baseline digest `2ec7872e3421f4bae07bf56fe7ebae619b08c43ab79628ab0711760ca2ee5de6`.
- Both submitted file SHA-256 values independently match detached contents: `projects/skills-inventory/records/awesome-design-md/findings.md` and `sources.json`.

## Actual source checks

**FACT:** Using the GitHub connector, fetched the fixed commit and full recursive Git tree, README, LICENSE and the Claude/Linear/Stripe DESIGN.md samples. Commit `fcc70284932276d085f01ef9f83edde90b1258cb` points to tree `84becd0fc3b6c3646093fcf65d4d62637e09aabc`; the reported commit timestamp `2026-10-28T15:45:37Z` matched primary API metadata.

**FACT:** Independent calculation from the returned tree found `truncated: false`, 260 entries, 173 blob files, 84 `design-md/*/DESIGN.md` paths, zero `SKILL.md`, and zero preview HTML files. The entire 84-path set matches sources.json. The absence claims rely on the full tree, not a root-directory listing or search-result snippet. Tree blob extensions are Markdown, YAML, gitignore and LICENSE; the research's “document reference collection” positioning is supported at this commit.

**FACT:** Recomputed raw fetched UTF-8 file lengths, SHA-256 and Git blob SHA-1 for all five remote texts; each matches sources.json and its fixed tree entry:

| File | Bytes | SHA-256 |
|---|---:|---|
| README.md | 17,056 | ba50d84d7cfb4b607958e75549eec2cc0db8ef27bd6ce768de1a64c2d51d7e85 |
| LICENSE | 1,066 | 6d4bdc9a9cf30e7beb593475fdcdbf29f981ea6bd7923f202866145409f87b44 |
| design-md/claude/DESIGN.md | 33,586 | 3d972f34f8d4f33b442fa28220cf3b7ca2f13c0a97c468e3988148f82521f9df |
| design-md/linear.app/DESIGN.md | 24,354 | 30bd30e72c48a16e4bdbd010f2d1c85fab657c6fae3cc85389399aab10f9cb5f |
| design-md/stripe/DESIGN.md | 24,606 | 5c8806b7dd3e0c2554ccba9d1e2a7c78e7c6e50e44fcf6ff5daea6026f8a9ed9 |

**FACT:** README's file table names preview files which are absent from the fixed tree. The report correctly preserves this contrary evidence and avoids claiming ready previews exist. README recommends choosing/copying a design document and explicitly telling an agent to use it; report does not treat that as proof of universal automatic loading or generation quality.

**FACT:** Sample claims are supported by actual frontmatter and relevant prose/gaps: Claude cream/coral/serif marketing world with product/chat components outside scope; Linear near-black/lavender marketing world with light theme and some product/error states undocumented; Stripe file's inspired/Stripi name, indigo/navy/gradient and thin proprietary type interpretation. All three are alpha documents. The report accurately limits these to third-party analysis, not official brand standards or measured current sites.

**FACT:** LICENSE identifies MIT and VoltAgent 2026. Report's notice-preservation description matches it; its separate caveat avoids treating this license as a grant of logo, trademark or proprietary font rights. No legal clearance is claimed.

**FACT:** Read the relevant local Skill instructions and independently recomputed all five local source hashes. All match sources.json. claude-design covers goal/flow/structure/states before implementation; ui-ux-pro-max provides local query/data modes and targeted vs system-wide scope; impeccable reads existing DESIGN.md/surface briefs and prioritizes a pinned brief with bounded verification; popular-web-designs researches/adapts examples. design-taste-frontend explicitly excludes gradients and cream/terracotta or violet/indigo in page house rules, while its existing-brand clause permits only scoped exceptions. The report's comparison and concrete conflict warning are supported; reading these as research data did not invoke their executable setup/browser instructions.

## Individual criteria

| acceptance_id | Result | Basis |
|---|---|---|
| design-md-result | PASS | Fixed primary README/LICENSE/tree and actual examples support positioning, contents/use and qualification; five real local methods support the comparison. No installation or operation-success claim. |
| PB-design-md-coverage | PASS | Answers the repo's role, use, sample structure, license and relationship to existing methods. Explicitly limits reading to three examples and records unknown generation/current-site quality. |
| PB-design-md-sources | PASS | Pinned commit/tree, full path list, five independently verified remote blobs and five matching local source hashes provide retrievable/versioned evidence and date. |
| PB-design-md-calibration | PASS | Separates FACT/INFERENCE/UNKNOWN, documents README/tree contradiction, alpha/third-party limits, untested generation/browser behavior and distinct rights boundaries. |
| PB-design-md-handoff | PASS | findings.md links sources.json and fixed source URLs; recommendation remains a candidate input to design tasks, with no automatic adoption or extra job. Downstream can use accepted source files/commit and preserve original limitations. |

No necessary defects found. The exact visual reference to adopt remains a user/project decision; this research does not choose a brand or alter the Flow. Other 81 design bodies were not independently reviewed, and no claim about them beyond the tree is approved.

Primary refs: [fixed commit](https://github.com/VoltAgent/awesome-design-md/commit/fcc70284932276d085f01ef9f83edde90b1258cb), [recursive tree](https://api.github.com/repos/VoltAgent/awesome-design-md/git/trees/84becd0fc3b6c3646093fcf65d4d62637e09aabc?recursive=1), [README](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/README.md), [LICENSE](https://github.com/VoltAgent/awesome-design-md/blob/fcc70284932276d085f01ef9f83edde90b1258cb/LICENSE), and the three fixed sample URLs in sources.json. These were retrieved through read-only GitHub connector calls.

No product, plan, formal state or main index changes; only this reviewer evidence and the separately stored bound JSON report were written. No installs, removals, browser, cloud session, source commands or external writes. Controller retains acceptance authority.
