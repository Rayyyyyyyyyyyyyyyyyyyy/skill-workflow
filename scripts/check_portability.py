"""Check the checked-in method bundle without network, installs or browser use."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import sys


def check(root: Path) -> list[str]:
    root = root.resolve()
    errors = []

    def local_file(raw):
        if not isinstance(raw, str) or not raw or "\\" in raw:
            raise ValueError(f"invalid repository path: {raw!r}")
        path = Path(raw)
        if path.is_absolute() or any(part in ("", ".", "..") for part in raw.split("/")):
            raise ValueError(f"source must be repository-relative: {raw}")
        cursor = root
        for part in path.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise ValueError(f"symlink source: {raw}")
        if not cursor.is_file():
            raise ValueError(f"missing file: {raw}")
        return cursor

    try:
        manifest = json.loads(local_file(".claude/methods-manifest.json").read_text())
        files = manifest["files"]
        if not isinstance(files, dict) or not files:
            raise ValueError("method manifest must contain file hashes")
        for relative, expected in files.items():
            actual = hashlib.sha256(local_file(relative).read_bytes()).hexdigest()
            if actual != expected:
                errors.append(f"method checksum mismatch: {relative}")
        roles = json.loads(local_file("library/roles.json").read_text())["roles"]
        for role, profile in roles.items():
            for source in [profile["source"], *profile.get("skills", [])]:
                raw = source["path"]
                local_file(raw)
                if raw not in files:
                    errors.append(f"method missing from manifest ({role}): {raw}")
        for relative in ("CLAUDE.md", "AGENTS.md", "docs/WORKFLOW.md", "docs/CLAUDE_CLOUD.md"):
            local_file(relative)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(str(exc))
    return errors


def main():
    errors = check(Path(__file__).resolve().parents[1])
    if sys.version_info < (3, 11):
        errors.append("Python 3.11+ is required")
    if not shutil.which("git"):
        errors.append("Git is required")
    for error in errors:
        print("FAIL: " + error, file=sys.stderr)
    if errors:
        return 1
    print("PASS: repo method files, hashes and Role/Skill paths; Python 3.11+ and Git available.")
    print("Node.js: " + ("available" if shutil.which("node") else "missing; design-taste scripts unavailable"))
    print("Not checked: Claude discovery/identity, cloud permissions, network or browser behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
