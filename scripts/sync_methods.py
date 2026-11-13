"""Regenerate the tool catalog and method-file hashes after adding or editing Skills/Roles.

Run from anywhere: python3 scripts/sync_methods.py
Writes library/CATALOG.md and the `files` map of
.claude/methods-manifest.json (the `packages` provenance is kept as written).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".claude/skills"
NATIVE_ROLES = ROOT / ".claude/agents"
MANIFEST = ROOT / ".claude/methods-manifest.json"

# Skills the Claude platform itself may provide; availability depends on the session.
PLATFORM_SKILLS = [
    ("deep-research", "多來源研究並寫成完整報告"),
    ("docs / docx / pdf / pptx / xlsx", "產生或讀寫文件、簡報、試算表、PDF"),
    ("skill-creator", "建立或改進 Skill 並跑評測"),
    ("dataviz", "做任何圖表或資料視覺化前先讀"),
    ("built-in-browser / chrome-browser / computer-use", "操作瀏覽器或桌面（需授權，見 CLAUDE.md）"),
    ("security-review / simplify", "Claude Code 內建的安全審查與精簡（`code-review` 指的是 repo 內 Matt 的版本）"),
]


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, str] = {}
    key = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            key, value = match.group(1), match.group(2).strip()
            data[key] = "" if value in (">", "|", ">-", "|-") else value
        elif key and line.startswith((" ", "\t")):
            data[key] = (data[key] + " " + line.strip()).strip()
    return {k: v.strip().strip('"').strip("'") for k, v in data.items()}


def short(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text).replace("|", "/")
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def skill_rows() -> list[str]:
    rows = []
    for skill in sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file()):
        meta = frontmatter(skill / "SKILL.md")
        how = "讀檔" if meta.get("disable-model-invocation") == "true" else "Skill 工具"
        rows.append(f"| `{meta.get('name', skill.name)}` | {how} | {short(meta.get('description', ''), 140)} |")
    return rows


def native_role_rows() -> list[str]:
    rows = []
    for role in sorted(NATIVE_ROLES.glob("*.md")):
        meta = frontmatter(role)
        if meta.get("name"):
            rows.append(f"| `{meta['name']}` | {short(meta.get('description', ''), 140)} |")
    return rows



def write_catalog() -> None:
    text = "\n".join([
        "# 工具目錄",
        "",
        "由 `scripts/sync_methods.py` 產生；新增或修改 Skill／Role 後重跑，不要手改。",
        "每接一個任務先掃過這份目錄，挑出這次用得上的 Skill 與角色，記到 PROJECT.md 的「工具」欄；做到一半需要別的就再加。",
        "",
        "## Skills（`.claude/skills/`）",
        "",
        "「呼叫」欄寫「Skill 工具」的，直接用 Skill 工具呼叫；寫「讀檔」的，這個 Skill 關掉了模型自動呼叫，"
        "要直接完整讀 `.claude/skills/<名稱>/SKILL.md` 再照做（使用者也可以自己打 `/名稱`）。",
        "Matt 工程系列（to-spec、to-tickets、triage、wayfinder、implement）的 issue tracker 設定已經寫在 "
        "`docs/agents/`：票放在 `projects/<slug>/` 的本機 Markdown，不必另跑 setup-matt-pocock-skills。",
        "",
        "| Skill | 呼叫 | 用途 |",
        "|---|---|---|",
        *skill_rows(),
        "",
        "## 平台可能提供的 Skills（依當次 session 實際清單為準）",
        "",
        "| Skill | 用途 |",
        "|---|---|",
        *[f"| `{n}` | {d} |" for n, d in PLATFORM_SKILLS],
        "",
        "## 原生角色（`.claude/agents/`，可直接當 subagent_type 使用）",
        "",
        "| 角色 | 用途 |",
        "|---|---|",
        *native_role_rows(),
        "",
        "## 專業角色（全域 `~/.claude/agents/`，不在 repo 裡）",
        "",
        "agency-agents 的專業角色裝在全域，session 的 subagent 類型清單上就有名稱和一行說明，直接用名稱開；"
        "派工時寫明要它用哪些方法與工具（不是只換口吻）。安裝方式與常用角色見根目錄 README「另外安裝」。",
        "",
    ])
    (ROOT / "library/CATALOG.md").write_text(text, encoding="utf-8")


def write_manifest() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = {}
    for base in (SKILLS, NATIVE_ROLES):
        for path in sorted(base.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts and path.name != ".DS_Store":
                files[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest["files"] = files
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    write_catalog()
    write_manifest()
    print(f"catalog: {len(skill_rows())} skills, {len(native_role_rows())} native roles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
