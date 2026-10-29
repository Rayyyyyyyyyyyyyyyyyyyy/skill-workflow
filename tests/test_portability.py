"""Exercise real shipped sources after relocation, without a personal install."""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from scripts.check_portability import check


REPO = Path(__file__).resolve().parents[1]


class PortabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="claude-relocated-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "fresh clone"
        self.root.mkdir()
        for name in (".claude", "library", "scripts"):
            shutil.copytree(REPO / name, self.root / name, ignore=shutil.ignore_patterns("__pycache__"))
        for name in ("config", "policies"):
            shutil.copytree(REPO / "runtime-reference" / name, self.root / "runtime-reference" / name)
        for name in ("CLAUDE.md", "AGENTS.md", "workbench.py"):
            shutil.copy2(REPO / name, self.root / name)
        (self.root / "docs").mkdir()
        for name in ("WORKFLOW.md", "CLAUDE_CLOUD.md"):
            shutil.copy2(REPO / "docs" / name, self.root / "docs" / name)

    def test_moved_bundle_plans_and_dispatches_each_real_role(self):
        home = Path(self.temp.name) / "empty-home"
        home.mkdir()
        env = dict(os.environ, HOME=str(home), PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run([sys.executable, "scripts/check_portability.py"], cwd=self.root, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)
        code = '''
import json
from pathlib import Path
from workbench import Workbench
w=Workbench()
assert w.list()==[]
roles=json.loads(Path("library/roles.json").read_text())["roles"]
for role,pb in [("planner","clarify"),("researcher","research"),("designer","design"),("implementer","deliver"),("writer","deliver"),("integrator","integrate")]:
    slug="portable-"+role
    w.new(slug,"Validate a local portable method packet.")
    p={"scope":"prepare","planner":"fixture-planner","routing":{"maturity":"ready","reason":"Portable source test fixture.","missing_inputs":[]},"limits":{"max_rounds":2,"review_retries":0},"requirements":[{"id":"R1","text":"Load real packaged method sources."}],"tasks":[{"id":"check","playbook":pb,"role":role,"depends_on":[],"allowed_paths":["artifact.md"],"requirement_ids":["R1"],"acceptance":[{"id":"A1","description":"Real packaged sources load after relocation.","method":"Inspect pinned method packets.","requirement_ids":["R1"]}]}]}
    s=w.plan(slug,p)
    base=w.project(slug)/"workspace"
    (base/"plan-review.md").write_text("Test fixture: method packet coverage only, not semantic approval.")
    w.approve_plan(slug,{"plan_hash":s["plan_hash"],"reviewer":"fixture-reviewer","status":"PASS","reason":"Portable source fixture only.","evidence":"plan-review.md"})
    packet=w.dispatch(slug,"check","fixture-author")["packet"]
    assert packet["role_instructions"]==Path(roles[role]["source"]["path"]).read_text()
    assert packet["skill_instructions"]==[Path(x["path"]).read_text() for x in roles[role]["skills"]]
    assert str(Path.cwd()) in packet["workspace"]
    assert all(str(Path.cwd()) in b["role"]["path"] for b in s["plan"]["bindings"].values())
    assert "reviewer" in s["plan"]["bindings"]
print("Six author roles plus reviewer sources loaded from relocated repository.")
'''
        result = subprocess.run([sys.executable, "-c", code], cwd=self.root, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Six author roles", result.stdout)

    def test_missing_support_and_changed_skill_are_reported(self):
        self.assertEqual(check(self.root), [])
        support = self.root / ".claude/skills/domain-modeling/ADR-FORMAT.md"
        support.unlink()
        self.assertTrue(any("missing file" in error for error in check(self.root)))
        shutil.copy2(REPO / ".claude/skills/domain-modeling/ADR-FORMAT.md", support)
        skill = self.root / ".claude/skills/grilling/SKILL.md"
        skill.write_text(skill.read_text() + "\nChanged content.\n")
        self.assertTrue(any("checksum mismatch" in error for error in check(self.root)))

    def test_home_sources_and_symlinks_are_rejected(self):
        path = self.root / "library/roles.json"
        roles = json.loads(path.read_text())
        changed = copy.deepcopy(roles)
        changed["roles"]["planner"]["source"]["path"] = "/missing/home/role.md"
        path.write_text(json.dumps(changed))
        self.assertTrue(any("repository-relative" in error for error in check(self.root)))
        path.write_text(json.dumps(roles))
        source = self.root / ".claude/skills/grilling/SKILL.md"
        external = Path(self.temp.name) / "external.md"
        source.rename(external)
        source.symlink_to(external)
        self.assertTrue(any("symlink" in error for error in check(self.root)))
