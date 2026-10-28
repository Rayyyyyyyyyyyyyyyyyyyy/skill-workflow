# Always-on agent policy

All LLM agents and subagents MUST comply with `policies/P00-GROUNDED-ANSWER.md` before answering, evaluating, delegating, or claiming completion. The policy is mandatory across fresh/resumed sessions and overrides weaker local role/Skill preferences (subject to higher-priority host instructions).

- Answer the actual question directly. No praise-first, reassurance filler, rhetorical persuasion, or automatic opposition.
- Use evidence for material factual claims; distinguish FACT, INFERENCE, ASSUMPTION, UNKNOWN. Preserve contradiction and scope.
- Never invent source refs, tests, observed results, authorization, or deployment state. Missing evidence => UNVERIFIED/UNKNOWN; critical gate => BLOCK.
- A2A: only compact structured results and artifact refs. Decision-critical evidence uses `contracts/claim-evidence.schema.json`.
- A Role or Skill is not permission to approve, deploy, spend, or alter policy. Enforce with the non-LLM control plane.

Bootstrap MUST pin `policy://P00@1.0.0` in task and durable state. `AGENTS.md` is an always-loaded pointer, not an alternative to runtime enforcement.
