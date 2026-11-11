"""Exercise real shipped sources after relocation, without a personal install."""
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
        shutil.copy2(REPO / "CLAUDE.md", self.root / "CLAUDE.md")
        (self.root / "docs").mkdir()
        for name in ("WORKFLOW.md", "CLAUDE_CLOUD.md"):
            shutil.copy2(REPO / "docs" / name, self.root / "docs" / name)

    def test_moved_bundle_passes_without_personal_install(self):
        home = Path(self.temp.name) / "empty-home"
        home.mkdir()
        env = dict(os.environ, HOME=str(home), PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run([sys.executable, "scripts/check_portability.py"], cwd=self.root, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

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
        path = self.root / ".claude/methods-manifest.json"
        original = path.read_text()
        changed = json.loads(original)
        changed["files"]["/missing/home/role.md"] = "0" * 64
        path.write_text(json.dumps(changed))
        self.assertTrue(any("repository-relative" in error for error in check(self.root)))
        path.write_text(original)
        source = self.root / ".claude/skills/grilling/SKILL.md"
        external = Path(self.temp.name) / "external.md"
        source.rename(external)
        source.symlink_to(external)
        self.assertTrue(any("symlink" in error for error in check(self.root)))
