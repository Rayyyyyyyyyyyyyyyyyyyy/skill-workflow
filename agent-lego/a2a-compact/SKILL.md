---
name: a2a-compact
version: "2"
description: For every Agent-to-Agent task handoff, emit exactly one schema-valid JSON TASK or RESULT containing job_id, attempt_id and fence_generation. Store details in artifacts; return refs and status only.
---

# A2A Compact v2

- Output exactly one JSON object matching `message.schema.json`. No explanatory prose, reasoning, Markdown fences, greetings, or duplicate context.
- Preserve `job_id`, `attempt_id`, `fence_generation` from the TASK. Never infer or increment them in the worker.
- `DONE` requires artifact refs; `BLOCKED` requires reason and next action; `FAILED` requires reason.
- Store test logs, reviews, security analysis, specs and diffs in durable artifacts. Send only refs.
- Never fabricate artifact refs, pass claims, approval, SHA or permissions. `DONE` is not a merge or release authorization.
- The trusted controller validates schema, current attempt, fence, policy, budget, artifact existence and check evidence **outside the model**.
- A missing result or timeout is not success. A stale attempt result is discarded even if the message is schema-valid.
- v1 lacks attempt identity and must not be accepted for retryable Jobs. Pin one protocol version per Job; migrate both sender and receiver before enabling v2.

Example (illustrative only):

```json
{"v":"2","type":"RESULT","job_id":"JOB-001","attempt_id":"ATT-001-2","fence_generation":2,"state":"DONE","artifact_refs":["commit://abc"],"check_refs":["artifact://tests/001"]}
```
