# Issue tracker: Local Markdown

Issues and specs live as markdown files in the Project folder `projects/<slug>/` of this collection, one folder per Project. This holds even when the code lives in an external repo: the tickets stay here, next to PROJECT.md and LOG.md.

## Conventions

- One Project per directory: `projects/<slug>/`
- The spec is `projects/<slug>/spec.md`
- Implementation issues are one file per ticket at `projects/<slug>/issues/<NN>-<slug>.md`, numbered from `01`, never a single combined tickets file
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## Overrides for this repo

These take precedence over what `to-tickets` says:

- **No user approval round.** Skip the skill's "Quiz the user" step. The main session decides the breakdown itself and records the reasoning in LOG.md (see `docs/WORKFLOW.md` section 4). Ask the user only for the cases that section lists.
- **Tickets are always written to files** at `projects/<slug>/issues/<NN>-<slug>.md` (not `.scratch/`) before any dispatch. A ticket that exists only in the conversation cannot be dispatched or reviewed.
- **Required fields.** On top of the skill's template (What to build, Blocked by, Status, acceptance criteria), every ticket file must also have:
  - `**Scope:**` the areas or modules the work may touch
  - `**Out of scope:**` what the implementer must not do
  - `**Verify:**` commands that can be run as written, each with the result that means PASS. If something can only be checked by hand or in a browser, say so and say how.

## When a skill says "publish to the issue tracker"

Create a new file under `projects/<slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## When a skill says "resolve the ticket" or "close the work"

Set the ticket's `Status:` line to `done` and append a line under `## Comments` with the commit that resolves it. `implement-spec` step 8 uses this.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a file with one **child** file per ticket.

- **Map**: `projects/<slug>/map.md` (the Notes / Decisions-so-far / Fog body).
- **Child ticket**: `projects/<slug>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); a `Status:` line records `claimed`/`resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier**: scan `projects/<slug>/issues/` for files that are open, unblocked, and unclaimed; first by number wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (gist + link) to the map's Decisions-so-far in `map.md`.
