# Ponytail license rework

Fixed defect F1 from independent review round 1 by preserving the exact Ponytail 5.3.2 MIT copyright/permission notice in `.claude/skills/ponytail/LICENSE`. The notice was read from frozen reviewer evidence, not the mutable home installation.

- Frozen evidence: `projects/claude-cloud-portability/records/package-review-v1.md`, SHA-256 `2df939cb989fa2a169c8cfa893a3e7a2fa0db76dd11fe74030028f552eb2cef6`, review evidence commit `b9c7e23be005b647d79df5abca32da44d916d988`.
- Preserved source and shipped notice SHA-256: `fb1bc6909ac3ef82d5c22106e32ef682b0cff66788fa915fb9b53b15c9d2f3ab`.
- `.claude/methods-manifest.json` now includes the shipped file hash, upstream LICENSE hash, and frozen evidence provenance. No Role, Skill behavior, controller code, or other docs changed.

Checks: exact evidence and notice SHA-256 assertions passed; `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_portability.py` passed; final Git scope inspection found exactly the three assigned paths and `git diff --check` passed.

The prior 51 functional tests were not repeated for this license/manifest-only patch. Claude cloud, browser, network and external publication checks remain NOT_RUN. This rework record is not formal acceptance; the controller must submit this fixed version for independent second-round review.
